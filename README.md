# Gmail rules

Python script that integrates with Gmail API and performs some rule based operations on emails.

Prerequisites

To run this application, you need the following prerequisites:

Python 3.6 or greater.
A Google Cloud Platform project with the API enabled. To create a project and enable an API, [refer to Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
Note: For this application, you are enabling the "Gmail API".
Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials).
A Google account with Gmail enabled.


Step 1: Create Virtual Environment & Install Requirements
To create virtual environment, run the following commands:
```
cd app/
python3 -m venv venv
source venv/bin/activate
```
To install requiremnts, run the following command:
```
pip install -r requirements.txt
```
Step 2: Authenticate to Google’s Gmail API using OAuth and fetch a list of emails from your Inbox.
run the following command:
```
python get_email.py
```

Step 3: Run the Application
run the following command:
```
python main.py
```
when you run this command a development server will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)
open this URL in the browser and configure the rules
Once you configure rules, submit the rules, if the rules match with existing email in the database.

then matched rules will be added in rules.json file and messages will be displayed in the page.
