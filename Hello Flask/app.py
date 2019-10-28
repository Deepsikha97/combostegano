from flask import Flask,request,render_template,redirect,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from encrypt import encrypt,decrypt
import os
from stegano import encode_image
from werkzeug.utils import secure_filename
from flask import send_file
from datetime import datetime
from zipfile import ZipFile
#from forms import SenderForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data1.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT,"temp\\")
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png','jpg'])

db = SQLAlchemy(app)

#os.urandom(n)
salt = b'/\xcd\xfe\xed\x95MP\xf4\xc1\xd4\xf2\x8b\x80#s)\xf3\xcb}\x08\x16\xe0\xcb\xb9M\x91$\x9fy\xcd\xde\x15\x1c]\xd9\xcaB5 \x14:T4M`\xba\x94L\x82u<[X\xe7nj\x01\x1edM\x87\x19\xd9\x18'
nonce = b'\xc5\xaeK\xda\xaa\xa8-v\xdaV\xd5O'

@app.before_first_request
def create_table():
    db.create_all()

class Book(db.Model):
    name = db.Column(db.String(80), nullable=False, primary_key=True)
    # key = db.Column(db.String(80), unique=True, nullable=False)
    # message = db.Column(db.String(80), unique=True, nullable=False)
    data=db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/sender", methods=["GET", "POST"])
def sender():
    if request.method == 'POST':
        print(request.form)
        file=request.files['file']
        # saving file name
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        #return(file.filename)
        # encrypting msg
        cipher = encrypt(request.form.get("message"),request.form.get("key"),salt,nonce)

        print("cipher text :" + str(cipher))
        # decrypted = decrypt(cipher,request.form.get("key"),salt,nonce)
        # print("decrypted string:" + str(decrypted))
        # stegano image
        path_name=UPLOAD_FOLDER+file.filename
        filepath=encode_image(request.form.get("name"),str(cipher),APP_ROOT,path_name)
        print("filepath:" + str(filepath))
        # putting data into databse
        # book = Book(name=request.form.get("name"),data=file.read())
        # filename=user_name.split()[0]+"_"+datetime.now().strftime("%d_%m_%y-%H:%M:%S")+".png"
        username=request.form.get("name").split()[0]+"-"+datetime.now().strftime("%d_%m_%y-%H:%M:%S")
        book = Book(name=username,data=filepath)
        db.session.add(book)
        db.session.commit()
        return(file.filename)
    else:
        return render_template("sender.html")


# @app.route("/receiver", methods=["GET", "POST"])
# def receiver():
#     file_data=Book.query.filter_by(name='kinjal das').first()
#     return send_file(BytesIO(file_data.data),attachment_filename='test.jpg',as_attachment=True)


@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    if request.method == 'POST':
        username=request.form.get("name").split()[0]
        print(username)
        file_data=Book.query.all()
        zipObj = ZipFile(username + '_download.zip', 'w')
        for data in file_data:
            name=data.name.split("-")[0]
            if(name==username):
                dataf=data.data
                print(dataf)
                # return send_file(dataf,as_attachment=True)
                zipObj.write(dataf)
        zipObj.close()
        return send_file(username + '_download.zip',as_attachment=True)
        # return send_file(BytesIO(file_data.data),attachment_filename='test.jpg',as_attachment=True)
        # return send_file(data.data,as_attachment=True)
    else:
        return render_template("receiver.html")





if __name__ == '__main__':
    # from db import db # DEBUG: db.init_app(app)
    # db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
