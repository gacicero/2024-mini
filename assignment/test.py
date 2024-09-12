import random
import time
import json
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser
import jwt
import requests


API_BASE_URL = "https://flask-api-560047854310.us-east1.run.app"

# Google OAuth 2.0 flow for Gmail login
def authenticate_user():
    # Use run_local_server for handling the redirect_uri correctly
    webbrowser.register('manual', None, webbrowser.GenericBrowser('true'))  
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=["openid","https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"])

    creds = flow.run_local_server(port=8000, open_browser=True)  # Disable automatic browser opening

    # Decode the JWT (ID token) to access the user information
    decoded_token = jwt.decode(creds.id_token, options={"verify_signature": False}) # type: ignore

    # Return the Firebase UID (sub) from the decoded ID token
    return decoded_token['sub'], decoded_token.get('email'), decoded_token.get('name')

def store_data(uid, data):
    response = requests.post(f"{API_BASE_URL}/user/{uid}", json=data)
    response.raise_for_status()



def fetch_user_data(uid):
    response = requests.get(f"{API_BASE_URL}/user/{uid}")
    if response.status_code == 200:
        return response.json()
    return None

def check_user_in_firebase(uid):
    response = requests.get(f"{API_BASE_URL}/user/check/{uid}")
    
    # Print the response content for debugging
    # print(f"Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")
    
    # Handle unexpected responses
    if response.status_code != 200:
        print("Error: Unexpected status code or response")
        return False
    
    try:
        return response.json().get('exists', False)
    except ValueError:
        print("Error: Could not decode JSON response")
        return False
# def check_user_in_firebase(uid):
#     response = requests.get(f"{API_BASE_URL}/user/check/{uid}")
#     return response.json().get('exists', False)



def create_user_in_firebase(uid, email, user_name):
    data = {
        'uid': uid,
        'email': email,
        'display_name': user_name
    }
    response = requests.post(f"{API_BASE_URL}/user/create", json=data)
    response.raise_for_status()


def main():
    print('Welcome. Please authenticate yourself to view data and/or store new data.')
    uid, email, user_name = authenticate_user()
    print('\n')
    print(f"Welcome, {user_name}!")
    print('\n')

    if not check_user_in_firebase(uid):
        create_user_in_firebase(uid, email, user_name)

    while True:
        print('Would you like to view data or store new data?')
        print('1. View data')
        print('2. Store new data')
        print('3. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            print('Viewing data...')
            user_data = fetch_user_data(uid)
        
            if user_data:
                print(f"User Data for {user_name}: ")
                print(f"Average response time: {user_data['average_response_time']} ms")
                print(f"Minimum response time: {user_data['minimum_response_time']} ms")
                print(f"Maximum response time: {user_data['maximum_response_time']} ms")
                print(f"Score: {user_data['score'] * 100:.2f}%")
            else:
                print(f"No data found for {user_name}")

        elif choice == '2':
            print('Storing data...')
            
            t_good = []
            x = int(random.randint(1, 10))

            for i in range(x):
                y = random.uniform(0.5, 5)
                t_good.append(y)

            avg_time = sum(t_good) / len(t_good)
            min_time = min(t_good)
            max_time = max(t_good)
            score = (10 - x) / 10

            # Display results
            print(f"Average response time: {avg_time} ms")
            print(f"Minimum response time: {min_time} ms")
            print(f"Maximum response time: {max_time} ms")
            print(f"Score: {score * 100:.2f}%")

            # Store results in a dictionary
            data = {
                "average_response_time": avg_time,
                "minimum_response_time": min_time,
                "maximum_response_time": max_time,
                "score": score
            }

            store_data(uid, data)
        elif choice == '3':
            print('Exiting...\nThank you!')
            break
        else:
            print('Invalid choice. Please try again.')
        
    return



if __name__ == "__main__":
    main()
    
