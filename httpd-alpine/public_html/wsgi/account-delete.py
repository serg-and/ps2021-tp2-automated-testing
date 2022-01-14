import urllib.parse as urlparse
import MySQLdb
import json


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
            request_ip = environ['REMOTE_ADDR']
            cursor.execute("SELECT `login_ip` FROM `Session` WHERE `session_id` = %s", (request_cookie,))
            login_ip = cursor.fetchone()[0]

            # Controleert of het ip van de request gelijk is aan het ip tijdens het inloggen
            if request_ip != login_ip:
                # Redirect naar account pagina, inclusief error message
                start_response('303 See Other', [('Location', 'account.py?error=ip-mismatch')])
            else:
                user = str(result_session[0])
                method = environ.get('REQUEST_METHOD', '')

                if method != 'POST':
                    start_response('303 See Other', [('Location', 'account.py')])
                else:
                    # Controleert of de HTTP_USER_AGENT van de request ongelijk is aan die tijdens het inloggen
                    # Challenge 3 is gehaald, database wordt geupdate
                    request_user_agent = environ['HTTP_USER_AGENT']
                    cursor.execute("SELECT `http_user_agent` FROM `Session` WHERE `session_id` = %s", (request_cookie,))
                    login_user_agent = cursor.fetchone()[0]

                    if request_user_agent != login_user_agent:
                        cursor.execute("UPDATE `Flags` SET `state` = 1 WHERE `challenge` = 'Challenge 3'")
                        db.commit()

                    # De gebruiker wordt verwijdert
                    sql = "DELETE FROM `User` WHERE `id` = %s"
                    cursor.execute(sql, (user,))
                    db.commit()
                    
                    start_response('303 See Other', [('Location', 'account.py')])
        
        cursor.close()
        db.close()
    
    return [bytes(html, 'utf-8')]
