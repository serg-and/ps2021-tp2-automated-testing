import urllib.parse as urlparse
import MySQLdb
import json
from os import path


def application(environ, start_response):
    html = ''

    if "HTTP_COOKIE" not in environ:
        start_response("303 See Other", [("Location", "../login.html")])
    else:
        cookies = urlparse.parse_qs(environ["HTTP_COOKIE"])
        request_cookie = cookies.get("session", [''])[0]

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

        if result_session is None:
            start_response("303 See Other", [("Location", "../login.html")])
        else:
            user = str(result_session[0])

            status = "200 OK"
            response_header = [("Content-type", "text/html")]
            start_response(status, response_header)

            # fetching all user data & flags
            cursor.execute("SELECT `displayName` FROM `User` WHERE `id` = %s", (user,))
            displayname = cursor.fetchone()[0]

            cursor.execute("SELECT * FROM `Flags`")
            flags = cursor.fetchall()

            html += '<html lang="en">\n'
            html += '    <head>\n'
            html += '        <title>Rough Road </title>\n'
            html += '        <meta charset="utf-8">\n'
            html += '        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">\n'
            html += '        <title>CTF progress</title>\n'
            html += '        <link rel="stylesheet" href="../assets/bootstrap/css/bootstrap.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/fontawesome-all.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/font-awesome.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/fontawesome5-overrides.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/css/navbar.css">\n'
            html += '        <link rel="stylesheet" href="../assets/css/products-page.css">\n'
            html += '    </head>\n'
            html += '    <body>\n'
            html += '        <nav class="navbar navbar-light navbar-expand-md navigation-clean">\n'
            html += '            <div class="container">\n'
            html += '                <a class="navbar-brand" href="products.py"><em>Rough Road</em></a>\n'
            html += '                <button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>\n'
            html += '                    <div class="collapse navbar-collapse" id="navcol-1">\n'
            html += '                        <ul class="navbar-nav ml-auto">\n'
            html += '                            <li class="nav-item" id="sellButton">\n'
            html += '                                <a class="nav-link active" href="sell.py">Sell now</a>\n'
            html += '                            </li>\n'
            html += '                            <li class="nav-item dropdown">\n'
            html += '                                <a class="dropdown-toggle nav-link" aria-expanded="false" data-toggle="dropdown">' + displayname

            if path.isfile('/usr/local/apache2/htdocs/assets/img/avatars/' + str(user) + '.jpg'):
                html += '<img class="profile" src="../assets/img/avatars/' + str(user) + '.jpg"></a>\n'
            else:
                html += '<img class="profile" src="../assets/img/avatar.png"></a>\n'

            html += '                                <div class="dropdown-menu">\n'
            html += '                                    <a class="dropdown-item" href="account.py"><i class="fa fa-user"></i>&nbsp;Account</a>\n'
            # html += '                                    <a class="dropdown-item" href="#"><i class="fa fa-heart"></i>&nbsp;Favorites</a>\n'
            html += '                            </li>\n'
            # html += '                            <li class="nav-item"><a id="cart" href="#"><i class="fa fa-shopping-cart"></i></a></li>\n'
            html += '                        </ul>\n'
            html += '                    </div>\n'
            html += '            </div>\n'
            html += '        </nav>\n'
            html += '        <nav class="navbar navbar-light navbar-expand-md navigation-clean-search">\n'
            html += '            <div class="container">\n'
            html += '                <div class="collapse navbar-collapse">\n'
            html += '                    <ul class="navbar-nav">\n'
            html += '                        <li class="nav-item">\n'
            html += '                            <a class="nav-link" href="products.py">Products</a>\n'
            html += '                        </li>\n'
            html += '                        <li class="nav-item">\n'
            html += '                            <a class="nav-link" href="flags.py">Flags</a>\n'
            html += '                        </li>\n'
            html += '                        <li>\n'
            html += '                            <a class="nav-link" href="aboutus.py">About</a>\n'
            html += '                        </li>\n'
            html += '                    </ul>\n'
            html += '                    <form class="form-inline mr-auto" action="products.py" target="_self">\n'
            html += '                        <div class="form-group"><label for="search-field"></label><i class="fa fa-search"></i><input class="form-control search-field" type="search" id="search-field" name="search" placeholder="Search..."></div>\n'
            html += '                    </form>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </nav>\n'
            html += '        <div class="container">\n'
            html += '            <div class="row">\n'
            html += '                <div class="col-md-4 col-sm-12 offset-md-4">\n'
            html += '                    <div class="card mt-5 text-center">\n'
            html += '                        <h1>Flag 1</h1>\n'
            html += '                        <p>Create a review that automatically likes itself when a user visits its page</p>\n'
            html += '                        <p>Status:\n'
            html += '                        <svg width="24px" height="24px"><g fill="green"><path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"></path></g></svg><strong class="text-success"> complete</strong></p>\n' if flags[0][1] == b'\x01' else '<strong class="text-danger">nope</strong></p>'
            html += '                        <h1>Flag 2</h1>\n'
            html += '                        <p>Hijack another users session and change their display name</p>\n'
            html += '                        <p>Status:\n'
            html += '                        <svg width="24px" height="24px"><g fill="green"><path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"></path></g></svg><strong class="text-success"> complete</strong></p>\n' if flags[1][1] == b'\x01' else '<strong class="text-danger">nope</strong></p>'
            html += '                        <h1>Flag 3</h1>\n'
            html += '                        <p>Delete the account of a hijacked session</p>\n'
            html += '                        <p>Status:\n'            
            html += '                        <svg width="24px" height="24px"><g fill="green"><path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"></path></g></svg><strong class="text-success"> complete</strong></p>\n' if flags[2][1] == b'\x01' else '<strong class="text-danger">nope</strong></p>'
            html += '                    </div>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </div>\n'
            html += '        <script src="../assets/js/jquery.min.js"></script>\n'
            html += '        <script src="../assets/bootstrap/js/bootstrap.min.js"></script>\n'
            html += '    </body>\n'
            html += '</html>\n'

        cursor.close()
        db.close()

    return [bytes(html, "utf-8")]