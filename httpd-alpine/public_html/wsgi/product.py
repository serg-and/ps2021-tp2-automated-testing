import urllib.parse as urlparse
import MySQLdb
import json
from os import path
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

            status = '200 OK'
            response_header = [('Content-type', 'text/html')]
            start_response(status, response_header)

            params = urlparse.parse_qs(environ['QUERY_STRING'])
            productid = params.get('id', [''])[0]

            cursor.execute("SELECT `displayName` FROM `User` WHERE `id` = %s", (user,))
            displayname = cursor.fetchone()[0]

            cursor.execute("SELECT `Product`.`id`, `name`, `price`, `description`, `displayName` FROM `Product` INNER JOIN `RRdb`.`User` ON `User_id`=`User`.`id` WHERE `Product`.`id`=%s", (productid,))
            productInfo = cursor.fetchone()

            cursor.execute("SELECT `User`.`id`, `User`.`displayName`, `dateTime`, `text` FROM `Review` INNER JOIN `RRdb`.`User` ON `User_id`=`id` WHERE `Product_id`=%s ORDER BY `dateTime`", (productid,))
            reviews = cursor.fetchall()

            html += '<html>\n'
            html += '    <head>\n'
            html += '    <title>Rough Road </title>\n'
            html += '    <meta charset="utf-8">\n'
            html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">\n'
            html += '    <link rel="stylesheet" href="../assets/bootstrap/css/bootstrap.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/fontawesome-all.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/font-awesome.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/fontawesome5-overrides.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/css/navbar.css">\n'
            html += '    <link rel="stylesheet" href="../assets/css/style-product-page.css">\n'
            html += '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css">\n'
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
            html += '                                    <a class="dropdown-item" href="#"><i class="fas fa-wallet"></i>&nbsp;Wallet</a>\n'
            html += '                                    <a class="dropdown-item" href="#"><i class="fa fa-heart"></i>&nbsp;Favorites</a>\n'
            html += '                                    <a class="dropdown-item" href="#"><i class="fa fa-history"></i>&nbsp;Order History</a>\n'
            html += '                                    <a class="dropdown-item" href="#"><i class="fa fa-gear"></i>&nbsp;Settings</a></div>\n'
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
            html += '                        <li class="nav-item">\n'
            html += '                            <a class="nav-link" href="aboutus.py">About</a>\n'
            html += '                        </li>\n'
            html += '                    </ul>\n'
            html += '                    <form class="form-inline mr-auto" target="_self">\n'
            html += '                        <div class="form-group"><label for="search-field"></label><i class="fa fa-search"></i><input class="form-control search-field" type="search" id="search-field" name="search" placeholder="Search..."></div>\n'
            html += '                    </form>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </nav>\n'
            html += '        <div class="container" id="container1">\n'
            html += '            <div class="row">\n'
            html += '                <div class="col-md-5">\n'
            html += '                            <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">\n'
            html += '  <div class="carousel-indicators">\n'

            arch = str(subprocess.check_output("ls /usr/local/apache2/htdocs/assets/img/products/" + productid + "/ | wc -l", shell=True))
            imgCount = int(arch.replace("\\", "'").split("'")[1])

            for i in range(imgCount):
                if i == 0:
                    html += '    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="' + str(i) + '" class="active" aria-current="true" aria-label="Slide ' + str(i + 1) + '"></button>\n'
                else:
                    html += '    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="' + str(i) + '" aria-label="Slide ' + str(i + 1) + '"></button>\n'

            html += '  </div>\n'
            html += '  <div class="carousel-inner">\n'

            for i in range(imgCount):
                if i == 0:
                    html += '    <div class="carousel-item active" id="carousels">\n'
                    html += '      <img src="../assets/img/products/' + productid + '/' + str(i) + '.jpg" class="d-block w-100 h-100" alt="Slide' + str(i + 1) + '">\n'
                    html += '    </div>\n'
                else:
                    html += '    <div class="carousel-item" id="carousels">\n'
                    html += '      <img src="../assets/img/products/' + productid + '/' + str(i) + '.jpg" class="d-block w-100 h-100" alt="Slide' + str(i + 1) + '">\n'
                    html += '    </div>\n'

            html += '  </div>\n'
            html += '  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"  data-bs-slide="prev">\n'
            html += '    <span class="carousel-control-prev-icon" aria-hidden="true"></span>\n'
            html += '    <span class="visually-hidden">Previous</span>\n'
            html += '  </button>\n'
            html += '  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"  data-bs-slide="next">\n'
            html += '    <span class="carousel-control-next-icon" aria-hidden="true"></span>\n'
            html += '    <span class="visually-hidden">Next</span>\n'
            html += '  </button>\n'
            html += '</div>\n'
            html += '                </div>\n'
            html += '                <div class="col-md-7">\n'
            html += '                    <p class="newarrival text-center">NEW</p>\n'
            html += '                    <h2>' + productInfo[1] + '</h2>\n'
            html += '                    <p class="seller">Seller: <a href="#"><b>' + productInfo[4] + '</b></a></p>\n'
            html += '                    <p class="price">€' + str(productInfo[2]) + '</p>\n'
            html += '                    <p><b>Availability:</b> In stock</p>\n'
            html += '                    <p><b>Condition:</b> New</p>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </div>\n'
            html += '        <div class="container" id="container-description">\n'
            html += '            <div class="row">\n'
            html += '                <h3>Description</h3>\n'
            html += '                <p>' + str(productInfo[3]) + '</p>\n'
            html += '            </div>\n'
            html += '        </div>\n'
            html += '        <div class="container" id="container-reviews">\n'
            html += '            <div class="row" id="reviews">\n'
            html += '                <h2>Reviews</h2>\n'

            for i in reviews:
                # totaal waarde voor likes en dislikes
                cursor.execute("SELECT COUNT(*), `User_id` FROM `Dislike` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s", (productid, i[0], i[2]))
                dislikes = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*), `User_id` FROM `Like` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s", (productid, i[0], i[2]))
                likes = cursor.fetchone()[0]
                # heeft de gebruiker geliked of gedisliked
                cursor.execute("SELECT COUNT(*) FROM `Dislike` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, i[0], i[2], user))
                disliked = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM `Like` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, i[0], i[2], user))
                liked = cursor.fetchone()[0]

                html += '                <div class="Comment">\n'
                html += '                    <div class="Avatar">'

                if path.isfile('/usr/local/apache2/htdocs/assets/img/avatars/' + str(i[0]) + '.jpg'):
                    html += '<img src="../assets/img/avatars/' + str(i[0]) + '.jpg" alt="Avatar"></div>\n'
                else:
                    html += '<img src="../assets/img/avatar.png" alt="Avatar"></div>\n'

                html += '                    <div class="Comment-body">\n'
                html += '                        <div class="Comment-header">\n'
                html += '                            <span class="user">' + str(i[1]) + '</span>\n'
                html += '                            <span class="Comment-datetime">' + str(i[2]) + '</span>\n'
                html += '                            <span class="likes">\n'

                # bij disliked/liked > 0 heeft de gebruiker geliked of gedisliked
                if disliked > 0:
                    html += '                                <a class="disliked" href="add-like.py?val=dislike&product=' + productid + '&user=' + str(i[0]) + '&time=' + str(i[2]) + '"><i class="fa fa-thumbs-down" style="color:blue"></i></a> ' + str(dislikes) + '&nbsp;\n'
                else:
                    html += '                                <a class="dislikey" href="add-like.py?val=dislike&product=' + productid + '&user=' + str(i[0]) + '&time=' + str(i[2]) + '"><i class="fa fa-thumbs-down" style="color:grey"></i></a> ' + str(dislikes) + '&nbsp;\n'

                if liked > 0:
                    html += '                                <a class="liked" href="add-like.py?val=like&product=' + productid + '&user=' + str(i[0]) + '&time=' + str(i[2]) + '"><i class="fa fa-thumbs-up" style="color:blue"></i></a> ' + str(likes) + '\n'
                else:
                    html += '                                <a class="likey" href="add-like.py?val=like&product=' + productid + '&user=' + str(i[0]) + '&time=' + str(i[2]) + '"><i class="fa fa-thumbs-up" style="color:grey"></i></a> ' + str(likes) + '\n'

                html += '                            </from></span>\n'
                html += '                        </div>\n'
                html += '                        <div class="Comment-text">' + str(i[3]) + '</div>\n'
                html += '                    </div>\n'
                html += '                </div>\n'

            html += '                <form class="Write-review" action=add-comment.py method="post">\n'
            html += '                    <div>\n'
            html += '                        <textarea class="resizedTextbox" name="message" placeholder="Write a review" rows="3" required></textarea>\n'
            html += '                    </div>\n'
            html += '                    <div>\n'
            html += '                        <input type="submit" value="Place review">\n'
            html += '                    </div>\n'
            html += '                    <input type="hidden" name="product-id" value="' + productid + '"/>\n'
            html += '                    <input type="hidden" name="user-id" value="' + str(user) + '"/>\n'
            html += '                </form>\n'
            html += '            </div>\n'
            html += '        </div>\n'
            html += '    <script src="../assets/js/jquery.min.js"></script>\n'
            html += '    <script src="../assets/bootstrap/js/bootstrap.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.min.js"></script>\n'
            html += '    </body>\n'
            html += '</html>\n'

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
