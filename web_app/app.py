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
from models import db, Content, Role, User, dataCatin
from views import MyModelView, ContentView, dataCatinView

def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    bootstrap = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin = flask_admin.Admin(
        app,
        'Example: Auth',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )

    admin.add_view(ContentView(Content, db.session))
    admin.add_view(dataCatinView(dataCatin, db.session))
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


    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/society')
    def society():
        return render_template('society_dashboard.html')

    @app.route('/userinputdata')
    def userinputdata():
        return render_template('user_input_data.html')

    return app