from flask import Flask, request, jsonify

import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# Initialize Firebase
# firebase_admin.initialize_app(cred)

firebase_admin.initialize_app()
db = firestore.client()

@app.route('/user/<uid>', methods=['GET'])
def get_user_data(uid):
    try:
        user_ref = db.collection('users').document(uid)
        doc = user_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/<uid>', methods=['POST'])
def store_user_data(uid):
    try:
        data = request.json
        user_ref = db.collection('users').document(uid)
        user_ref.set(data) # type: ignore
        return jsonify({"message": "Data stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/check/<uid>', methods=['GET'])
def check_user(uid):
    try:
        auth.get_user(uid)
        return jsonify({"exists": True}), 200
    except auth.UserNotFoundError:
        return jsonify({"exists": False}), 200

@app.route('/user/create', methods=['POST'])
def create_user():
    try:
        data = request.json
        user_record = auth.create_user(
            uid=data['uid'], # type: ignore
            email=data['email'], # type: ignore
            display_name=data['display_name'] # type: ignore
        )
        return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

