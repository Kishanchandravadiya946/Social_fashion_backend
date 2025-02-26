from flask import request, jsonify
from extensions import db
from models.site_user import SiteUser
from models.shopping_cart import ShoppingCart
from models.address import Address
from models.user_address import UserAddress
from models.country import Country
from ..schemas.user_schema import UserSchema
from ..schemas.country_schema import CountrySchema
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
        shopping_cart = ShoppingCart(user_id=new_user.id)
        db.session.add(shopping_cart)
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
      #   print(user)
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
     
    def profile_update():
      try:
        current_user = get_jwt_identity()
        user = SiteUser.query.get(current_user['user_id'])
        print(current_user['user_id'])
        if not user:
           return {'error':"user doesn't exists "},400
        
        data=request.get_json()
        if not data.get("username"):
           return {'error':"username required"},400
         
        if not data.get("phone_number"):
           return {'error':"phone_number required"},400
        user.username=data.get("username")
        user.phone_number=data.get("phone_number")
      #   print(user.email_address)

        db.session.commit()      
        return{"massage":"update successfull"},200

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
    
    def address_create():  
        try:
         current_user = get_jwt_identity()
         user = SiteUser.query.get(current_user['user_id'])
         # print("m")
         data = request.get_json()
         print(data.get("unit_number"))
         print(data.get("street_number"))
         # print("x")
         required_fields = ["unit_number", "street_number", "address_line1", "city", "region", "postal_code", "country_id", "user_id"]
         print("a")
         missing_fields = [field for field in required_fields if not data.get(field)]
         if not missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
         print("h")
         new_address = Address(
               unit_number=data.get("unit_number"),
               street_number=data.get("street_number"),
               address_line1=data.get("address_line1"),
               address_line2=data.get("address_line2"),
               city=data.get("city"),
               region=data.get("region"),
               postal_code=data.get("postal_code"),
               country_id=data.get("country_id")
         )
         # print("o")
         print(new_address.unit_number)
         db.session.add(new_address)
         db.session.commit()
         user_address = UserAddress(
               user_id=user.id,  # Ensure user_id is passed in the request
               address_id=new_address.id,  # Use the ID of the newly created address
               is_default=False  # New addresses are not default by default
         )
         db.session.add(user_address)
         db.session.commit()
         address_list = {
            "id": new_address.id,
            "unit_number": new_address.unit_number,
            "street_number": new_address.street_number,
            "address_line1": new_address.address_line1,
            "address_line2": new_address.address_line2,
            "city": new_address.city,
            "region": new_address.region,
            "postal_code": new_address.postal_code,
            "country_name": new_address.country_id
         }
         return jsonify({"message": "Address added successfully","new_user":address_list}), 201
         
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}),500
 
    def get_countries():
      try:
         countries=Country.query.all()
         countryschema=CountrySchema(many=True)
         return countryschema.jsonify(countries), 200
      except Exception as e:
         return {"error":e},500

    def address_fetch():
      try:
         # print("x")
         current_user = get_jwt_identity()
         user = SiteUser.query.get(current_user['user_id'])
         if not user:
            return jsonify({"error": "User not found"}), 404
         # print("a")
         user_addresses = UserAddress.query.filter_by(user_id=user.id).all()
         address_ids = [ua.address_id for ua in user_addresses]
         default_add = next((ua.address_id for ua in user_addresses if ua.is_default), None)
         # print(default_add);
         # print("b")
         addresses = db.session.query(
            Address.id,
            Address.unit_number,
            Address.street_number,
            Address.address_line1,
            Address.address_line2,
            Address.city,
            Address.region,
            Address.postal_code,
            Country.country_name.label("country_name")  # Fetch country name instead of country_id
        ).join(Country, Address.country_id == Country.id).filter(Address.id.in_(address_ids)).all()
         # print("c")
        # Convert address objects to JSON format
         address_list = [{
            "id": addr.id,
            "unit_number": addr.unit_number,
            "street_number": addr.street_number,
            "address_line1": addr.address_line1,
            "address_line2": addr.address_line2,
            "city": addr.city,
            "region": addr.region,
            "postal_code": addr.postal_code,
            "country_name": addr.country_name
         } for addr in addresses]
         # print("d")
         return jsonify({"address_list": address_list, "is_default": default_add}), 200
      except Exception as e:
         print("hy i am error",e)
         return {"error":e},500
      
    def address_set(address_id):
      #  print("m")
       try:
         # print(address_id)
         current_user = get_jwt_identity()
         user = SiteUser.query.get(current_user['user_id'])
         # print(user)
         if not user:
            # print("hy")
            return jsonify({"error": "User not found"}), 404
         # print("A")  
         # Find the user's existing default address and unset it
         UserAddress.query.filter_by(user_id=user.id, is_default=True).update({"is_default": False})

        # Set the new default address
         new_default_address = UserAddress.query.filter_by(user_id=user.id, address_id=address_id).first()
         if not new_default_address:
            # print("ax")
            return jsonify({"error": "Address not found"}), 404

         new_default_address.is_default = True
         db.session.commit()
         return jsonify({"message": "Default address updated successfully"}), 200

       except Exception as e:
          return {'error':e},500 
       
    def address_delete(address_id):
       try: 
         current_user = get_jwt_identity()
         user = SiteUser.query.get(current_user['user_id'])
         if not user:  
            return jsonify({"error": "User not found"}), 404
         
         address = Address.query.get(address_id)
         if not address:
            return jsonify({"error": "Address not found"}), 404

         UserAddress.query.filter_by(user_id=user.id, address_id=address_id).delete()
         db.session.delete(address)
         db.session.commit()

         return jsonify({"message": "Address deleted successfully"}), 200

       except Exception as e:
          return {'error':e},500 
           
