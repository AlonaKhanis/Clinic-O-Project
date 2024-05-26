from pathlib import Path
import bcrypt
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required
from psycopg2.extras import RealDictCursor
from db import get_db, close_db
from flask_cors import CORS
from dotenv import load_dotenv

from models.users import User
from models.patient import Patient
from models.doctor import Doctor
from models.owner import Owner

from views.users import bp as users_bp
from views.appointments import bp as appointments_bp
from views.patient import bp as patient
from views.doctor import bp as doctors_bp



app = Flask(__name__)
app.config.from_prefixed_env()
FRONTEND_URL = app.config.get("FRONTEND_URL")
cors = CORS(app, origins=FRONTEND_URL, methods=["GET", "POST", "DELETE"])
jwt = JWTManager(app)
app.teardown_appcontext(close_db)
app.register_blueprint(users_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(patient)
app.register_blueprint(doctors_bp)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    cursor = db.cursor(cursor_factory=RealDictCursor)  

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (data["username"], data["password"]))
    user = cursor.fetchone()
    
    if user:
        access_token = create_access_token(identity=user["id"])
        return {"access_token": access_token} , 200 
    else:
       return {"error": "Invalid username or password"} , 401


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     db = get_db()
#     cursor = db.cursor(cursor_factory=RealDictCursor)  

#     cursor.execute("SELECT * FROM users WHERE username = %s", (data["username"],))
#     user = cursor.fetchone()
    
#     if user and bcrypt.checkpw(data["password"].encode('utf-8'), user["password"].encode('utf-8')):
#         access_token = create_access_token(identity=user["id"])
#         return {"access_token": access_token}, 200 
#     else:
#         return {"error": "Invalid username or password"}, 401


@app.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)

      
        cursor.execute("SELECT * FROM users WHERE id = %s", (current_user_id,))
        user_data = cursor.fetchone()
        

        if not user_data:
            return jsonify({'message': 'User not found'}), 404
        
        role = user_data['role']

        if role == 'patient':
            patient_info = Patient.get_patient(cursor, current_user_id)

            if patient_info:
                return jsonify(patient_info), 200
            
        elif role == 'doctor':
            doctor_info = Doctor.get_doctor(cursor, current_user_id)
            if doctor_info:
                return jsonify(doctor_info), 200
            
        elif role == 'owner':
            owner_info = Owner.get_owner(cursor, current_user_id)
            if owner_info:
                return jsonify(owner_info), 200
        else:
            return jsonify({'message': 'Invalid user role'}), 400

        return jsonify({'message': 'User details not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()




   