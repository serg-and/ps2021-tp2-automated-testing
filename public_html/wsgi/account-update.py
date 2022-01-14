# made by Esmee from the RR team
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

        # ip addre
        request_ip = environ['REMOTE_ADDR']
        cursor.execute("SELECT `login_ip` FROM `Session` WHERE `session_id` = %s", (request_cookie,))
        login_ip = cursor.fetchone()[0]


        # Kijkt of de session_id bij een gebruiker hoort
        if result_session is None:
            # Inkomende request heeft geen session, wordt doorgestuurd naar login pagina
            start_response('303 See Other', [('Location', '../login.html')])
        else:
            user = str(result_session[0])
            method = environ.get('REQUEST_METHOD', '')

            # Cheks if the request is POST
            if method != 'POST':
                # Redirects user to the account page
                start_response('303 See Other', [('Location', 'account.py')])
            else:
                # Redirects user to the account page
                start_response('303 See Other', [('Location', 'account.py?succes=Updated%20account%20info')])

                # ------------------ USER CHANGES HIS DATA ---------------------------------------->
                # retrieves info from html name values for updating account
                updateInput = environ['wsgi.input'].read().decode()
                params = urlparse.parse_qs(updateInput)
                email = params.get('email', [''])[0]
                displayName = params.get('displayname', [''])[0]
                password = params.get('password', [''])[0]

                if request_ip != login_ip:
                    flag_2 = """UPDATE `Flags` SET `state` = %s WHERE `challenge` = %s"""
                    cursor.execute(flag_2, (1, 'Challenge 2'))

                # queries to update info to database with corresponding execution
                update_mailQuery = """UPDATE `User` SET `email`= %s WHERE `id` = %s"""
                cursor.execute(update_mailQuery, (email, user))

                update_displayNameQuery = """UPDATE `User` SET `displayName`= %s WHERE `id` = %s"""
                cursor.execute(update_displayNameQuery, (displayName, user))

                start_response('303 See Other', [('Location', './account.py')])

                #update_passwordQuery = """UPDATE `User` SET `password`= %s WHERE `id` = %s"""
                #cursor.execute(update_passwordQuery, (password, user))
                # update_betaalgegevensQuery = """UPDATE `User` SET ``= %s WHERE `id` = %s"""
                # cursor.execute()
                # update_afleverdadresQuery = """UPDATE `User` SET ``= %s WHERE `id` = %s"""
                # cursor.execute()

                db.commit()

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
