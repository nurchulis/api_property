from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_restful import Api
from flask import json
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_pymongo import PyMongo
import urllib 
from flask_cors import CORS, cross_origin
import datetime
app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
##app.config['PROPAGATE_EXCEPTIONS'] = True
app=Flask(__name__,template_folder='static')
api = Api(app)

app.config['MONGO_DBNAME'] = 'property'
app.config['MONGO_URI'] = 'mongodb://nurchulis:' + urllib.quote("linamaulana11") + '@cluster0-shard-00-00-9w1yt.mongodb.net:27017,cluster0-shard-00-01-9w1yt.mongodb.net:27017,cluster0-shard-00-02-9w1yt.mongodb.net:27017/property?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
mongo = PyMongo(app)

CORS(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
##app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(0.01)
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
import views, Advert_Controller, User_Controller
path_api ='/api/v1'


@app.route('/')
def main_world():
    return render_template('index.html')

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/list', methods=['GET'])
def get_all_stars():
  advert = mongo.db.advert
  output = []
  for s in advert.find():
    output.append({'name' : s['title'], 'distance' : s['harga']})
  return jsonify({'result' : output})

@app.route('/insert_advert', methods=['POST'])
def post_advert():
	 data =({"title":"Rumah Dijual","harga":20000000,"nego":"true","luas":{"luas_tana":2392},"sertifikasi":"true","fasilitas":["Kamar mandi","Kamar Tidur"],"kategori":"apartemen","tersedia":1,"foto":["insa.jpg"]})
	 action=mongo.db.advert.insert_one(data)

	 if(action):
	 	return ('berhasil')


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


#authentification auth
api.add_resource(User_Controller.UserRegistration, path_api+'/registration')
api.add_resource(User_Controller.usersAuth, path_api+'/auth')

#user
api.add_resource(User_Controller.OTPverification, path_api+'/OTP')
api.add_resource(User_Controller.ActivationUser, path_api+'/activation')
api.add_resource(User_Controller.GetUser, path_api+'/getuser')
#Edit Profile User

#advert
api.add_resource(Advert_Controller.PostAdvert, path_api+'/postadvert')
api.add_resource(Advert_Controller.Deleteadvert, path_api+'/deleteadvert/<string:id_advert>')
api.add_resource(Advert_Controller.Getadvert, path_api+'/getadvert/<string:id_advert>')
api.add_resource(Advert_Controller.alladvert, path_api+'/alladvert')
api.add_resource(Advert_Controller.searchAdvert, path_api+'/search')

#Fitur Tambahan
api.add_resource(Advert_Controller.countAdvert, path_api+'/countadvertpercategory')


if __name__ == '__main__':
     app.run(debug=True)
