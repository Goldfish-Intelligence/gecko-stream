# Usage (when everything is set up)

Navigate to `kamerakind/src/` and execute `source source.sh`. You can now run
kamerakind with `python3 kamerakind.py`.

You will be presented with a bunch of questions. Every action is executed after
you answered the singular question.

## Use upcoming event as currently active (previous if no)?

Select which of the presented events is relevant at the moment. It will be used
as the 'active' event. This means its description and other calendar-features
will be used in the main box of the website or for creating the live event.

## Create new YouTube event?

Create a new YouTube Live stream. It will generate a description based on what
is written in the calendar event and the YOUTUBE_HEADER variable in
`kamerakind.py`.

After creation you will be prompted to visit an URL leading to YouTube studio.
This required to be done to finish setting up the new broadcast event.

If a broadcast event was allready created in another run of this script, answer
with no. In thi scase provide a link to the broadcast to the prompt. This is not
the link to YouTube Studio page, but to the normal viewing site.

## Regenerate Website?

(Re-)Generate the website into the `out/` dir. This will refresh all events with
information from the Google Calendar. It will also place a link and other
information for the active stream very prominently on the top of the page.

## Publish website?

Push what currently resides in th `out/` dir to https://team-gecko.de

## Send notifcation for active event and YouTube link?

Does exactly what it says. You probably want to answer this question with yes,
just after hitting 'stream' in OBS.

## Start Youtube => Discord Chat bridge?

Starts an infinte loop and forwards all messages from YouTube chat to Discord.
Only works one-way. Leave running until event is over.

Note: Thera is an about 2 seconds delay that can not be fixed without bad
consequences.