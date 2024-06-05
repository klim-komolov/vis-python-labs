from math import ceil
from flask import Blueprint, request, url_for, render_template,send_file
from mysql_db import MySQL
import io


stats_bp = Blueprint('stats', __name__, url_prefix = '/stats')
mysql = MySQL(stats_bp)

PER_PAGE = 5


@stats_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM stats LIMIT %s OFFSET %s', (PER_PAGE, offset))
        stats = cursor.fetchall()
        cursor.close()
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT COUNT(*) AS total FROM stats')
        total = cursor.fetchone().total
        cursor.close()
    last_page = ceil(total/PER_PAGE)
    return render_template('stats/index.html', stats=stats, page=page, last_page=last_page)


@stats_bp.route('/export_csv')
def export_csv():
    csv_data=''
    keys = ['path', 'user_id']
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM stats')
        stats = cursor.fetchall()
    csv_data = ', '.join(keys) + '\n'
    for stat in stats:
        values = [str(getattr(stat,key, '')) for key in keys]
        csv_data += ', '.join(values) + '\n'

    f = io.BytesIO()
    f.write(csv_data.encode('utf-8'))
    f.seek(0)
    return send_file(f, as_attachment=True, download_name='stats.csv')


@stats_bp.route('/export_csv_by_users')
def export_csv_by_users():
    csv_data=''
    keys = ['full_name', 'count']
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name) AS full_name, COUNT(*) as count
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id
            GROUP BY full_name
            ORDER BY count DESC
        ''')
        stats = cursor.fetchall()
    csv_data = ', '.join(keys) + '\n'
    for stat in stats:
        if stat.full_name:
            full_name = stat.full_name
        else:
            full_name = "Неаутентифицированный пользователь"
        values = [full_name, str(stat.count)]
        csv_data += ', '.join(values) + '\n'

    f = io.BytesIO()
    f.write(csv_data.encode('utf-8'))
    f.seek(0)
    return send_file(f, as_attachment=True, download_name='stats.csv')


@stats_bp.route('/by_routes')
def by_routes():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE
    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT path, COUNT(*) as count
            FROM stats
            GROUP BY path
            ORDER BY COUNT(*) DESC
            LIMIT %s OFFSET %s
        ''', (PER_PAGE, offset))
        stats = cursor.fetchall()

    with mysql.connection().cursor(named_tuple=True, buffered=True) as cursor:
        cursor.execute('SELECT COUNT(*) AS total FROM stats GROUP BY path')
        total = cursor.fetchone().total

    last_page = ceil(total/PER_PAGE)
    return render_template('stats/by_routes.html', stats=stats, page=page, last_page=last_page)



@stats_bp.route('/by_users')
def by_users():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('''
            SELECT CONCAT_WS(' ', users.first_name, users.middle_name, users.last_name) AS full_name, COUNT(*) as count
            FROM stats
            LEFT JOIN users ON stats.user_id = users.id
            GROUP BY full_name
            ORDER BY count DESC
            LIMIT %s OFFSET %s
        ''', (PER_PAGE, offset))
        stats = cursor.fetchall()

    with mysql.connection().cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT COUNT(DISTINCT user_id) AS total FROM stats')
        total = cursor.fetchone().total

    last_page = ceil(total/PER_PAGE)
    return render_template('stats/by_users.html', stats=stats, page=page, last_page=last_page)
