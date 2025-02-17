from flask import request, jsonify
from extensions import db
from models.site_user import SiteUser
from ..schemas.user_schema import UserSchema
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required, get_jwt_identity,verify_jwt_in_request,get_jwt
import re


revoked_tokens = set()


class UserResource:
    @staticmethod
    def create_user():
     data = request.get_json()
     required_fields = ['username', 'email_address', 'password']
     for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
         
     phone_number = data.get('phone_number', None)
     if phone_number and not re.fullmatch(r'\d{10}', phone_number):
        return jsonify({'error': 'Phone number must be exactly 10 digits'}), 400

     existing_user = SiteUser.query.filter_by(email_address=data.get('email_address')).first()
     if existing_user:
        return jsonify({'error': 'Email already exists'}), 400
     hashed_password = generate_password_hash(data['password'])
     new_user = SiteUser(
        username=data['username'],
        email_address=data['email_address'],
        phone_number=phone_number,
        password=hashed_password
     )

     try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully!', 'user_id': new_user.id}), 201
     except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
     
    
    @staticmethod
    def login_user():
      data = request.get_json()
      required_fields = ['email_address', 'password']
    
      for field in required_fields:
         if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

      email_address = data['email_address']
      password = data['password']
      
      user = SiteUser.query.filter_by(email_address=email_address).first()
      # print(user.id)
      if not user:
         return jsonify({'error': 'User not found'}), 404

      if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 401

      ADMIN_EMAILS = {"kishanchandravadiya946@gmail.com"}
       
      role = "admin" if email_address in ADMIN_EMAILS else "user"
      
      access_token = create_access_token(
        identity={"user_id": user.id, "role": role},
        expires_delta=timedelta(minutes=10)
      )
      refresh_token = create_refresh_token(identity={"user_id": user.id, "role": role})

      user.access_token = access_token
      user.refresh_token = refresh_token

      try:
           db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
      
      return jsonify({
        'message': 'Login successful',
        'user_id':user.id,
        'access_token': access_token,
        'refresh_token': refresh_token
      }), 200
   
    @staticmethod
    def get_users():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
               return jsonify({'error': 'Unauthorized access'}), 403  
        users = SiteUser.query.all()
        userschema=UserSchema(many=True)
        return userschema.jsonify(users), 200
     
    def get_profile():
     try:
        current_user = get_jwt_identity()
        user = SiteUser.query.get(current_user['user_id'])

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "email_address": user.email_address,
            "phone_number": user.phone_number,
            "role": current_user["role"]
        }), 200

     except Exception as e:
        return jsonify({"error": str(e)}), 500
   
    def logout_user():       
       jti = get_jwt()["jti"]  
       revoked_tokens.add(jti)  
       print("B",revoked_tokens)
       user = SiteUser.query.get(get_jwt_identity()['user_id'])
       if user:
        user.access_token = None
        user.refresh_token = None
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'Logout successful'}), 200
   
   
 
