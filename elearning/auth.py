import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from elearning.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    majors = db.execute('SELECT id, name FROM major').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        major_id = request.form['major_id']

        error = None
        if not name:
            error = 'Name is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not major_id:
            error = 'Major is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (name, phone, email, password, role_id) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, email, generate_password_hash(password), 3),
                )
                db.commit()
                user = db.execute(
                    'SELECT * FROM users WHERE email = ?', (email,)
                ).fetchone()
                db.execute(
                    'INSERT INTO students (major_id, user_id) VALUES (?, ?)',
                    (major_id, user['id'])
                )
                db.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for("auth.login"))
            except db.IntegrityError:
                error = f"User {email} already exists."

        flash(error)

    return render_template('auth/register.html', majors=majors)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def login_required_role(role_id):
    def decorator(f):
        @functools.wraps(f)
        def wrapped_view(*args, **kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))

            if g.user['role_id'] != role_id:
                return redirect(url_for('auth.unauthorized'))

            return f(*args, **kwargs)
        return wrapped_view
    return decorator

@bp.route('/unauthorized')
def unauthorized():
    return render_template('auth/unauthorized.html')

"""
#reigistration for lect
@bp.route('/register2', methods=('GET', 'POST'))
def register2():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        if not name:
            error = 'Name is required.'
        elif not phone:
            error = 'Password is required.'
        elif not email:
            error = 'Password is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (name, phone, email, password, role_id) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, email, generate_password_hash(password), 2),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register2.html')
"""