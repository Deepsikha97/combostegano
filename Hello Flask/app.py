from flask import Flask,request,render_template,redirect,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from encrypt import encrypt,decrypt
import os
#from forms import SenderForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data1.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)

#os.urandom(n)
salt = b'/\xcd\xfe\xed\x95MP\xf4\xc1\xd4\xf2\x8b\x80#s)\xf3\xcb}\x08\x16\xe0\xcb\xb9M\x91$\x9fy\xcd\xde\x15\x1c]\xd9\xcaB5 \x14:T4M`\xba\x94L\x82u<[X\xe7nj\x01\x1edM\x87\x19\xd9\x18'
nonce = b'\xc5\xaeK\xda\xaa\xa8-v\xdaV\xd5O'

@app.before_first_request
def create_table():
    db.create_all()

class Book(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.String(80), unique=True, nullable=False)
    data=db.Column(db.LargeBinary)

    def __repr__(self):
        return "<Title: {}>".format(self.name)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/sender", methods=["GET", "POST"])
def sender():
    if request.method == 'POST':
        print(request.form)
        file=request.files['file']
        #return(file.filename)
        cipher = encrypt(request.form.get("message"),request.form.get("key"),salt,nonce)
        print("cipher text :" + str(cipher))
        decrypted = decrypt(cipher,request.form.get("key"),salt,nonce)
        print("decrypted string:" + str(decrypted))
        book = Book(name=request.form.get("name"),key=request.form.get("key"),
        message=request.form.get("message"),data=file.read())
        db.session.add(book)
        db.session.commit()
        return(file.filename)
    return render_template("sender.html")


@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    file_data=Book.query.filter_by(name='kinjal das').first()
    return send_file(BytesIO(file_data.data),attachment_filename='test.jpg',as_attachment=True)


if __name__ == '__main__':
    # from db import db # DEBUG: db.init_app(app)
    # db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
