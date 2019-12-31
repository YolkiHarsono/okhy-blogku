from flask import render_template, url_for, flash, redirect, request
from blog_ku import app, db, bcrypt
from blog_ku.forms import Registrasi_F, Login_F, Update_Account_F, Post_F, Admin_F
from blog_ku.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image


@app.route("/")  
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", title='Home', posts=posts)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title='Dashboard')

@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
    form = Registrasi_F()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun Anda berhasil ditambahkan!', 'success')
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    return render_template("registrasi.html", title="Registrasi", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login_F()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login gagal..!, periksa username dan password', 'danger')
            return redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def simpan_foto(form_foto):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_foto.filename)
    foto_fn = random_hex + f_ext
    foto_path = os.path.join(app.root_path, 'static/foto_profil', foto_fn)
    form_foto.save(foto_path)
    return foto_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = Update_Account_F()
    if form.validate_on_submit():
        # save foto profil
        if form.foto.data:
            file_foto = simpan_foto(form.foto.data)
            current_user.image_file = file_foto
        # simpan database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Akun berhasil di update', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='foto_profil/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = Post_F()
    if form.validate_on_submit():
        post = Post(title=form.title.data, konten=form.konten.data, penulis=current_user)
        db.session.add(post)
        db.session.commit()
        flash('post berhasil ditambahkan', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.penulis != current_user:
        abort(403)
    form = Post_F()
    if form.validate_on_submit():
        post.title = form.title.data
        post.konten = form.konten.data
        db.session.commit()
        flash('post berhasil di ubah', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.konten.data = post.konten
    return render_template('create_post.html', title="Update", form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.penulis != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post berhasil dihapus', 'success')
    return redirect(url_for('home'))

@app.route("/index", methods=['GET','POST'])
def index():
	form = Admin_F()
	if form.validate_on_submit():
		if form.username.data == 'nabila' and form.password.data == '4199':
			return redirect('index')
		else :
			flash('Login gagal..!, periksa username dan password','danger')
	return render_template("admin/index.html", title="index", form=form)
