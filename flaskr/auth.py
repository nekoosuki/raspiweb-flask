import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

SUPER_PASS = 'neko'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        devname = request.form['devname']
        password = request.form['password']
        adminpass = request.form['admin']
        db = get_db()
        error = None

        if not devname:
            error = 'Devname is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:

            try:
                if adminpass == SUPER_PASS:
                    db.execute('INSERT INTO user (devname, password, isadmin) VALUES (?, ?, ?)', (devname, generate_password_hash(password),1))
                else:
                    db.execute('INSERT INTO user (devname, password) VALUES (?, ?)', (devname, generate_password_hash(password)))
                db.execute('INSERT INTO config (devname) VALUES (?)', (devname,))
                db.commit()
            except db.IntegrityError:
                error = f'Device {devname} is already registered'
                db.rollback()
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        devname = request.form['devname']
        password = request.form['password']
        db = get_db()
        error = None
        dev = db.execute('SELECT * FROM user WHERE devname = ?', (devname,)).fetchone()

        if dev is None:
            error = 'Incorrect devname.'
        elif not check_password_hash(dev['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['devid'] = dev['id']
            session['devname'] = devname
            return redirect(url_for('config'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    devid = session.get('devid')
    devname = session.get('devname')
    if devid is None or devname is None:
        g.dev = None
    else:
        db = get_db()
        g.dev = db.execute('SELECT * FROM user WHERE id = ?', (devid,)).fetchone()

@bp.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.dev is None:
            return redirect(url_for('auth.login'))
        
        return view(*args,**kwargs)
    
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    @login_required
    def wrapped_view(*args,**kwargs):
        if g.dev['isadmin'] == 0:
            return redirect(url_for('config'))

        return view(*args,**kwargs)
    
    return wrapped_view