# http://localhost:8080/login - VSCode
# http://127.0.0.1:5000/login - cmd

from flask import Flask, redirect, request, render_template # type: ignore
# pip install Flask
app = Flask(__name__)

# Example regex validation (for demonstration purposes, not secure)
import re

import sqlite3

def get_db_connection():
    """Create and return a new database connection and cursor."""
    conn = sqlite3.connect('SampleFYProj.db')
    conn.row_factory = sqlite3.Row  # Optional: allows accessing columns by name
    cursor = conn.cursor()
    return conn, cursor


# Regex pattern for username validation (this is where the vulnerability might lie)
USERNAME_PATTERN = r"^[a-zA-Z0-9_']+$"  # Only allows alphanumeric characters and underscores, at least one character long


# In-memory storage for a single user (for demo purposes)
users = {
    "administrator_": "admin_123"  # Example user (username: administrator_, password: admin_123)
}

@app.route('/login', methods=['GET', 'POST'])
# This line creates a route in the Flask application that listens for requests to the URL '/login'.
# The 'methods' argument specifies that this route can handle both GET and POST HTTP requests.
# - GET: Used when the user initially visits the login page. The server responds by rendering the login form.
# - POST: Used when the user submits the login form with their username and password. The server processes this data to authenticate the user.
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate inputs
        if not username:
            error = "Enter a username"
        elif not re.match(USERNAME_PATTERN, username):
            error = "Username can only be alpha-numeric and underscores"
        elif not password:
            error = "Enter a password"
        else:
            # Check database for user
            conn, cursor = get_db_connection()
            try:
                query = f"SELECT password FROM users WHERE username = '{username}' AND password = '{password}'" 
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return "Welcome, " + username + "!"
                else:
                    error = "Invalid username or password!"
            except sqlite3.Error as e:
                error = f"Database error: {e}"
            finally:
                conn.close()
    return render_template('Login.html', error=error)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate inputs (not sufficient to prevent SQLi)
        if not username:
            error = "Enter a username"
        elif not re.match(USERNAME_PATTERN, username):
            error = "Username can only be alpha-numeric and underscores"
        elif len(username) > 25:
            error = "Username must be 25 characters or less"
        elif not password:
            error = "Enter a password"
        elif len(password) > 25:
            error = "Password must be 25 characters or less"
        else:
            conn, cursor = get_db_connection()
            try:
                # Check if username exists (vulnerable to SQLi)
                query = f"SELECT COUNT(*) FROM users WHERE username = '{username}'"
                cursor.execute(query)
                username_count = cursor.fetchone()[0]
                if username_count > 0:
                    error = "Username already exists."
                else:
                    # DANGER: Vulnerable query
                    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
                    cursor.execute(query)
                    conn.commit()
                    return redirect('/login')
            except sqlite3.Error as e:
                error = f"Database error: {e}"
            finally:
                conn.close()

    return render_template('CreateNew.html', error=error)


if __name__ == '__main__':
    # Create the users table if it doesn't exist
    conn, cursor = get_db_connection()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(25) UNIQUE,
                        password VARCHAR(25)
                    )''')
    conn.commit()
    conn.close()
    app.run(host='localhost', port=8080, debug=True)
