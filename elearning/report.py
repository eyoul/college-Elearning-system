from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from flask_login import current_user, LoginManager
from werkzeug.exceptions import abort

from elearning .auth import login_required
from elearning .db import get_db

bp = Blueprint('report', __name__)



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


@bp.route('/streem', methods=['GET', 'POST'])
def streem():
    if 'user_id' not in session:
        flash('Please log in to register a major.', 'info')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        major_id = request.form['major_id']
        db = get_db()
        db.execute(
            'UPDATE students SET major_id = ? WHERE user_id = ?',
            (major_id, session['user_id'])
        )
        db.commit()
        flash('Major registration successful!', 'success')

    db = get_db()
    student = db.execute(
        'SELECT students.id, students.major_id, students.user_id, major.name '
        'FROM students JOIN major ON students.major_id = major.id '
        'WHERE students.user_id = ?',
        (session['user_id'],)
    ).fetchone()

    majors = db.execute('SELECT id, name FROM major').fetchall()
    return render_template('report/streem.html', student=student, majors=majors)




"""
Student Must registr for major 
    the student will nee only his/her grade 
Lecturer rigistrer the student 
    input grade 
    view all student 
    update all student grade 
    crud posts on dashboard 
    

@bp.route('/view_stu')
@login_required
def view_stu():
    db = get_db()
    users = db.execute(
        'SELECT  name, phone, email '
        'FROM users'
    ).fetchall()
    
    return render_template('report/view_stu.html', users=users)

# @bp.route('/add_stu')
# @login_required
# def add_stu():
#     db = get_db()
"""