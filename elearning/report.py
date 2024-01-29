from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from elearning .auth import login_required
from elearning .db import get_db

bp = Blueprint('report', __name__)

"""
Student Must registr for major 
    the student will nee only his/her grade 
Lecturer rigistrer the student 
    input grade 
    view all student 
    update all student grade 
    crud posts on dashboard 
    
"""

@bp.route('/view_stu')
@login_required
def view_stu():
    db = get_db()
    users = db.execute(
        'SELECT u.id, u.name, u.phone, u.email, m.name AS major_name '
        'FROM users u '
        'JOIN students s ON u.id = s.user_id '
        'JOIN major m ON s.major_id = m.id'
    ).fetchall()
    
    return render_template('report/view_stu.html', users=users)

# @bp.route('/add_stu')
# @login_required
# def add_stu():
#     db = get_db()
    