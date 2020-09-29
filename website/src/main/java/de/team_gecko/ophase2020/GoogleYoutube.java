package de.team_gecko.ophase2020;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;

import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.LiveBroadcastListResponse;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.Arrays;
import java.util.Collections;

public class GoogleYoutube {
  private YouTube service;

  public GoogleYoutube(HttpTransport httpTransport, Credential apiCredentials) {
    service = new YouTube.Builder(httpTransport, JacksonFactory.getDefaultInstance(), apiCredentials).build();
  }

  /**
   * Call function to create API service object. Define and execute API request.
   * Print API response.
   * 
   * @throws IOException
   *
   * @throws GeneralSecurityException, IOException, GoogleJsonResponseException
   */
  public void something() throws IOException {
    YouTube.LiveBroadcasts.List request = service.liveBroadcasts()
            .list(Arrays.asList("id", "snippet", "status"));
        LiveBroadcastListResponse response = request.setBroadcastStatus("upcoming")
            .setMine(true)
            .execute();
    System.out.println(response);
  }
}
