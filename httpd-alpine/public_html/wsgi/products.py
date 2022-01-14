import urllib.parse as urlparse
import MySQLdb
import json
from os import path


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

            status = '200 OK'
            response_header = [('Content-type', 'text/html')]
            start_response(status, response_header)

            params = urlparse.parse_qs(environ['QUERY_STRING'])
            searchValue = params.get('search', [''])[0]

            if searchValue != '':
                cursor.execute("SELECT `id`, `name`, `price` FROM `Product` WHERE `name` COLLATE UTF8_GENERAL_CI LIKE %s", ("%" + searchValue + "%",))
            else:
                cursor.execute("SELECT `id`, `name`, `price` FROM `Product`")

            products = cursor.fetchall()

            cursor.execute("SELECT `displayName` FROM `User` WHERE `id` = %s", (user,))
            displayname = cursor.fetchone()[0]

            html += '<html lang="en">\n'
            html += '    <head>\n'
            html += '        <title>Rough Road </title>\n'
            html += '        <meta charset="utf-8">\n'
            html += '        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">\n'
            html += '        <title>home.html</title>\n'
            html += '        <link rel="stylesheet" href="../assets/bootstrap/css/bootstrap.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/fontawesome-all.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/font-awesome.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/fonts/fontawesome5-overrides.min.css">\n'
            html += '        <link rel="stylesheet" href="../assets/css/navbar.css">\n'
            html += '        <link rel="stylesheet" href="../assets/css/products-page.css">\n'
            html += '    </head>\n'
            html += '    <body style="background: rgb(0,0,0);">\n'
            html += '        <nav class="navbar navbar-light navbar-expand-md navigation-clean">\n'
            html += '            <div class="container">\n'
            html += '                <a class="navbar-brand" href="products.py"><em>Rough Road</em></a>\n'
            html += '                <button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>\n'
            html += '                    <div class="collapse navbar-collapse" id="navcol-1">\n'
            html += '                        <ul class="navbar-nav ml-auto">\n'
            html += '                            <li class="nav-item" id="sellButton">\n'
            html += '                                <a class="nav-link active" href="sell.py">Sell now</a>\n'
            html += '                            </li>\n'
            html += '                               <li class="nav-item dropdown">\n'
            html += '                                <a class="dropdown-toggle nav-link" aria-expanded="false" data-toggle="dropdown">' + displayname

            if path.isfile('/usr/local/apache2/htdocs/assets/img/avatars/' + str(user) + '.jpg'):
                html += '<img class="profile" src="../assets/img/avatars/' + str(user) + '.jpg"></a>\n'
            else:
                html += '<img class="profile" src="../assets/img/avatar.png"></a>\n'

            html += '                                <div class="dropdown-menu">\n'
            html += '                                    <a class="dropdown-item" href="account.py"><i class="fa fa-user"></i>&nbsp;Account</a>\n'
            # html += '                                    <a class="dropdown-item" href="#"><i class="fa fa-heart"></i>&nbsp;Favorites</a>\n'
            html += '                               </li>\n'
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
            html += '                    <form class="form-inline mr-auto" target="_self">\n'
            html += '                        <div class="form-group"><label for="search-field"></label><i class="fa fa-search"></i><input class="form-control search-field" type="search" id="search-field" name="search" placeholder="Search..."></div>\n'
            html += '                    </form>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </nav>\n'
            html += '        <div class="banner">\n'
            html += '            <h1 class="banner-title">Ready to ride?  </h1>\n'
            html += '            <a class="btn banner-button" role="button" href="sell.py">Sell now</a>\n'
            html += '        </div>\n'
            html += '        <div class="container">\n'
            html += '            <div class="row product-list">\n'

            for i in products:
                html += '                <div class="col- col-sm-6 col-md-3 product-item">\n'
                html += '                    <div class="product-container">\n'
                html += '                        <div class="row">\n'
                html += '                            <div class="col-md-12"><a class="product-image" href="product.py?id=' + str(i[0]) + '"><img src="../assets/img/products/' + str(i[0]) + '/0.jpg" alt="missing cover image"></a></div>\n'
                html += '                        </div>\n'
                html += '                        <div class="row">\n'
                html += '                            <div class="col-12">\n'
                html += '                                <h2><a href="product.py?id=' + str(i[0]) + '">' + str(i[1]) + '</a></h2>\n'
                html += '                            </div>\n'
                html += '                        </div>\n'
                html += '                        <div class="row">\n'
                html += '                            <div class="col-12">\n'
                html += '                                <p class="product-price"><i class="fa fa-eur"></i>&nbsp;' + str(i[2]) + '</p>\n'
                html += '                            </div>\n'
                html += '                        </div>\n'
                html += '                    </div>\n'
                html += '                </div>\n'


            html += '            </div>\n'
            html += '        </div>\n'
            html += '        <script src="../assets/js/jquery.min.js"></script>\n'
            html += '        <script src="../assets/bootstrap/js/bootstrap.min.js"></script>\n'
            html += '        <script src="../assets/js/Paralax-Hero-Banner.js"></script>\n'
            html += '    </body>\n'
            html += '</html>\n'

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
