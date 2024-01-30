from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

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


@bp.route('/edit_stu/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_stu(user_id):
    db = get_db()
    majors = db.execute('SELECT id, name FROM major').fetchall()
    user = db.execute(
        'SELECT u.id, u.name, u.phone, u.email, m.name AS major_name, s.major_id '
        'FROM users u '
        'JOIN students s ON u.id = s.user_id '
        'JOIN major m ON s.major_id = m.id '
        'WHERE u.id = ?',
        (user_id,)
    ).fetchone()

    if user is None:
        # Handle the case when the user does not exist
        return redirect(url_for('view_stu'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        major_id = request.form['major_id']
        db = get_db()
        db.execute(
            'UPDATE users SET name = ?, phone = ? WHERE id = ?',
            (name, phone, user_id)
        )
        db.execute(
            'UPDATE students SET major_id = ? WHERE user_id = ?',
            (major_id, user_id)
        )
        db.commit()
        flash('User updated successfully!')

        return redirect(url_for('report.view_stu'))

    return render_template('report/edit_stu.html', user=user, majors=majors)


@bp.route('/delete_stu/<int:user_id>', methods=['POST'])
@login_required
def delete_stu(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()

    return redirect(url_for('view_stu'))


@bp.route('/g_report', methods=['GET', 'POST'])
def g_report():
    db = get_db()
    student = db.execute(
        'SELECT students.id, students.major_id, students.user_id, major.name '
        'FROM students JOIN major ON students.major_id = major.id '
        'WHERE students.user_id = ?',
        (session['user_id'],)
    ).fetchone()

    majors = db.execute('SELECT id, name FROM major').fetchall()
    return render_template('report/g_report.html', student=student, majors=majors)

