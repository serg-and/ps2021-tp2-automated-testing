import urllib.parse as urlparse
import MySQLdb
import json
import cgi
import tempfile
import subprocess


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

            if method != 'POST':
                start_response('303 See Other', [('Location', '../sell.html')])
            else:
                temp_file = tempfile.TemporaryFile()
                temp_file.write(environ['wsgi.input'].read())
                temp_file.seek(0)

                field_storage = cgi.FieldStorage(
                    fp=temp_file,
                    environ=environ,
                    keep_blank_values=True
                )

                cursor.execute("SELECT MAX(`id`) FROM `Product`")
                productid = str(cursor.fetchall()[0][0] + 1)

                cursor.execute(
                    "INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (%s, %s, %s, %s, %s)", (
                    productid, field_storage['product-name'].value, field_storage['price'].value,
                    field_storage['description'].value, user))
                db.commit()

                subprocess.run(["mkdir", "/usr/local/apache2/htdocs/assets/img/products/" + productid])

                try:
                    for i in range(len(field_storage['file'])):
                        fileitem = field_storage['file'][i]
                        open("/usr/local/apache2/htdocs/assets/img/products/" + productid + "/" + str(i) + ".jpg", 'wb').write(fileitem.file.read())
                except TypeError:
                    fileitem = field_storage['file']
                    open("/usr/local/apache2/htdocs/assets/img/products/" + productid + "/0.jpg", 'wb').write(fileitem.file.read())

                temp_file.close()

                start_response('303 See Other', [('Location', 'product.py?id=' + productid)])

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
