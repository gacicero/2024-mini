from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import firebase_admin
import os
from firebase_admin import credentials, auth, firestore
import requests


app = Flask(__name__)

# Initialize Firebase
# firebase_admin.initialize_app(cred)

#  RATE LIMITING
limiter = Limiter(
    get_remote_address, 
    app=app,
    default_limits=["1000 per day"], 
)


firebase_admin.initialize_app()
db = firestore.client()



def verify_token(f):
    from functools import wraps
    def wrapper(*args, **kwargs):
        id_token = request.headers.get('Authorization')
        if not id_token:
            return jsonify({'error': 'Missing Authorization Header'}), 401
        try:
            # Remove 'Bearer ' prefix if present
            if id_token.startswith('Bearer '):
                id_token = id_token[len('Bearer '):]
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token # type: ignore
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return wraps(f)(wrapper)


@app.route('/user/data', methods=['GET', 'POST']) # type: ignore
@limiter.limit("200 per day")
@verify_token
def user_data():
    try:
        uid = request.user['uid'] # type: ignore
        user_ref = db.collection('users').document(uid)
        if request.method == 'GET':
            doc = user_ref.get()
            if doc.exists:
                return jsonify(doc.to_dict()), 200
            else:
                return jsonify({'error': 'No data found for user'}), 404
        elif request.method == 'POST':
            data = request.json
            user_ref.set(data) # type: ignore
            return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/user/register', methods=['POST'])
@limiter.limit("50 per day")
def register_user():
    try:
        data = request.json
        email = data['email'] # type: ignore
        password = data['password'] # type: ignore
        display_name = data.get('display_name', '') # type: ignore

        if not email.endswith('@gmail.com') and not email.endswith('edu'):
            return jsonify({'error': 'Please login with a valid email address.'}), 400

        # Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )

        return jsonify({'message': 'User registered successfully', 'uid': user.uid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data['email'] # type: ignore
        password = data['password'] # type: ignore

        # Sign in the user using Firebase Authentication
        # Note: Firebase Admin SDK doesn't support sign-in with email and password directly.
        # You'll need to use Firebase's REST API for authentication.


        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        load_dotenv('.env')
        api_key = os.getenv('Firebase_API_KEY')
        response = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}',
            json=payload
        )

        if response.status_code == 200:
            id_token = response.json()['idToken']
            return jsonify({'message': 'Login successful', 'idToken': id_token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

