from flask import Blueprint, render_template, request

from flaskr.db import get_db
from flaskr.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/lookup', methods=['GET', 'POST'])
@admin_required
def lookup():
    db = get_db()
    if request.method == 'POST':
        d = request.form['id']
        admin = request.form['isadmin']
        try:
            db.execute('UPDATE user SET isadmin = ? WHERE id = ?', (1 if admin == 'y' else 0, d))
            db.commit()
        except db.IntegrityError: # pragma: no cover
            db.rollback()
    data = db.execute('SELECT user.devname,id,conf,iou,isadmin FROM config,user WHERE config.devname = user.devname').fetchall()
    return render_template('admin/lookup.html', data = data)

