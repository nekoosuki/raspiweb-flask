from flask import Blueprint, flash, g, render_template, request

from flaskr.db import get_db

from werkzeug.security import check_password_hash

bp = Blueprint('api',__name__,url_prefix='/api')

SUPER_PASS = 'pbkdf2:sha256:150000$5Cqj28Iz$f02e435ac70cbc86bd8143ea8e8f8be2c16ff630f9b0ace74fdd3885a685c4b1'

@bp.route('/query_config', methods=['POST'])
def query_config():
    devname = request.form['n']
    p = request.form['p']

    db = get_db()
    if check_password_hash(SUPER_PASS,p):
        dev = db.execute('SELECT conf,iou FROM config,user WHERE devname = ? AND config.id=user.id',(devname,)).fetchone()
        if dev is None:
            return {'code':-1}

        return {'conf':dev['conf'],'iou':dev['iou'],'code':0}
    
    return {'code':-1}
