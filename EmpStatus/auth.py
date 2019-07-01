import functools
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,send_file
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            if username != 'admin':
                session.clear()
                session['user_id'] = user['id']
                session['name'] = user['username']
                return redirect(url_for('auth.employeeStatus'))
            else:
                session.clear()
                session['user_id'] = user['id']
                session['name'] = user['username']
                return redirect(url_for('auth.list'))
        flash(error)
    return render_template('auth/login.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/list')
def list():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM Status'
    ).fetchall()
    return render_template('dashboard.html', posts=posts)

@bp.route('/export_excelfile', methods=['GET', 'POST'])
def export_excelfile():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM Status'
    ).fetchall()
    df = DataFrame(posts)
    df.columns = ['Emp ID','Username','Project Name','Day','Status']
    df.to_excel (r'..\EmpStatus\export.xlsx', index = None, header=True)
    return send_file('../EmpStatus/export.xlsx', attachment_filename='export.xlsx',as_attachment=True)
    # return render_template('dashboard.html', posts=posts)

@bp.route('/employeeStatus', methods=('GET', 'POST'))
def employeeStatus():
    error = None
    if request.method == 'POST':
        user_id = session.get('user_id')
        name = session.get('name')
        projectName = request.form['project']
        date = request.form['date']
        status = request.form['status']
        db = get_db()
        if not projectName:
            error = 'Project is required.'
        elif not date:
            error = 'Date is required.'
        elif not status:
            error = 'Status is required.'
        db.execute(
            'INSERT INTO Status (user_id, name, projectName, day, statusEmp) VALUES (?, ?, ?, ?, ?)',
                (user_id, name, projectName, date, status)
            )
        db.commit()
        return redirect(url_for('auth.logout'))
    flash(error)
    return render_template('index.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
