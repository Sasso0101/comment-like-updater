# Comment like updater
A simple Python comment updater based on the current like count of the comment's parent.
Uses [Google's Python Library](https://github.com/googleapis/google-api-python-client) to interface with YouTube APIs.
Based on a challenge started by [Overvolt Official](https://t.me/overVoltOfficial/4912).

## How it works
The program's logic is really simple and follows this high-level flowchart:
![Diagram](https://raw.githubusercontent.com/Sasso0101/comment-like-updater/main/docs/diagram.png)

All the programs functions are divided in... well, functions. Each function [does only one thing](https://en.wikipedia.org/wiki/Single-responsibility_principle), which helps keeking the code clean and tidy. The script uses 2 helper files to store the OAuth secrets (`secrets.json` and `credentials.json`) that Google provides and the OAuth credentials we got from the user (more on that later).

### Python stuff
Libraries and modules used:
 - [Google's OAuth Python module](https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.credentials.html) to manage the OAuth credentials
 - [Google's Auth Flow Python module](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html) for the authentication part
 - [Python's Request library](https://requests.readthedocs.io/en/master/) to make the requests
 - [Google's API Client Discovery](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html) and [error handling modules](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.errors-module.html) for interacting with YouTube's APIs
 ## Getting it working 🚀
To get this working you need a recent version of Python 3 and pip.
Steps to install:
1. Clone or download the repo from Github
    `git clone https://github.com/Sasso0101/comment-like-updater.git`
2. Generate a new OAuth client ID from [Google Console](https://console.developers.google.com/apis/credentials), choose Desktop Application as the type, download the JSON file and save it in the downloaded folder as `secrets.json`
3. Enable [YouTube's API](https://console.developers.google.com/apis/library/youtube.googleapis.com?id=125bab65-cfb6-4f25-9826-4dcc309bc508)
4. Install the required dependencies
	`pip install -r requirements.txt`
5. Change the `thread ID` in the main file. I suggest using the [documentation's Try It box](https://developers.google.com/youtube/v3/docs/commentThreads/list) to get it
6. Run the script! Follow the instructions to authorize the application. This is needed only once. The first time you'll run the script it'll also create a new comment if you didn't provide a valid `commentID`. To update the comment instead of creating new ones just paste the `commentID` you got in the first request into the code and now you're ready to go!

If you have any questions write me on [Telegram](https://t.me/sasso0101), I'll be happy to help! :)
