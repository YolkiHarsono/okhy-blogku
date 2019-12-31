from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from blog_ku import db, login_manager, app
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Admin(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20),nullable=False)
	password = db.Column(db.String(60), nullable=False)	

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='penulis', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	konten = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.tgl_post}', '{self.konten}')"

class Matakuliah(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	matakuliah = db.Column(db.String(20), nullable=False)
	sks = db.Column(db.Integer, nullable=False)
	keterangan = db.Column(db.Text, nullable=False)
	mk = db.relationship('Jadwal', backref='Matakuliah', lazy=True)

	def __repr__(self):
		return f"Matakuliah('{self.matakuliah}', '{self.sks}')"

class Dosen(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama = db.Column(db.String(30), nullable=False)
	nidn = db.Column(db.Integer, nullable=False)
	no_telpon = db.Column(db.Integer, nullable=False)
	alamat = db.Column(db.String(100), nullable=False)
	dosens = db.relationship('Jadwal', backref='Dosen', lazy=True)

	def __repr__(self):
		return f"Dosen('{self.nama}', '{self.nidn}')"

class Jadwal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	hari = db.Column(db.DateTime, nullable=False)
	jam = db.Column(db.Time, nullable=False)
	mk_id = db.Column(db.Integer, db.ForeignKey('matakuliah.id'))
	dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'))

	def __repr__(self):
		return f"Jadwal('{self.hari}', '{self.jam}')"

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Matakuliah, db.session))
admin.add_view(ModelView(Dosen, db.session))
admin.add_view(ModelView(Jadwal, db.session))