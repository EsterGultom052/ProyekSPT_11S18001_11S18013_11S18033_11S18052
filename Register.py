from flask import Flask, flash, redirect, render_template, request, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename 
from flask_wtf import FlaskForm
from wtforms import SelectField
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.secret_key = "secret key"

class Bursar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String)
    total = db.Column(db.Integer)
    spp = db.Column(db.Integer)
    asrama = db.Column(db.Integer)
    makan = db.Column(db.Integer)
    admin = db.Column(db.Integer)
    status = db.Column(db.String(10))

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10))
    nama = db.Column(db.String(100))

class BuktiPembayaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    period = db.Column(db.String(20))

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    st = db.Column(db.String(10))

class Form(FlaskForm):
    status = SelectField('status', choices=[])

@app.route('/')
def index():
    form = Form()
    form.status.choices = [(status.st) for status in Status.query.all()]
    newFiles = Bursar.query.order_by(Bursar.id.desc()).all()
    item1 = Bursar.query.order_by(Bursar.id.desc()).first()
    return render_template('Register.html', newFiles=newFiles, item1=item1, form=form)

@app.route('/listMahasiswa', methods=['GET', 'POST'])
def listMahasiswa():
    if request.method == 'POST':
        return redirect(url_for('index'))

    showMahasiswa = Mahasiswa(id=request.form.get("id"), nim=request.form.get("nim"), nama=request.form.get("nama"))
    showMahasiswas = Mahasiswa.query.all()   
    return render_template('listMahasiswa.html', showMahasiswas=showMahasiswas)

@app.route('/verifikasi', methods=['GET'])
def verifikasi():  
    buktis = BuktiPembayaran.query.order_by(BuktiPembayaran.id.desc()).all()
    newFiles = Bursar.query.order_by(Bursar.id.desc()).all()
    return render_template('verifikasi.html', buktis=buktis, newFiles=newFiles)
    
@app.route("/uploadBursar", methods=['POST'])
def uploadBursar():
    # file = request.files['inputFile']
    form = Form()
    form.status.choices = [(status.st) for status in Status.query.all()]
    newFile = Bursar(id=request.form.get("id"), period=request.form.get("period"), total=request.form.get("total"), spp=request.form.get("spp"), asrama=request.form.get("asrama"), makan=request.form.get("makan"), admin=request.form.get("admin"), status=request.form.get("status"))
    db.session.add(newFile)
    db.session.commit()
    newFiles = Bursar.query.order_by(Bursar.id.desc()).all()  
    item1 = Bursar.query.order_by(Bursar.id.desc()).first()
    return render_template('uploadbursar.html', newFiles=newFiles, item1=item1, form=form)

@app.route('/downloadbukti')
def downloadbukti():
    file_data = BuktiPembayaran.query.order_by(BuktiPembayaran.id.desc()).first()
    return send_file(BytesIO(file_data.data), attachment_filename="bukti_pembayaran.jpg", as_attachment=False)

@app.route('/editstatus', methods=['GET'])
def editstatus():  
    buktis = BuktiPembayaran.query.order_by(BuktiPembayaran.id.desc()).all()
    newFiles = Bursar.query.order_by(Bursar.id.desc()).all()
    form = Form()
    form.status.choices = [(status.st) for status in Status.query.all()]
    return render_template('editstatus.html', buktis=buktis, newFiles=newFiles, form=form)

@app.route("/update", methods=["POST"])
def update():
    form = Form()
    form.status.choices = [(status.st) for status in Status.query.all()]
    newtitle = request.form.get("status")
    oldtitle = request.form.get("oldtitle")
    edit = Bursar.query.filter_by(status=oldtitle).first()
    edit.status = newtitle
    db.session.commit()
    return redirect('verifikasi')

if __name__ == '__main__':
    app.run(debug=True)