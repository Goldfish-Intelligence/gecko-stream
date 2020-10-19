import os
import pickle
from re import template
import jinja2
import datetime
import pytz
from dateutil import parser
from pytchat import LiveChat
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import locale

# This will be prepended in the YouTube description before the calendar description
YOUTUBE_HEADER = """
Hauptchat: http://dc.team-gecko.de (Dann #chat)\n
O-Phase 2020 FC Gecko: https://www.o-phase.com https://www.team-gecko.de\n
\n
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/youtube'
]

# You can get this from Discord server settings. Then set as environment variable.
DISCORD_NOTIFICATION_WEBHOOK = os.environ['DISCORD_NOTIFICATION_WEBHOOK']
DISCORD_CHAT_WEBHOOK = os.environ['DISCORD_CHAT_WEBHOOK']

locale.setlocale(locale.LC_TIME, 'de_DE.utf8')

creds = None

def main():
    global creds
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    events = getStreamEvents()

    previousEvent = None
    futureEvent = None
    now = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
    for event in events:
        startTime = parser.parse(event["start"]["dateTime"])
        if startTime < now:
            previousEvent = event
        else:
            futureEvent = event
            break

    activeEvent = None
    if previousEvent:
        print("Event previous: {} - {} \n".format(previousEvent["summary"], previousEvent["start"]["human"]))
    else:
        print("Previous event not existing.\n")
    if futureEvent:
        print("Event upcoming: {} - {} \n".format(futureEvent["summary"], futureEvent["start"]["human"]))
    else:
        print("Upcoming event not existing.\n")
    useUpcoming = yesNoPrompt("Use upcoming event as currently active (previous if no)?")
    if useUpcoming:
        activeEvent = futureEvent
    else:
        activeEvent = previousEvent
    
    if not activeEvent:
        print("Error: event does not exist")
        os.exit(1)

    activeYoutubeLink = None
    doCreateYoutubeLink = yesNoPrompt("Create new YouTube event?")
    if doCreateYoutubeLink:
        activeYoutubeLink = createYoutubeLink(activeEvent)
    else:
        activeYoutubeLink = input("Please paste YouTube link (not YT Studio / Live Control) for further processing.")
    
    doCreateWebsite = yesNoPrompt("Regenerate Website?")
    if doCreateWebsite:
        createWebsite(events, activeEvent, activeYoutubeLink)

    doPublishWebsite = yesNoPrompt("Publish website?")
    if doPublishWebsite:
        publishWebsite()

    doCreateDiscordNotification = yesNoPrompt("Send notifcation for active event and YouTube link?")
    if doCreateDiscordNotification:
        createDiscordNotification(activeEvent, activeYoutubeLink)

    doPipeYoutubeChat =yesNoPrompt("Start Youtube => Discord Chat bridge?")
    if doPipeYoutubeChat:
        pipeYoutubeChat(activeYoutubeLink)
    

def yesNoPrompt(prompt):
    while True:
        userChoice = input("{} [y/n]: ".format(prompt))
        if userChoice.lower() == "y":
            return True
        elif userChoice.lower() == "n":
            return False
        else:
            print("Please type 'y' or 'n'\n")


def getStreamEvents():
    service = build('calendar', 'v3', credentials=creds)

    results = service.events().list(
        calendarId='93fj10tioa3bq86qtdlcfq3cjs@group.calendar.google.com', maxResults=50, singleEvents=True,
        orderBy='startTime', timeMax="2020-11-01T00:00:00+02:00",
        timeMin="2020-10-19T00:00:00+02:00").execute()["items"]

    for event in results:
        event["start"]["human"] = parser.parse(event["start"]["dateTime"]) \
            .strftime("%a %-d. Okt %H:%M Uhr")
        event["end"]["human"] = parser.parse(event["end"]["dateTime"]) \
            .strftime("%a %-d. Okt %H:%M Uhr")
        event["calendarBgColor"] = "#0297df"
        if "colorId" in event:
            if event["colorId"] == "8":
                event["calendarBgColor"] = "#616161"
            if event["colorId"] == "3":
                event["calendarBgColor"] = "#8e24aa"
            if event["colorId"] == "1":
                event["calendarBgColor"] = "#7986cb"

    return results

def createYoutubeLink(event):
    youtube = build(
        'youtube', 'v3', credentials=creds)

    description = YOUTUBE_HEADER
    if "description" in event:
        for line in event["description"].split('\n'):
            if not line.startswith("//"):
                description += line + "\n"

    request = youtube.liveBroadcasts().insert(
        part="snippet,contentDetails,status",
        body={
          "contentDetails": {
            "enableAutoStart": True,
            "enableDvr": True,
            "enableAutoStop": True,
            "monitorStream": {
              "enableMonitorStream": False
            },
            "enableLowLatency": False
          },
          "snippet": {
            "title": event["summary"],
            "scheduledStartTime": event["start"]["dateTime"],
            "description": description
          },
          "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False
          }
        }
    )
    response = request.execute()

    print("Please visit https://studio.youtube.com/video/{}/livestreaming to complete setup.".format(response["id"]))

    return "https://youtu.be/{}".format(response["id"])

def createWebsite(events, activeEvent, activeYoutubeLink):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"), autoescape=True)
    templates = env.list_templates()

    for event in events:
        event["ignore"] = False
        if "description" not in event:
            continue
        for line in event["description"].split('\n'):
            if line.startswith("//ignore") or line.startswith("// ignore"):
                event["ignore"] = True

    context = {
        "events": events,
        "activeEvent": activeEvent,
        "youtubeLink": activeYoutubeLink,
    }
    for template in templates:
        env.get_template(template).stream(context).dump("out/" + template)

def publishWebsite():
    os.system("./website_push.sh")
    print("Published at https://team-gecko.de. GitHub might need a minute to refresh.")

def createDiscordNotification(activeEvent, activeYoutubeLink):
    discord_msg = "Wir sind live!\n{}\nGeplanter start: {}\n{}".format(
        activeEvent["summary"], activeEvent["start"]["human"], activeYoutubeLink)
    requests.post(DISCORD_NOTIFICATION_WEBHOOK, json={
        "content": discord_msg
    })


def pipeYoutubeChat(activeYoutubeLink):
    livechat = LiveChat(activeYoutubeLink)
    while livechat.is_alive():
        try:
            chatdata = livechat.get()
            for c in chatdata.items:
                print(f"{c.datetime} [{c.author.name}]- {c.message}")
                requests.post(DISCORD_CHAT_WEBHOOK, json={
                    "content": c.message,
                    "username": f"YT: {c.author.name}"
                })
                chatdata.tick()
        except KeyboardInterrupt:
            livechat.terminate()
            break
    print("Terminated chat bridge.")


if __name__ == "__main__":
    main()
