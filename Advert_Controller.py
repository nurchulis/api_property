import os
from flask_restful import Resource, reqparse
from flask import json, request
from run import app
from run import jsonify
from werkzeug import secure_filename
import random
import string
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from Advert_Models import AdvertModel

file = reqparse.RequestParser()
data_property = reqparse.RequestParser()


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s

file.add_argument('image', location=['headers', 'values'])
data_property.add_argument('title', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('keterangan', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('luas_bangunan', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('luas_tanah', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('kategori', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('harga', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('sertifikasi', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('nego', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('tersedia', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('provinsi', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('kab', help= 'This field cannot be blank', required = True, type=non_empty_string)
data_property.add_argument('id_user', help= 'This field cannot be blank', required = True, type=non_empty_string)


def randomString():
	for x in range(100):
		return random.randint(1,1100000)

def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def randomFile(stringLength=25):
    """Generate a random string of fixed length """
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,stringLength))
class Getadvert(Resource):
	def get(self,id_advert=None):
		if not id_advert:
			return 404
		return AdvertModel.GetAdvert(id_advert)
class countAdvert(Resource):
	def get(self):
		return AdvertModel.getCountAdvert()

class alladvert(Resource):
	def get(self):
		return AdvertModel.getAdverts()

class searchAdvert(Resource):
	def get(self):
		args = request.args
		provinsi=(args['provinsi'])
		kab=(args['kab'])
		cari=(args['cari'])
		kategori=(args['kategori'])
		return AdvertModel.SearchAdvert(kategori,provinsi,kab,cari)
		

class PostAdvert(Resource):
    def post(self):
        # Get the name of the uplo
        uploaded_files = request.files.getlist("image")
        data =data_property.parse_args()
        title = data['title']
        keterangan =data['keterangan']
        luas_bangunan= data['luas_bangunan']
        luas_tanah= data['luas_tanah']
        kategori= data['kategori']
        harga = data['harga']
        tersedia = data['tersedia']
        nego = data['nego']
        sertifikasi = data['sertifikasi']
        provinsi = data['provinsi']
        kab = data['kab']
        id_user = data['id_user']
        filenames = []
        uniqe_name_data=randomString()
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)

                uniqe_name=randomFile()+filename

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqe_name))
                filenames.append(uniqe_name)


       	return AdvertModel.InsertAdvert(title, keterangan, luas_bangunan,luas_tanah, 
       		harga, kategori,filenames, sertifikasi, nego, tersedia, provinsi, kab, id_user)


class UpdateAdvert(Resource):
    def put(self):
        uploaded_files = request.files.getlist("image")
    
        data =data_property.parse_args()
        title = data['title']
        keterangan =data['keterangan']
        luas_bangunan= data['luas_bangunan']
        luas_tanah= data['luas_tanah']
        kategori= data['kategori']
        harga = data['harga']
        tersedia = data['tersedia']
        nego = data['nego']
        sertifikasi = data['sertifikasi']
        filenames = []
        uniqe_name_data=randomString()
        if(uploaded_files):
	        for file in uploaded_files:
	            # Check if the file is one of the allowed types/extensions
	            if file and allowed_file(file.filename):
	                # Make the filename safe, remove unsupported chars
	                filename = secure_filename(file.filename)

	                uniqe_name=randomFile()+filename

	                file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqe_name))
	                filenames.append(uniqe_name)
	            else:
	            	return('gagal')

		else:	           
			return ('tidak ada')
        return AdvertModel.UpdateAdvert(title, keterangan, luas_bangunan,luas_tanah, harga, kategori,filenames, sertifikasi, nego, tersedia)

class Deleteadvert(Resource):
	def get(self, id_advert= None):
		return AdvertModel.deleteadvert(id_advert)

