import os
from flask_restful import Resource, reqparse
from flask import json, request
from run import app
from run import jsonify
import string
from flask_jwt_extended import (create_access_token, create_refresh_token, JWTManager, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from User_Models import UserModel

auth = reqparse.RequestParser()
register = reqparse.RequestParser()
#Register
register.add_argument('username', help = 'This field cannot be blank', required = True)
register.add_argument('password', help = 'This field cannot be blank', required = True)
register.add_argument('email', help= 'This field cannot be blank', required = True)
#Auth_login
auth.add_argument('email', help= 'This field cannot be blank', required = True)
auth.add_argument('password', help= 'This field cannot be blank', required = True)
##jwt = JWTManager(app)

class UserRegistration(Resource):

	def post(self):
		data = register.parse_args()
		cek_username = UserModel.find_user_by_username_count(data.username)
		cek_email = UserModel.find_user_by_username_count(data.username)
		ambil=json.dumps(data)
		if (cek_username>=1):
			return jsonify({
				"success":False,
				"messege":"username already exist"})
		elif (cek_email>=1):
			return jsonify({
				"success":False,
				"messege":"email already exist"})
		else:
			action = UserModel.InsertUser({"username":data.username, 
				"password":data.password, 
				"email":data.email,
				"verified":False
				}) 
			get_data= UserModel.find_user_by_email(data.email)
			data_user = UserModel.jsonDumps(get_data)
			get_id=(data_user['_id'])
			id_user=(get_id['$oid'])
			return jsonify({
				"success":True,
				"messege":"success register",
				"data":{
				"id":id_user,
				"username":data.username,
				"email":data.email
				}
				})	

class usersAuth(Resource):
    def post(self):
        data = auth.parse_args()
        current_user = UserModel.find_user_by_email(data.email)
        data_user = UserModel.jsonDumps(current_user)
        get_id=(data_user['_id'])
        id_user=(get_id['$oid'])
        if not current_user:
            return {
            "success":False,
            "message": "email not Found"}
        
        if UserModel.verify_hash(data.password, data_user["password"]):
            access_token = create_access_token(identity = id_user)
            return {
            	"success":True,
            	"data":{
            	"username":data_user["username"],
            	"email":data_user["email"]
            	},
            	"access_token":access_token,
                "message": "Logged in as"
                }
        else:
            return {"message": "Wrong credentials"}

class GetUser(Resource):
	@jwt_required
	def get(self):
		id_user = get_jwt_identity()
		return UserModel.Getuser(id_user)


class OTPverification(Resource):
	@jwt_required   
	def post(self):
		id_user = get_jwt_identity()
		get_number = request.form['number']  
		return UserModel.OTPuser(get_number,id_user)

class ActivationUser(Resource):
	@jwt_required   
	def post(self):
		id_user = get_jwt_identity()
		requests = json.loads(request.data)
		code_activation = requests['code_activation']  
		return UserModel.activation_user(id_user,code_activation)

