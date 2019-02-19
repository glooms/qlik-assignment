## Access

To access the deployed app go to:

[https://qlik-assignment.appspot.com/][app]

  [app]: https://qlik-assignment.appspot.com/

You can also use the client from a python interpreter by:

`python -i run_client.py`

The app only responds in json format.

## Building

To build run the following commands:

`virtualenv -p python3 venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

## Run locally

If you want, running the application locally with virtual environment activated is done as so:

`python main.py`

## Deploying

The app is deployed to the Google App Engine.
This requires Google Cloud SDK and OAuth2 identification after
which the app can be deployed as:

`gcloud app deploy --project=qlik-assignment`

unfortunately, my database solution does not seem to be compatible
with GAE and I did not have time to implement another solution.
This resulted in that any manipulation of the database is prohibited,
meaning any requests that modify the database, such as post or delete,
 don't really work. 

But, since you can still access the data inside the database, populated the database so
that one can at least perform get requests properly. (You can populate the database
and then deploy it to the cloud.)

Furthermore, there is a minimal config file `app.yaml` used for the deployment. It simply
specifies the languages and urls used.

## Architecture

The application is split into two main parts, the database and the endpoints.

All database classes are found under `service/models` as well as an interface file used
for all communication with the database.

The endpoints are found under `service/blueprints` and are split into two files, `user.py` and `message.py`,
where `user.py` contains routes for creating, listing and getting specific users as well as the index route.
The `message.py` file contains the routes for all operations regarding messages such as listing, creating and deleting.

The `service/__init__.py` file is what creates the app, db and registers the blueprints (routes/endpoints).

The `main.py` file runs the server (locally) as well as initiates (and wipes) the database so that it is in a clean state.
Database used here is sqlite3 which does not seem to work on Google App Engine but works fine locally.

Lastly, `service/config.py` specifies the path to the database.

## Tests & Client

Tests can be found under `tests/` and are generally run as:

`python -m unittest tests/blueprint\_tests.py'
`python -m unittest tests/model\_tests.py'

note that to run the blueprint tests the server must be running locally.

Furthermore, there is a client class located in the `client/client.py` file which
can be used to run locally or remote. You can create an instance of the class in the
python interpreter by running:

`python -i run\_client.py [local]`

where [local] is an optional argument, either none or "local", which specifies if the
client should connect to localhost or the deployed app.

## API

**GET**     `/user`  
Returns: A list of all created users.

**POST**    `/user`  
payload: name  
Creates a new user with the specified name.  
Returns: The created user.

**GET**     `/user/<user_name>`  
Returns: The user with the specified username.

**GET**     `/user/<user_name>/message`  
Returns: A list of all received messages by the user.

**POST**    `/user/<uesr_name>/message`  
payload: name, message  
Creates and sends a message from the user with the name in the url to the user specified in
the payload.  
Returns: The message created.

**GET**     `/user/<user_name>/message/<message_id>`  
Returns: The message with the specified id if it was either sent or received by the user.

**DELETE**  `/user/<user_name>/message/<message_id>`  
Deletes the message specified by the id if it was either sent or received by the user.  
Returns: Whether the operation was successful or not

**GET**     `/user/<user_name>/message/sent`  
Returns: A list of all messages sent by the user.

I recommend glancing over the `client/client.py` file if there is any confusion regarding
payloads or urls since all the requests listed here can be called from the client.
