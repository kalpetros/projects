# Conference Organization App
![](screenshot.png)
Cloud-based API server that supports a provided conference organization application that exists on the web. The API supports the following functionality found within the app: user authentication, user profiles, conference information and various manners in which to query the data.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.

## View the app online

You can view the app online [here](https://conforgapp.appspot.com/).

## View the APIs explorer
1. Visit localhost:8080/_ah/api/exlorer
2. Click conference API to view the endpoints

If you don't see your endpoints click the shield next to the url (Google Chrome) and load the unsafe scripts.

**Update:** You might get an error message if you are trying to access your local APIs explorer using Google Chrome. That is because the APIs Explorer is loaded over HTTPS, but your API when running locally is hosted on HTTP.

[Suggested solution from Google:](https://developers.google.com/explorer-help/#hitting_local_api)
>To resolve this using Chrome, you must start a Chrome session with special flags as follows:
```
[path-to-Chrome] --user-data-dir=test --unsafely-treat-insecure-origin-as-secure=http://localhost:port
```
or a more concrete example:
```
 /usr/bin/google-chrome-stable --user-data-dir=test --unsafely-treat-insecure-origin-as-secure=http://localhost:8080
```
You should only do this for local testing purposes, in which case you can ignore the warning banner displayed in the browser.

## Design decisions

#### What were your design choises for session and speaker implementation?

The first design decision I took is to model my endpoints (session, speaker) as children of Conference.

Also when a user creates a session it is mandatory to include the session's name, type and its speaker because logically a session without those attributes could not exist.

#### Think about other types of queries that would be useful for this application. Describe the purpose of 2 new queries and write the code that would perform them.

Some usesful queries would be session by type and by speaker in a user's wishlist where the user can filter all the sessions in his wishlist to return the sessions he wants by their type for example (workshops, lectures) or by their speaker.

#### Let’s say that you don't like workshops and you don't like sessions after 7pm. How would you handle a query for all non-workshop sessions before 7pm? What is the problem for implementing this query? What ways to solve it did you think of?

The problem is with NDB. With NDB you can query for items for a given date but not for a given time. i.e. You can't return sessions before or after 7pm.
A workaround to this problem is to create a Python function that after quering for all sessions, excluding workshops you split all sessions into days and remove sessions after 7pm in those days. Then the function merges the sessions and returns a list of sessions before 7pm.

[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
