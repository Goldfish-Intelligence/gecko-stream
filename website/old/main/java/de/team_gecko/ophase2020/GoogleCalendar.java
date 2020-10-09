package de.team_gecko.ophase2020;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.Calendar;
import com.google.api.services.calendar.model.Event;
import com.google.api.services.calendar.model.Events;
import java.io.IOException;
import java.util.List;

public class GoogleCalendar {
  private Calendar service;

  public GoogleCalendar(HttpTransport httpTransport, Credential apiCredentials) {
    service = new Calendar.Builder(httpTransport, JacksonFactory.getDefaultInstance(), apiCredentials).build();
  }

  public List<Event> readCalendar() throws IOException {

    // List the next events from the primary calendar.
    Events events = service.events().list("primary")
        .setTimeMax(DateTime.parseRfc3339("2020-11-01T00:00:00+02:00"))
        .setTimeMin(DateTime.parseRfc3339("2020-10-19T00:00:00+02:00"))
        .setOrderBy("startTime")
        .setSingleEvents(true)
        .execute();
    List<Event> items = events.getItems();

    //remove later
    for (Event event : items) {
      DateTime start = event.getStart().getDateTime();
      if (start == null) {
        start = event.getStart().getDate();
      }
      System.out.println("event: " + event.getDescription() + " at time " + event.getOriginalStartTime().toString());
    }

    return items;
  }
}
