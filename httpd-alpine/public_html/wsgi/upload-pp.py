import urllib.parse as urlparse
import MySQLdb
import json
import cgi
import tempfile


def application(environ, start_response):
    html = ''

    if 'HTTP_COOKIE' not in environ:
        # Inkomende request heeft geen session, wordt doorgestuurd naar login pagina
        start_response('303 See Other', [('Location', '../login.html')])
    else:
        cookies = urlparse.parse_qs(environ['HTTP_COOKIE'])
        request_cookie = cookies.get('session', [''])[0]

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
        cursor = db.cursor()
        cursor.execute("SELECT `User_id` FROM `Session` WHERE `session_id` = %s", (request_cookie,))
        result_session = cursor.fetchone()

        # Kijkt of de session_id bij een gebruiker hoort
        if result_session is None:
            # Inkomende request heeft geen session, wordt doorgestuurd naar login pagina
            start_response('303 See Other', [('Location', '../login.html')])
        else:
            user = str(result_session[0])
            method = environ.get('REQUEST_METHOD', '')
            
            if method == 'POST':
                temp_file = tempfile.TemporaryFile()
                temp_file.write(environ['wsgi.input'].read())
                temp_file.seek(0)
                
                field_storage = cgi.FieldStorage(
                    fp=temp_file,
                    environ=environ,
                    keep_blank_values=True
                )

                cursor.execute("UPDATE `User` SET `avatar` = id WHERE id=%s", (user,))
                        
                # for i in range(len(field_storage['file'])):
                fileitem = field_storage['pp']
                open("/usr/local/apache2/htdocs/assets/img/avatars/" + str(user) + ".jpg", 'wb').write(fileitem.file.read())

                temp_file.close()

                html = 'OK'
                start_response('303 See Other', [('Location', 'account.py?succes=Uploaded%20profile%20picture')])
            else:
                start_response('303 See Other', [('Location', 'account.py')])
    
        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
