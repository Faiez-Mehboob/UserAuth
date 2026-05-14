# User Authentication via Socket Programming

A Computer Networks course project demonstrating user authentication over TCP sockets. The system separates authentication logic from the web layer — a custom auth server handles all credential management, and a Flask web server communicates with it over sockets.

## Architecture

Two servers run independently:

- **AuthServer** — a raw TCP socket server that handles signup, login, password changes, and note storage. Passwords are hashed using bcrypt and user data is stored in a SQLite database. Notes are stored per-user in a JSON file.
- **WebServer** — a Flask app that serves the frontend. It forwards all auth and data requests to the AuthServer over TCP.

## Setup

```bash
pip install -r requirements.txt
```

**Start the Auth Server:**
```bash
cd AuthServer
python AuthServer.py
```

**Start the Web Server** (in a separate terminal):
```bash
cd WebServer
python app.py
```

By default, both use `localhost:9999` for the auth connection. You can override this:
```bash
python AuthServer.py --Host 0.0.0.0 --Port 8888
python app.py --AuthHost 0.0.0.0 --AuthPort 8888
```

Then open `http://localhost:5000` in your browser.

## Features

- User signup and login
- bcrypt password hashing with salting
- Password change
- Session-based access control
- Basic note-taking dashboard (create, edit, delete notes)

## Tech Stack

- Python (sockets, threading)
- Flask
- SQLAlchemy + SQLite
- bcrypt