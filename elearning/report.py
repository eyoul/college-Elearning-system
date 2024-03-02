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

"""
# @bp.route('/delete_stu/<int:user_id>', methods=['POST'])
# @login_required
# def delete_stu(user_id):
#     db = get_db()
#     db.execute('DELETE FROM users WHERE id = ?', (user_id,))
#     db.commit()

#     return redirect(url_for('view_stu'))
"""
@bp.route('/g_report', methods=['GET', 'POST'])
def g_report():
    db = get_db()
    student = db.execute(
        'SELECT students.id, students.major_id, students.user_id, major.name '
        'FROM students JOIN major ON students.major_id = major.id '
        'WHERE students.user_id = ?',
        (session['user_id'],)
    ).fetchone()
    gradereport = db.execute(
        'SELECT g.id, g.student_id, u.name AS student_name, g.lecturer_id, l.name AS lecturer_name, '
        'g.course_id, c.name AS course_code, c.description AS course_name, g.grade, g.creditH '
        'FROM grades g '
        'JOIN students s ON g.student_id = s.id '
        'JOIN users u ON s.user_id = u.id '
        'JOIN users l ON g.lecturer_id = l.id '
        'JOIN courses c ON g.course_id = c.id ' 
        'WHERE s.user_id = ?',
        (session['user_id'],)
).fetchall()
    return render_template('report/g_report.html', student=student, gradereport=gradereport)


@bp.route('/stu_report', methods=['GET', 'POST'])
def stu_report():
    db = get_db()
    grades = db.execute(
        'SELECT g.id, g.student_id, u.name AS student_name, g.lecturer_id, l.name AS lecturer_name, '
        'g.course_id, c.name AS course_name, g.grade, g.creditH '
        'FROM grades g '
        'JOIN students s ON g.student_id = s.id '
        'JOIN users u ON s.user_id = u.id '
        'JOIN users l ON g.lecturer_id = l.id '
        'JOIN courses c ON g.course_id = c.id'
    ).fetchall()

    return render_template('report/stu_report.html', grades=grades)
# Define your grading scale
grading_scale = {
    'A+': [90, 100],
    'A': [83, 90],
    'A-': [80, 83],
    'B+': [75, 80],
    'B': [68, 75],
    'B-': [65, 68],
    'C+': [60, 65],
    'C': [50, 60],
    'C-': [45, 50],
    'D': [40, 45],
    'Fx': [30, 40],
    'F': [0, 30]
}


@bp.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        # Retrieve the form data
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        raw_grade = int(request.form['grade'])
        creditH = int(request.form['creditH'])

        grade = determine_grade(raw_grade)
        # Insert the new grade into the database
        db = get_db()
        try:
            db.execute(
                'INSERT INTO grades (student_id, lecturer_id, course_id, grade, creditH) '
                'VALUES (?, ?, ?, ?, ?)',
                (student_id, g.user['id'], course_id, grade, creditH)
            )
            db.commit()

        # Redirect to the grades page
            return redirect(url_for('report.stu_report'))
        except db.IntegrityError:
            error = f"The course is alrady exist"
        flash(error)

    # Retrieve necessary data for the form
    db = get_db()
    students = db.execute(
        'SELECT s.id, s.user_id, u.name AS student_name '
        'FROM students s '
        'JOIN users u ON s.user_id = u.id'
    ).fetchall()

    courses = db.execute('SELECT * FROM courses').fetchall()

    # Render the add_grade.html template with the form and data
    return render_template('report/add_grade.html', students=students, courses=courses)

def determine_grade(score):
    for grade, range_ in grading_scale.items():
        if range_[0] <= score < range_[1]:
            return grade
    return 'Invalid'

"""

Raw Mark Interval [100 %]	Corresponding fixed
Number Grade

Corresponding
Letter Grade

Status Description	Class Description
[90,100]	4.0	    A+	Excellent	First class with Great distinction
[83, 90)	4.0	    A
[80, 83)	3.75	A–
[75, 80)	3.5	    B+	Very Good	First class with Distinction
[68, 75)	3.0	    B
[65, 68)	2.75	B–	Good	First class
[60, 65)	2.5	    C+	Second class
[50, 60)	2.0	    C	Satisfactory
[45, 50)	1.75	C–	Unsatisfactory	Lower class
[40,45)	    1.0	    D	Very Poor	Lower class
[30,40)	    0	    Fx	Fail	Lowest class
[<30)	    0	    F	Fail	Lowest class
"""