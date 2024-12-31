import requests

# Step 1: Define the login URL and credentials
login_url = "http://127.0.0.1:8000/login/"
login_data = {
    "username": "medical-admin",  # Replace with your actual username
    "password": "chatbotuser"   # Replace with your actual password
}

# Step 2: Start a session
session = requests.Session()

# Step 3: Log in to obtain a session
login_response = session.post(login_url, data=login_data)

# Step 4: Check if login was successful
if login_response.status_code == 200:
    print("Login successful!")
    
    # Step 5: Access the protected endpoint
    url = "http://127.0.0.1:8000/doctors/"
    response = session.get(url)

    # Step 6: Check the response
    if response.status_code == 200:
        print(response.json())  # Print the JSON response if the request was successful
   