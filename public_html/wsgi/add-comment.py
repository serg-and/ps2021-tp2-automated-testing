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
            user = str(result_session[0])

            method = environ.get('REQUEST_METHOD', '')
            input = environ['wsgi.input'].read().decode()
            params = urlparse.parse_qs(input)
            productid = params.get('product-id', [''])[0]
            msg = params.get('message', [''])[0]

            if method == 'POST' and msg != '':
                cursor.execute("INSERT INTO `Review` (`Product_id`, `User_id`, `dateTime`, `text`) VALUES (%s, %s, NOW(), %s)", (productid, user, msg))
                db.commit()

                start_response('303 See Other', [('Location', 'product.py?id=' + productid + '#reviews')])
            else:
                start_response('303 See Other', [('Location', 'products.py')])

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
