#!/usr/bin/env python3.7
import os, requests, google.auth, google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors, pytz
from datetime import datetime
from os import path
tz = pytz.timezone('Europe/Rome')

''' Returns OAuth credentials (if they don't exist ask for new ones) '''
def getCredentials():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    # File containing the secrets obtained from https://console.developers.google.com/apis/credentials
    secrets_file = "secrets.json"
    # File containing the OAuth credentials granted from the user
    credentials_file = "credentials.json"

    # Checks if we altredy have OAuth credentials
    if not path.exists(credentials_file):
        # If they don't exist start and auth flow in the console
        credentials = login(secrets_file, scopes, credentials_file)
    else:
        # Otherwise just get the credentials from the JSON file
        try:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(credentials_file, scopes)
            if not(credentials.valid):
                request = google.auth.transport.requests.Request()
                credentials.refresh(request)
        except google.auth.exceptions.RefreshError:
            # If the credentials can't be refershed initiate a new oAuth flow
            credentials = login(secrets_file, scopes, credentials_file)

    return credentials

''' Starts an start and auth flow in the console
    Returns a credentials object and updates the credentials file '''
def login(secrets_file, scopes, credentials_file):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    secrets_file, scopes)
    credentials = flow.run_console()
    with open(credentials_file, "w") as f:
        f.write(credentials.to_json())
    return credentials

''' Returns current number of likes '''
def getLikes(youtube, threadID):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        id=threadID,
    )
    response = request.execute()
    return response['items'][0]['snippet']['topLevelComment']['snippet']['likeCount']

''' Returns new comment message '''
def getMessage(likes):
    lastUpdated = datetime.now(tz)
    lastUpdated= lastUpdated.strftime("%d/%m/%Y %H:%M")
    message = "🤖 Lo hai detto *" + str(likes) + " volte* ! 🤖\n\n\n_Ultimo aggiornamento: " + lastUpdated + "_\nQuesto messaggio si aggiorna automaticamente  ogni 10 minuti _circa_ perché Google è tirchia e se faccio più richieste mi fa pagare 😂\nScritto in python 🐍 e hostato su GitHub :)\nhttps://github.com/Sasso0101/comment-like-updater"
    return message

''' Insert a new reply in the given thread '''
def insertComment(youtube, threadID, message):
    request = youtube.comments().insert(
        part="snippet",
        body={
          "snippet": {
            "parentId": threadID,
            "textOriginal": message
          }
        }
    )
    response = request.execute()
    return response

''' Update existing comment '''
def updateComment(youtube, commentID, message):
    request = youtube.comments().update(
        part="id,snippet",
        body={
          "id": commentID,
          "snippet": {
            "textOriginal": message
          }
        }
    )
    response = request.execute()
    return response

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    threadID = "YOUR_THREAD"
    commentID = threadID + ".YOUR_COMMENT"

    credentials = getCredentials()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    likes = getLikes(youtube, threadID)
    message = getMessage(likes)
    try:
        response = updateComment(youtube, commentID, message)
    except googleapiclient.errors.HttpError:
        # If the comment doesn't exist create a new one
        response = insertComment(youtube, threadID, message)
    print(response)

if __name__ == "__main__":
    main()