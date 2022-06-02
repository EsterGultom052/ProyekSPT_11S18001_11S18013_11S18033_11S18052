from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.secret_key = "secret key"

class BuktiPembayaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    period = db.Column(db.String(20))

class Bursar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String)
    total = db.Column(db.Integer)
    spp = db.Column(db.Integer)
    asrama = db.Column(db.Integer)
    makan = db.Column(db.Integer)
    admin = db.Column(db.Integer)
    status = db.Column(db.String(10))

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    newFiles = Bursar.query.order_by(Bursar.id.desc()).all()
    item1 = Bursar.query.order_by(Bursar.id.desc()).first()
    return render_template('Login.html', newFiles=newFiles, item1=item1)

@app.route('/uploadView', methods=['GET', 'POST'])
def uploadView():
    if request.method == 'POST':
        return redirect(url_for('index'))
        
    return render_template('uploadView.html')
    
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    
    if file and allowed_file(file.filename):
        newFile = BuktiPembayaran(name=file.filename, period=request.form.get("period"), data=file.read())
        db.session.add(newFile)
        db.session.commit()
        filename = secure_filename(file.filename)
        flash('File successfully uploaded')
        return redirect('/uploadView')
    else:
        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        return redirect('/uploadView')

if __name__ == '__main__':
    app.run(debug=True)