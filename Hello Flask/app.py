from flask import Flask,request,render_template,redirect,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
#from forms import SenderForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data1.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)



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
