import json
from passlib.hash import pbkdf2_sha256 as sha256
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import json_util, ObjectId
from bson import ObjectId
from twilio.rest import Client
from run import mongo
from run import jsonify
import string
from datetime import datetime
class AdvertModel():

	@staticmethod
	def GetAdvert(id_advert):
		action=mongo.db.advert.find_one(ObjectId(id_advert))
		data=AdvertModel.jsonDumps(action)
		if data is None:
			return {"data":"null"}
		else:	
			get_id=(data['_id'])
			id_advert=(get_id['$oid'])
			del data["_id"]
			return jsonify({"data":data})

	@staticmethod
	def getAdverts():
		record=mongo.db.advert
		cursor=record.find()
		output = []
		for doc in cursor:
			data=AdvertModel.jsonDumps(doc)
			output.append(data)
		return ({"succes":True,"data":output})
	
	@staticmethod
	def getCountAdvert():
		record=mongo.db.advert
		cursor= record.aggregate([{"$group":{"_id":"$kategori", "count":{"$sum":1}}}])
		output = []
		for doc in cursor:
			data=AdvertModel.jsonDumps(doc)
			output.append(data)
		return ({"succes":True,"data":output})
	
	@staticmethod
	def SearchAdvert(kategori, provinsi, kab, cari):
		record=mongo.db.advert
		search = []
		if provinsi == "" and kab == "" and cari == "" and kategori == "":
			cursor= record.find()
			output = []
			for doc in cursor:
				data=AdvertModel.jsonDumps(doc)
				output.append(data)
			return ({"succes":True,"data":output})
		else:
			if kategori:
				search.append({"kategori":kategori})
			if provinsi:
				search.append({"provinsi":provinsi})
			if kab:
				search.append({"kab":kab})
			if cari:
				search.append({ "$text": { "$search":cari } })

			#cursor=record.find({"$and":[{"provinsi":provinsi},{"kab":kab}, { "$text": { "$search": "rumah" } }]})	
			cursor=record.find({"$and":search}).sort([("number", 1), ("date", -1)])
			output = []
			for doc in cursor:
				data=AdvertModel.jsonDumps(doc)
				output.append(data)
			return ({"succes":True,"data":output})		

	@staticmethod		
	def jsonDumps(get_data):
		return json.loads(json_util.dumps(get_data))

	@staticmethod
	def InsertAdvert(title, keterangan, luas_bangunan,luas_tanah, harga, kategori,
		filenames, sertifikasi, nego, tersedia, provinsi, kab, id_user ):
		today = str(datetime.today())
		
		action=mongo.db.advert.insert({"title":title,"keterangan":keterangan,
			"luas":{"luas_tanah":luas_tanah,"luas_bangunan":luas_bangunan},
			"harga":harga,"kategori":kategori,"foto":filenames, "sertifikasi":sertifikasi,
			"nego":nego, "tersedia":tersedia, "provinsi":provinsi, "kab":kab, "id_user":id_user,
			"date":today
			})
		if(action):
			response=jsonify({"succes":True, "messege":"succes insert data"})
			response.headers.add('Access-Control-Allow-Origin', '*')
			response.headers.add('Access-Control-Allow-Headers', '*')
			return response
		else:
			return ({"succes":False, "messege":"Failed insert data"})

	@staticmethod
	def UpdateAdvert(title, keterangan, luas_bangunan,luas_tanah, harga, kategori,filenames, sertifikasi, nego, tersedia  ):
		action=mongo.db.advert.insert({"title":title,"keterangan":keterangan,
			"luas":{"luas_tanah":luas_tanah,"luas_bangunan":luas_bangunan},
			"harga":harga,"kategori":kategori,"foto":filenames, "sertifikasi":sertifikasi,
			"nego":nego, "tersedia":tersedia
			})
		if(action):
			response=jsonify({"succes":True, "messege":"succes insert data"})
			response.headers.add('Access-Control-Allow-Origin', '*')
			response.headers.add('Access-Control-Allow-Headers', '*')
			return response
		else:
			return ({"succes":False, "messege":"Failed insert data"})

	@staticmethod
	def deleteadvert(id_advert):
		action=mongo.db.advert.delete_one({"_id":ObjectId(id_advert)})
		
		if(action.deleted_count > 0):
			return ({"success": True, "messege":"Berhasil Menghapus Iklan"})
		else:
			return ({"succes":False,"messege":"Gagal Menghapus Iklan, Mungkin Pesan sudah terhapus atau tidak ada"})	



	