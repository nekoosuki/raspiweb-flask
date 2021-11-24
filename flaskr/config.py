from flask import Blueprint, flash, g, render_template, request

from flaskr.db import get_db
from flaskr.auth import login_required

import re


bp = Blueprint('config', __name__)

@bp.route('/',methods=['GET'])
@login_required
def config_interface():
    return render_template('config.html')


@bp.route('/business/config', methods=['GET', 'POST'])
@login_required
def config():
    db = get_db()
    if request.method == 'POST':
        conf = request.form['conf']
        iou = request.form['iou']

        if not conf or not iou:
            #为了flash可用，出错时必须刷新页面，待优化
            flash("Input not complete")
            return {'code':-1}

        if re.search(r'^(0.\d+|0|1)$', str(conf)) is None or re.search(r'^(0.\d+|0|1)$', str(iou)) is None:
            flash("Input values between 0 and 1")
            return {'code':-1}

        try:
            db.execute('UPDATE config SET conf = ?, iou = ? WHERE devname = ?', (conf, iou, str(g.dev['devname'])))
            db.commit()
        except db.IntegrityError: # pragma: no cover
            db.rollback()
            flash("Unexcepted error")
            return {'code':-2}
    
    config = dict(db.execute('SELECT * FROM config WHERE devname = ?',(str(g.dev['devname']),)).fetchone())
    config['code'] = 0
    return config


