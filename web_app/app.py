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
from form import RegisterFormView, LoginFormView, SocietyInputDataView, OperatorAddDataView, EditCatin
import time
def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    url_index = 'http://localhost:8716/'

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

    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        form = LoginFormView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                session['email'] = request.form['email']
                takeEmail = session['email'] = request.form['email']
                takeRoles = User.query.filter_by(email=takeEmail).first()
                takeRoles = takeRoles.roles
                # takeRoles = ''.join(takeRoles)
                print('testing', takeRoles)
                user = User.query.filter_by(email=form.email.data).first()
                if verify_password(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    login_user(user, remember=form.remember.data)
                    if takeRoles == ['user']:
                        return redirect(url_for('operator'))
                    elif takeRoles == []:
                        return redirect(url_for('society'))
                else:
                    return '<h1>Invalid username or password</h1>'

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/society')
    @login_required
    def society():
        dataUser = User('', '', '')

        id_user = current_user.id

        try:
            result, nik_catin_laki_laki = db.session.query(User, DataCatin.NIK_catin_laki_laki).join(DataCatin).\
                filter(DataCatin.user_id == current_user.id).first()
            result, nama_catin_laki_laki = db.session.query(User, DataCatin.nama_catin_laki_laki).join(DataCatin).\
                filter(DataCatin.user_id == current_user.id).first()
            result, nik_catin_perempuan = db.session.query(User, DataCatin.NIK_catin_perempuan).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, nama_catin_perempuan = db.session.query(User, DataCatin.nama_catin_perempuan).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, tanggal_daftar = db.session.query(User, DataCatin.tanggal_daftar).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, jadwal_nikah = db.session.query(User, DataCatin.jadwal_nikah).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, jam = db.session.query(User, DataCatin.jam).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, tempat_pelaksaan_nikah = db.session.query(User, DataCatin.tempat_pelaksaan_nikah).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
            result, status_pendaftaran = db.session.query(User, DataCatin.status_pendaftaran).join(DataCatin). \
                filter(DataCatin.user_id == current_user.id).first()
        except:
            nik_catin_laki_laki = '-'
            nama_catin_laki_laki = '-'
            nik_catin_perempuan = '-'
            nama_catin_perempuan = '-'
            tanggal_daftar = '-'
            jadwal_nikah = '-'
            jam = '-'
            tempat_pelaksaan_nikah = '-'
            status_pendaftaran = '-'

        # return render_template('society_dashboard.html', WELCOME=current_user.name)
        return render_template('society_dashboard.html', WELCOME=current_user.name, NIK_LAKI_LAKI=nik_catin_laki_laki,
                               NAMA_CATIN_LAKI_LAKI=nama_catin_laki_laki, NIK_CATIN_PEREMPUAN=nik_catin_perempuan,
                               NAMA_CATIN_PEREMPUAN=nama_catin_perempuan, TANGGAL_DAFTAR=tanggal_daftar,
                               JAM=jam, JADWAL_NIKAH=jadwal_nikah, TEMPAT_PELAKSAAN_NIKAH=tempat_pelaksaan_nikah,
                               STATUS_PENDAFTARAN=status_pendaftaran)


    @app.route('/societyinputdata', methods = ['GET', 'POST'])
    @login_required
    def societyInputData():
        form = SocietyInputDataView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                tanggal_daftar = time.strftime("%Y-%m-%d %H:%M:%S")
                add_jam = request.form['jam']
                new_data = DataCatin(form.NIK_catin_laki_laki.data, form.nama_catin_laki_laki.data,
                                     form.NIK_catin_perempuan.data, form.nama_catin_perempuan.data,
                                     tanggal_daftar, form.jadwal_nikah.data, add_jam, form.tempat_pelaksaan_nikah.data, current_user.id)
                db.session.add(new_data)
                db.session.commit()
                return redirect(url_for('society'))

        return render_template('society_input_data.html', form=form)

    @app.route('/operator', methods = ['GET', 'POST'])
    @login_required
    def operator():
        if 'email' in session:
            name = current_user.name
            all_user_data = DataCatin.query.all()
            return render_template('operator_dashboard.html', WELCOME=current_user.name, catin=all_user_data)
        else:
            return redirect(url_for('index'))

    @app.route('/operatorAddData', methods=['GET', 'POST'])
    @login_required
    def operatorAddData():
        dataUser = User('', '', '')
        form = OperatorAddDataView(request.form)
        operator_name = current_user.name
        if request.method == 'POST':
            if form.validate_on_submit():
                add_jam = request.form['jam']
                new_data = DataCatin(form.NIK_catin_laki_laki.data, form.nama_catin_laki_laki.data,
                                     form.NIK_catin_perempuan.data, form.nama_catin_perempuan.data,
                                     form.tanggal_daftar.data, form.jadwal_nikah.data, add_jam,
                                     form.tempat_pelaksaan_nikah.data, current_user.id, False,
                                     form.status_pendaftaran.data)
                db.session.add(new_data)
                # db.session.commit()
                try:
                    db.session.commit()
                except:
                    return 'Data yang dimasukan sudah ada, mohon diulangi!!!'
                return redirect(url_for('operator'))

        return render_template('operatorAddData.html', form=form, OPERATOR_NAME=operator_name)


    @app.route('/delete_data/<id>')
    def delete_data(id):
        data = db.session.query(DataCatin, User).join(User).filter(DataCatin.id == id).first()
        if data.DataCatin.is_public:
            return render_template('catin_detail.html', catin=data)
        else:
            # if current_user.is_authenticated and data.DataCatin.user_id == current_user.id:
            if current_user.is_authenticated:
                data = DataCatin.query.filter_by(id=id).first()
                db.session.delete(data)
                db.session.commit()
        return redirect(url_for('operator'))


    @app.route('/catin_edit/<id>', methods=['GET', 'POST'])
    def catin_edit(id):
        data = db.session.query(DataCatin, User).join(User).filter(DataCatin.id== id).first()
        form = EditCatin(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                # if current_user.is_authenticated and data.DataCatin.user_id == current_user.id:
                if current_user.is_authenticated:
                    data = DataCatin.query.filter_by(id=id).first()
                    new_nik_L = form.NIK_catin_laki_laki.data
                    new_name_L = form.nama_catin_laki_laki.data
                    new_nik_P = form.NIK_catin_perempuan.data
                    new_name_P = form.nama_catin_perempuan.data
                    new_tanggal_daftar = form.tanggal_daftar.data
                    new_jadwal = form.jadwal_nikah.data
                    new_jam = request.form['jam']
                    new_tempat_pelaksaan_nikah = form.tempat_pelaksaan_nikah.data
                    new_status_pendaftaran = form.status_pendaftaran.data
                    try:
                        data.NIK_catin_laki_laki = new_nik_L
                        data.nama_catin_laki_laki = new_name_L
                        data.NIK_catin_perempuan = new_nik_P
                        data.nama_catin_perempuan = new_name_P
                        data.jadwal_nikah = new_jadwal
                        data.tanggal_daftar = new_tanggal_daftar
                        data.jam = new_jam
                        data.tempat_pelaksaan_nikah = new_tempat_pelaksaan_nikah
                        data.status_pendaftaran = new_status_pendaftaran
                        db.session.commit()

                    except Exception as e:
                        return {'error': str(e)}
                return redirect(url_for('operator'))

        return render_template('edit_catin.html', form=form, catin=data)

    return app