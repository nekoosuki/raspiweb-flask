import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from flaskr.db import get_db
from flaskr.auth import login_required

import re


bp = Blueprint('config', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()
    if request.method == 'POST':
        conf = request.form['conf']
        iou = request.form['iou']
        error = None

        if not conf or not iou:
            error = "Input not complete"

        if re.search('^(0.\d+|0|1)$', str(conf)) is None or re.search('^(0.\d+|0|1)$', str(iou)) is None:
            error = "Input decimals between 0 and 1"

        if error is None:
            try:
                db.execute('UPDATE config SET conf = ?, iou = ? WHERE devname = ?', (conf, iou, str(g.dev['devname'])))
                db.commit()
            except db.IntegrityError:
                pass
            else:
                error = 'update successful'
        flash(error)
    
    config = db.execute('SELECT * FROM config WHERE devname = ?',(str(g.dev['devname']),)).fetchone()
    return render_template('config.html',config=config)


