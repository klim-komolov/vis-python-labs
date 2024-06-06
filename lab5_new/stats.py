from math import ceil
from flask import Blueprint, request, url_for, render_template, send_file, flash, redirect
from flask_login import current_user

from mysql_db import MySQL
import io

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')
mysql = MySQL(stats_bp)

PER_PAGE = 5


@stats_bp.route('/')
def index():
    if current_user.is_admin():
        query_info = '''
        SELECT 
            CASE
                WHEN users.first_name IS NULL AND users.middle_name IS NULL AND users.last_name IS NULL
                THEN 'Неаутентифицированный пользователь'
                ELSE CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name)
            END AS full_name,
            path,
            created_at
        FROM stats
        LEFT JOIN users ON stats.user_id = users.id
        LIMIT %s OFFSET %s;
        '''
        query_count = 'SELECT COUNT(*) AS total FROM stats'
    else:
        query_info = f'''
        SELECT 
            CASE
                WHEN users.first_name IS NULL AND users.middle_name IS NULL AND users.last_name IS NULL
                THEN 'Неаутентифицированный пользователь'
                ELSE CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name)
            END AS full_name,
            path,
            created_at
        FROM stats
        LEFT JOIN users ON stats.user_id = users.id
        WHERE user_id = {current_user.id} 
        LIMIT %s OFFSET %s;
        '''
        print(query_info)
        query_count = f'SELECT COUNT(*) AS total FROM stats WHERE user_id = {current_user.id}'

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query_info, (PER_PAGE, offset))
        stats = cursor.fetchall()
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query_count)
        total = cursor.fetchone().total
    last_page = ceil(total / PER_PAGE)
    return render_template('stats/index.html', stats=stats, page=page, last_page=last_page)


@stats_bp.route('/export_csv')
def export_csv():
    mode = request.args.get(key='mode', type=str)
    print(f'view_{mode}', current_user.can(f'view_{mode}'))
    if not current_user.can(f'view_{mode}'):
        flash(f'Вы не можете это сделать', 'danger')
        return redirect(request.referrer)

    if mode == 'index':
        if current_user.is_admin():
            sql_query = '''
            SELECT 
                CASE
                    WHEN users.first_name IS NULL AND users.middle_name IS NULL AND users.last_name IS NULL
                    THEN 'Неаутентифицированный пользователь'
                    ELSE CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name)
                END AS full_name,
                path,
                created_at
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id;
            '''
        else:
            sql_query = f'''
            SELECT 
                CASE
                    WHEN users.first_name IS NULL AND users.middle_name IS NULL AND users.last_name IS NULL
                    THEN 'Неаутентифицированный пользователь'
                    ELSE CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name)
                END AS full_name,
                path,
                created_at
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id
            WHERE user_id = {current_user.id};
            '''
        keys = ['path', 'full_name', 'created_at']
    elif mode == 'by_routes':
        sql_query = '''
            SELECT path, COUNT(*) as count
            FROM stats
            GROUP BY path
            ORDER BY count DESC
        '''
        keys = ['path', 'count']
    elif mode == 'by_users':
        sql_query = '''
            SELECT CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name) as full_name, 
            COUNT(*) as count
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id
            GROUP BY full_name
            ORDER BY count DESC
        '''
        keys = ['full_name', 'count']

    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(sql_query)
        stats = cursor.fetchall()
    csv_data = ', '.join(keys) + '\n'
    for stat in stats:
        values = [str(getattr(stat, key, '')) for key in keys]
        csv_data += ', '.join(values) + '\n'

    f = io.BytesIO()
    f.write(csv_data.encode('utf-8'))
    f.seek(0)
    return send_file(f, as_attachment=True, download_name='stats.csv')


@stats_bp.route('/by_routes')
def by_routes():
    if not current_user.can(f'view_by_routes'):
        flash(f'Вы не можете это сделать', 'danger')
        return redirect(url_for('stats.index'))

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''        
            SELECT path, COUNT(*) as count
            FROM stats
            GROUP BY path
            ORDER BY count DESC
            LIMIT %s OFFSET %s
        ''', (PER_PAGE, offset))
        stats = cursor.fetchall()

    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT path) AS total 
            FROM stats
        ''')
        total = cursor.fetchone().total

    last_page = ceil(total / PER_PAGE)
    return render_template('stats/by_routes.html', stats=stats, page=page, last_page=last_page)


@stats_bp.route('/by_users')
def by_users():
    if not current_user.can(f'view_by_users'):
        flash(f'Вы не можете это сделать', 'danger')
        return redirect(url_for('stats.index'))

    page = request.args.get('page', default=1, type=int)
    offset = (page - 1) * PER_PAGE
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name) as full_name, 
            COUNT(*) as count
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id
            GROUP BY full_name
            ORDER BY count DESC
            LIMIT %s OFFSET %s
        ''', (PER_PAGE, offset))
        stats = cursor.fetchall()

    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT stats.user_id) AS total
            FROM stats
        ''')
        total = cursor.fetchone().total

    last_page = ceil(total / PER_PAGE)
    print(total)
    return render_template('stats/by_users.html', stats=stats, page=page, last_page=last_page)
