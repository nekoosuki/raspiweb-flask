from flask import Blueprint, render_template

from flaskr.db import get_db
from flaskr.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/lookup', methods=['GET'])
@admin_required
def lookup():
    db = get_db()
    data = db.execute('SELECT user.devname,id,conf,iou,isadmin FROM config,user WHERE config.devname = user.devname').fetchall()
    return render_template('admin/lookup.html', data = data)

