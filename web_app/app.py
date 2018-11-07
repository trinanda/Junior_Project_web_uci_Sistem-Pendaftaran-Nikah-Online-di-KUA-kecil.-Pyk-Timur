import os, sys
sys.path.append(os.getcwd() + '/web_app') #sesuai dengan mark directory as sources
from flask import Flask, render_template, request, session, url_for, redirect
import flask_admin
from flask_admin import Admin, helpers as admin_helpers
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password

import pdfkit
from models import db, Content, Role, User, DataCatin
from views import MyModelView, ContentView, dataCatinView
from form import RegisterFormView, LoginFormView
def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    url_index = 'http://127.0.0.1:9999/'

    bootstrap = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin = flask_admin.Admin(
        app,
        'Superuser',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )

    admin.add_view(ContentView(Content, db.session))
    admin.add_view(dataCatinView(DataCatin, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))


    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index_page.html')


    @app.route('/register', methods = ['GET', 'POST'])
    def register():
        form = RegisterFormView()
        try:
            if form.validate_on_submit():
                hashed_password = form.password.data
                new_user = User(name=form.name.data, email=form.email.data,
                                password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                return "<h1> Sukses mendaftar, Anda baru bisa login ketika akun sudah di aktivkan oleh " \
                       "admin. <br> kembali ke menu <a href=" + url_index + ">utama</a></h1>"
        except:
            return "<h2> Data yang di inputkan harus unique, sepertinya salah satu data yang Anda Masukan sudah terdaftar, " \
                   "Mohon ulangi input data dengan teliti...!!!  <br> <a href=" + url_index + "signup>Ulangi Input Data</a></h2>"

        return render_template('register.html', form=form)

    @app.route('/login')
    def login():
        form = LoginFormView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                session['email'] = request.form['email']
                user = User.query.filter_by(email=form.email.data).first()
                if verify_password(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
                else:
                    return '<h1>Invalid username or password</h1>'

        return render_template('login.html', form=form)
        return render_template('login.html')

    @app.route('/society')
    def society():
        return render_template('society_dashboard.html')

    @app.route('/userinputdata')
    def userinputdata():
        return render_template('user_input_data.html')

    @app.route('/operator')
    def operator():
        return render_template('operator_dashboard')

    return app