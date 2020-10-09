package de.team_gecko.ophase2020;

import com.google.api.services.calendar.model.Event;

import java.io.IOException;
import java.util.List;

public class EventManager {

  GoogleCalendar calendar;
  GoogleYoutube youtube;

  public EventManager(GoogleCalendar calendar, GoogleYoutube youtube) {
    this.calendar = calendar;
    this.youtube = youtube;
  }

  public void triggerEvent() throws IOException {
    //List<Event> calendarEvents = calendar.readCalendar();
    youtube.something();

    //Youtube stream

    //website erstellen

    //notifications senden

    //
  }
}
