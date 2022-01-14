import urllib.parse as urlparse
import MySQLdb
import json
import secrets
import bcrypt


def application(environ, startresponse):
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    startresponse(status, response_header)

    # defining request method and responding based on it
    method = environ.get('REQUEST_METHOD', '')

    params = {}
    if method == 'POST':
        input = environ['wsgi.input'].read().decode()
        params = urlparse.parse_qs(input)
    else:
        startresponse('303 See Other', [('Location', 'http://localhost:5000')])

    # papa database login credentials worden opgehaald
    with open('/run/secrets/papa_login') as f:
        data = json.load(f)
    papa_user = data["MYSQL_USER"]
    papa_login = data["MYSQL_PASSWORD"]

    # papa verbinding opstellen
    papa = MySQLdb.connect(
        host="papa",
        user=papa_user,
        passwd=papa_login,
        db="PAPAdb",
    )

    # PAPA.Database id en hash opvragen
    cursor = papa.cursor()
    query = """SELECT id, wwhash FROM PAPAdb.User"""
    cursor.execute(query)
    gegevens = cursor.fetchall()

    cursor.close()
    papa.close()

    # Gebruiker input
    email_input = params.get('email', [''])[0]
    password_input = params.get('password', [''])[0]
    password_input_bytes = bytes(password_input, 'utf-8')

    # Database login credentials worden opgehaald
    with open('/run/secrets/db_login') as f:
        data = json.load(f)
    db_user = data["MYSQL_USER"]
    db_login = data["MYSQL_PASSWORD"]

    # Zazabase verbinding opstellen
    db = MySQLdb.connect(
        host="mysql",
        user=db_user,
        passwd=db_login,
        db="RRdb",
    )
    # ZAAZAA.Database email, id opvragen
    cursor = db.cursor()
    query = """SELECT id, email FROM RRdb.User"""
    cursor.execute(query)
    record = cursor.fetchall()

    html = ''
    html += '<!DOCTYPE html>\n'
    html += '<html>\n'
    html += '<head> \n'
    html += '	<meta charset="utf-8">\n'
    html += '	<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '	<!-- stylesheets -->\n'
    html += '	<link rel="stylesheet" type="text/css" href="/assets/bootstrap/css/bootstrap(login).min.css">\n'
    html += '	<link rel="stylesheet" type="text/css" href="/assets/css/login.css">\n'
    html += '	<title>Login | Rough road</title>\n'
    html += '</head>\n'
    html += '<body>\n'
    html += '   	<div class="row g-0">\n'
    html += '       	<div class="col g-0">\n'
    html += '           	<div class="left-side"></div>\n'
    html += '       	</div>\n'
    html += '       	<div class="col g-0">\n'
    html += '           	<div class="right-side"></div>\n'
    html += '       	</div>\n'
    html += '   	</div>\n'
    html += '\n'
    html += '   	<div class="container-fluid bg">\n'
    html += '       	<div class="row justify-content-center">\n'
    html += '           	<div class="col-12 col-sm-6 col-md-3">\n'
    html += '\n'
    html += '               	<form class="form-container" action="/wsgi/login.py" method="post">\n'
    html += '\n'

    # Controleren van de inloggegevens ( gegevens : papa | records : zaazaa)
    for (id1,wwhash),(id2,email) in zip(gegevens,record):
        # de hash naar bytes formateren
        password_hash = bytes(wwhash, 'utf-8')

        if email_input == str(email) and bcrypt.checkpw(password_input_bytes, password_hash) and id2 == id1:
            # cookie implementeren
            sessionid = secrets.token_hex(32)
            request_ip = environ['REMOTE_ADDR']
            http_user_agent = environ['HTTP_USER_AGENT']

            # id opvragen
            cursor.execute("""SELECT id FROM User WHERE `email` = %s""", (email_input,))
            userid = cursor.fetchall()[0]

            sql = """ UPDATE `Session` SET `session_id` = %s, `login_ip` = %s, `http_user_agent` = %s WHERE `User_id` = %s """
            cursor.execute(sql, (sessionid, request_ip, http_user_agent, userid))
            db.commit()

            def set_cookie_header(name, value):

                return 'Set-Cookie', '{}={}; '.format(name, value)

            startresponse('303 See Other', [set_cookie_header('session', sessionid), ('Location', '/wsgi/products.py')])

    html += '                        <p style="color: red;">Login failed, wrong credentials</p>\n'

    cursor.close()
    db.close()

    html += '                   	<div class="mb-3">\n'
    html += '                       	<label class="form-label">Email</label>\n'
    html += '                       	<input type="text" class="form-control" name="email" required>\n'
    html += '                       	<div class="form-text"> And remember to be careful out there.</div>\n'
    html += '                   	</div>\n'
    html += '                   	<div class="mb-3">\n'
    html += '                       	<labelclass="form-label">Password</label>\n'
    html += '                       	<input type="password" class="form-control" name="password" required>\n'
    html += '                   	</div>\n'
    html += '                   	<div class="mb-3 form-check">\n'
    html += '                       	<input type="checkbox" class="form-check-input">\n'
    html += '                       	<label class="form-check-label" for="exampleCheck1">Keep me logged in</label>\n'
    html += '                   	</div>\n'
    html += '                   	<div class="container">\n'
    html += '                       	<div class="row">\n'
    html += '                           	<div class="col text-center">\n'
    html += '                               	<input type="submit" value="Start The Fun" class="btn btn-primary btn-lg active">\n'
    html += '                           	</div>\n'
    html += '                       	</div>\n'
    html += '                   	</div>\n'
    html += '               	</form>\n'
    html += '           	</div>\n'
    html += '       	</div>\n'
    html += '   	</div>\n'
    html += '	</body>\n'
    html += '</html>\n'

    return [bytes(html, 'utf-8')]