# Conference Organization App
![](screenshot.png)
Cloud-based API server that supports a provided conference organization application that exists on the web. The API supports the following functionality found within the app: user authentication, user profiles, conference information and various manners in which to query the data.

## View the app online

You can view the app online [here](https://conforgapp.appspot.com/).

## Run the app in your browser

1. Clone this repository by typing `$ git clone https://github.com/kalpetros/projects.git`
2. [Download App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
3. cd to the file you downloaded
4. Open your terminal and type: `$ ./dev_appserver.py clone_app_from_step_one`
5. Visit localhost:8000
6. Click default under Instances

## View the APIs explorer
1. Visit localhost:8080/_ah/api/exlorer
2. Click conference API to view the endpoints

If you don't see your endpoints click the shield next to the url (Google Chrome) and load the unsafe scripts.

**Update:** APIs explorer doesn't work with Google Chrome. Try with a different browser.

## Design decisions

#### What were your design choises for session and speaker implementation?

The first design decision I took is to model my endpoints (session, speaker) as children of Conference.

Also when a user creates a session it is mandatory to include the session's name, type and its speaker because logically a session without those attributes could not exist.

#### Think about other types of queries that would be useful for this application. Describe the purpose of 2 new queries and write the code that would perform them.

Some usesful queries would be session by type and by speaker in a user's wishlist where the user can filter all the sessions in his wishlist to return the sessions he wants by their type for example (workshops, lectures) or by their speaker.

#### Let’s say that you don't like workshops and you don't like sessions after 7pm. How would you handle a query for all non-workshop sessions before 7pm? What is the problem for implementing this query? What ways to solve it did you think of?

The problem is with NDB. With NDB you can query for items for a given date but not for a given time. i.e. You can't return sessions before or after 7pm.
A workaround to this problem is to create a Python function that after quering for all sessions, excluding workshops you split all sessions into days and remove sessions after 7pm in those days. Then the function merges the sessions and returns a list of sessions before 7pm.
