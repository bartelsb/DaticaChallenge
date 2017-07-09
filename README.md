# Coding Challenge: REST API

## Objectives

Assess the candidate's:

- programming skill and ability to adapt it to a potentially new area/concept

- programming style, structure, organization

- ability to understand a prescribed problem and deliver results in a short time window

- ability to interact with a backend datastore

- ability to use basic version control operations

## Parameters

- Programming language: Python, Golang

- Database: sqlite, MySQL, or PostgreSQL

- Recommended frameworks: Negroni, Falcon, etc (your choice)

- Version control: Git

- Send a link to the repository when finished

## Problem Statement

Implement a simple REST API that allows a user to sign up and provide a username and password along with additional optional JSON data (e.g., email, address, phone). The base route (GET /) will display JSON along with user information if the user has already authenticated. The user may also update or delete their account information.

#### Routes for the REST API

- Base route

    - GET /

        - Outputs JSON containing “Hello World” when not authenticated.

        - If a session token is present and valid, outputs the username and any additional JSON data for the authenticated user.

- User routes

    - POST /user

        - The sign-up route. Requires a username and password along with optional JSON data.

    - GET /user/{username}

        - Returns the given user’s data.

    - PUT /user/{username}

        - Updates the given user’s JSON data.

        - Don’t worry about updating username and/or password.

    - DELETE /user/{username}

        - Deletes the given user entirely.

- Authentication routes

    - POST /auth

        - Takes in a username/password and returns a session token to be used on /user for GET/PUT/DELETE.

    - DELETE /auth

        - Invalidates the user’s session token.

#### Implementation Requirements

- The base (GET /), authentication (POST /auth) and sign-up (POST /user) routes are the only cases where a session token is not strictly required.

- The password should not be stored in plaintext within the backend database.

- Users may not modify, view, or delete other user's accounts.

- Don’t worry about robust error handling. We will not be evaluating that in the interest of time.

- HTTP return codes are up to your discretion.

#### Bonus

- Allow users to specify arbitrary additional JSON data when creating their account.

- Add the concept of administrative users who can modify other user's accounts.

- Automated unit and/or integration tests.

- Use Redis to store and retrieve session data, having each token expire after 24 hours.


## Instructions for running and testing project

### Required software

- Python (3.6 or higher because I made use of the secrets module)

- Redis 3.2 - I used the Windows .msi found [here](https://github.com/MicrosoftArchive/redis/releases), but as long as you have a Redis server running locally and listening to port 6379, it should work

- Falcon - Just run 'pip install falcon' to get the latest version

- Waitress if on Windows ('pip install waitress', Gunicorn if on a Unix-based system ('pip install gunicorn')

### Instructions for running

- Start the server with 'waitress-serve --port=8000 RESTServer:app' if using Waitress, with 'gunicorn RESTServer:app' if using Gunicorn. I only tested using Waitress, but Falcon's documentation indicates that they both should work.

- Make web requests using a tool such as curl or [HTTPie](https://github.com/jakubroztocil/httpie). You can install HTTPie with 'pip install --upgrade httpie'.

- The request for signing up might look something like this: 'http --form POST localhost:8000/auth username=ben password=pass'.
