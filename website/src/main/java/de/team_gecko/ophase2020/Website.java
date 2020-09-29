package de.team_gecko.ophase2020;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.calendar.CalendarScopes;
import com.google.api.services.youtube.YouTubeScopes;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.Arrays;
import java.util.Collection;

public class Website {

  public static void main(String... args) throws IOException, GeneralSecurityException, InterruptedException {
    // Creates an authorized Credential object. Loads client secrets.
    var credentialsFile = Website.class.getResourceAsStream("credentials.json");
    if (credentialsFile == null) {
      throw new FileNotFoundException("No Google API credentials.");
    }
    var jsonFactory = JacksonFactory.getDefaultInstance();
    GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(jsonFactory, new InputStreamReader(credentialsFile));

    final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
    final Collection<String> SCOPES = Arrays.asList(YouTubeScopes.YOUTUBE, CalendarScopes.CALENDAR_READONLY);

    // Build flow and trigger user authorization request.
    GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(
        HTTP_TRANSPORT, jsonFactory, clientSecrets, SCOPES)
        .setDataStoreFactory(new FileDataStoreFactory(new java.io.File("google_tokens")))
        .setAccessType("offline")
        .build();
    LocalServerReceiver receiver = new LocalServerReceiver.Builder().setPort(8888).build();
    Credential apiCredentials = new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");

    GoogleCalendar calendar = new GoogleCalendar(HTTP_TRANSPORT, apiCredentials);
    GoogleYoutube youtube = new GoogleYoutube(HTTP_TRANSPORT, apiCredentials);
    EventManager eventManager = new EventManager(calendar, youtube);

    eventManager.triggerEvent();

    while (true) {
      Thread.sleep(1000*60*5);
      eventManager.triggerEvent();
    }
  }
}