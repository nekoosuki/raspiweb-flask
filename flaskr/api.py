from flask import Blueprint, flash, g, render_template, request

from flaskr.db import get_db


bp = Blueprint('api',__name__,url_prefix='/api')

SUPER_PASS = 'neko'

@bp.route('/query_config', methods=['POST'])
def query_config():
    devname = request.form['n']
    p = request.form['p']

    db = get_db()
    if p == SUPER_PASS:
        dev = db.execute('SELECT * FROM config WHERE devname = ?',(devname,)).fetchone()
        if dev is None:
            return {'code':-1}

        return {'conf':dev['conf'],'iou':dev['iou'],'code':0}
    
    return {'code':-1}
