# EventTracker
#### Video Demo: https://youtu.be/bZM6PUbXBZw
#### Description:
Event Tracker allows user to input important dates and events into a database and allows user to access events by date or type of events. User can use Event Tracker to see if a certain day is available to minimize double booking events and can use the view by type function to access history of important dates (eg. medical appointments)

Event Tracker was written in Python with Flask framework, with elements of javascript added to certain HTML pages and user data stored in the SQL database "eventtracker.db". Upon running the app, most of the functionalities of these app are viewable at the index page. However the right side of the navigation bar differs depending on whether the user has logged in, if the user is not logged in, the 2 options on the right will be "login" and "register", otherwise just a welcome message and the "logout" function.

If the user's not logged in, although the functionalities "add" (at center of the page), "upcoming" and "track" are still viewable, upon clicking on these functions, user will be redirected to the login page until the user is logged in.

Flask's session is used to implement "login", "register" and "logout". Register, upon post with all fields filled out, will execute a SQL query to insert new user into database's user table with unique username, user id and password.

The "add" function is accessible via "index.html", if the form was submitted via post and all required fields are filled out. The application will execute a SQL query inserting into eventtracker.db's table of events a row with the user id, and information from the form's "type", "date" and "details" fields. A diction of event type was created so that the user cannot maliciously modify the option to add event of a type that's not included in the app.

The "upcoming" function returns a html page containing a table of all of user's upcoming events in the next 7 days in ascending order, starting from the time of accessing this page. Upon visiting the page via get, a SQL query is executed which selects the event date and time, type of events, and any details of the event.

The "track" function allows user to track events in 2 ways, by date if the user is looking to see if a particular day is available to book events, and by type, if user wants a history and upcoming list of all events of a certain type. "track.html" only contains 2 buttons redirecting user to 2 other functions, "track by date" and "track by type".

"trackbydate" upon post, with date filled out properly, will return a html page with a table of all of the events on that day.

"trackbytype" allows user to select from a dropdown menu, all of the different event types, and upon submit displays a table of all events of the type which user selected. There were 2 ways for me to implement this. I could either create multiple html pages, one for each event type, and redirect user to the html page that was asked for. Or I could include all the tables on the page but set the display as none so that it wouldn't display, then use Javascript to display only the table of choice upon submission of the form. From a practical standpoint, it would probably be better to deploy the first method via flask because as the database gets bigger and the user input more information, pre-including all of the tables will just result in more loading time. However I chose the latter just to give myself a bit more practice with Javascript.

"error.html" was borrowed from CS50 Finance's apology function, it was used for a function called error() so that the app can display specific message based on different improper uses of the app from the user. error(message) takes a message input, which will indicate the improper use by the user(eg. password does not match) and return an html page containing that message to the user.

"styles.css" was used for the styling elements of the HTML pages as well to design the navigation bar, Bootstrap was also used for the design of tables and buttons.