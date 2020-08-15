# library flask
from flask import Flask, request

# library untk restful api
from flask_restful import Resource, Api

# library untuk mengaktifkan komunikasi rest api
from flask_cors import CORS

# library ORM database
from flask_sqlalchemy import SQLAlchemy

# library untuk mempermudah query database ke bentuk json
# from flask_marshmallow import Marshmallow

# untuk keperluan manipuasi operating system
import os

# inisiasi object-object dari library yang sudah diimport tadi
app = Flask(__name__)
api = Api(app)
CORS(app)
db = SQLAlchemy(app)
marshal = Marshmallow(app)

# mengatur file database sqlite nya
# buat database dengan nama 'db.sqlite'
# lalu simpan di dalam folder project sebagai root
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# membuat model databasenya
class DatabaseModel(db.Model):
    judul = db.Column(db.String(20))
    id = db.Column(db.Integer, primary_key=True)
    konten = db.Column(db.TEXT)

    # panggil fungsi ini setiap kali menambahkan data/record baru
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


# methode ini untuk membuat/mengenerate database sqlite yang baru
# jika ingin hapus database, tinggal delete aja file 'db.sqlite'-nya
# lalu jalankan ulang file flask nya
db.create_all()

#
# ini adalah class untuk menginisiasli marshamllow nya
# jika versi flask-marshmallow > 0.12,
# Maka gunakan marshal.SQLAlchemyAutoSchema
# class DatabaseModelSchema(marshal.SQLAlchemyAutoSchema):
#     class Meta:
#         model = DatabaseModel
# informasiSchema = DatabaseModelSchema(many=True)
#
# contoh :
# query = DatabaseModel.query.all()
# output = informasiSchema.dump(query)
# return output, 200
#


# buat class untuk objek restful - nya,
# namanya bebas
class ResourcePertama(Resource):

    # untuk lihat semua datanya
    def get(self):
        # query databasenya dulu
        query = DatabaseModel.query.all()
        # karena output dari fungsi get request ini harus dalam
        # bentuk dictionary python, maka kita buat dengan
        # menggunakan teknik list comprehension python
        # jika belum mengerti, cari di google apa itu list comprehension

        # teknik looping dengan list comprehension
        output = [
            {"id": data.id, "judul": data.judul, "konten": data.konten}
            for data in query
        ]
        return output, 200

    # untuk post sebuah data
    def post(self):
        # inisiasi object databasenya dengan nama model
        model = DatabaseModel()
        judul = request.json["judul"]
        konten = request.json["konten"]
        model.judul = judul
        model.konten = konten
        model.save()  # fungsi untuk menyimpan record ke db
        return {"status": "berasil dikirim"}, 200

    # untuk menghapus semua data di dalam databasenya
    def delete(self):
        # query semua datanya
        # lalu ambil satu per satu hasil querynya
        # setiap data dimasukan ke dalam fungsi db.session.delete
        query = DatabaseModel.query.all()
        for data in query:
            db.session.delete(data)
            db.session.commit()
        return {"status": "berhasil dihapus"}, 200


# class untuk mengedit data
class ResourcePertamaById(Resource):

    # edit data berdasarkan id data/recordnya
    def put(self, id):
        # query dulu data yang mana yg mau diambil berdasarkan id-nya
        query = DatabaseModel.query.filter_by(id=id).first()
        # masukan informasi baru pada datanya
        judul = request.json["judul"]
        konten = request.json["konten"]
        query.judul = judul
        query.konten = konten
        query.save()  # untuk save kembali data yang sudah dihapus

        # 'f' itu adalah string formatting. Kalau tidak mengerti,
        # silahkan cari di google
        return {"message": f"data dengan id {id} berhasil diedit"}, 200


# memanggil methode api untuk mengaktifkan teknik routing-nya
api.add_resource(ResourcePertama, "/coba", methods=["GET", "POST", "DELETE"])
api.add_resource(ResourcePertamaById, "/coba/<id>", methods=["PUT"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
