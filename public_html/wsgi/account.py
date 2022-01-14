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
            error_msg = params.get('error', [''])[0]
            succes_msg = params.get('succes', [''])[0]

            # query to view info from database
            viewQuery = """SELECT `email`, `displayName` FROM `User` WHERE `id` = %s"""
            cursor.execute(viewQuery, (user,))  # executes the view query
            userInfo = cursor.fetchone()  # fetches the info
            # the users info that will get displayed (to later put inside html)
            emailVal = userInfo[0]
            displayname = userInfo[1]

            html += '<html>\n'
            html += '    <head>\n'
            html += '    <title>Account</title>\n'
            html += '    <meta charset="utf-8">\n'
            html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">\n'
            html += '    <link rel="stylesheet" href="../assets/bootstrap/css/bootstrap.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/fontawesome-all.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/font-awesome.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/fonts/fontawesome5-overrides.min.css">\n'
            html += '    <link rel="stylesheet" href="../assets/css/navbar.css">\n'
            html += '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css">\n'
            html += '       <style>\n'
            html += '           body {\n'
            html += '           margin: 0;\n'
            html += '           font-family: sans-serif;\n'
            html += '           }\n'
            html += '           .Main ul {\n'
            html += '             list-style-type: none;\n'
            html += '             margin: 0;\n'
            html += '             padding: 0;\n'
            html += '             width: 25%;\n'
            html += '             background-color: #f1f1f1;\n'
            html += '             position: fixed;\n'
            html += '             height: 100%;\n'
            html += '             top: 86px;\n'
            html += '             overflow: auto;\n'
            html += '           }\n'
            html += '           .Main li a {\n'
            html += '             display: block;\n'
            html += '             color: #000;\n'
            html += '             padding: 50px 16px;\n'
            html += '             text-decoration: none;\n'
            html += '           }\n'
            html += '           .Main li a.active {\n'
            html += '             background-color: ;\n'
            html += '             color: white;\n'
            html += '           }\n'
            html += '           .Main li a:hover:not(.active) {\n'
            html += '             background-color:#ad0505;\n'
            html += '             color: white;\n'
            html += '           }\n'
            html += '           .error{\n'
            html += '             background-color:#ffb3b3;\n'
            html += '             color:darkred;\n'
            html += '             margin-top: 10px;\n'
            html += '             margin-bottom: 10px;\n'
            html += '             padding: 6px;\n'
            html += '           }\n'
            html += '           .succes{\n'
            html += '             background-color:#ccffcc;\n'
            html += '             color:darkgreen;\n'
            html += '             margin-top: 10px;\n'
            html += '             margin-bottom: 10px;\n'
            html += '             padding: 6px;\n'
            html += '           }\n'
            html += '           .Main .main-content{\n'
            html += '             margin-top: 0px;\n'
            html += '           }\n'
            html += '           .ButtonSmall {\n'
            html += '             background-color: red;\n'
            html += '             color: white;\n'
            html += '             padding: 14px 20px;\n'
            html += '             margin: 8px 0;\n'
            html += '             border: none;\n'
            html += '             cursor: pointer;\n'
            html += '             width: 120px;\n'
            html += '             opacity: 0.9;\n'
            html += '           }\n'
            html += '           button {\n'
            html += '             background-color: red;\n'
            html += '             color: white;\n'
            html += '             padding: 14px 20px;\n'
            html += '             margin: 8px 0;\n'
            html += '             border: none;\n'
            html += '             cursor: pointer;\n'
            html += '             width: 100%;\n'
            html += '             opacity: 0.9;\n'
            html += '           }\n'
            html += '           .cancelbtn {\n'
            html += '             background-color: #ccc;\n'
            html += '             color: black;\n'
            html += '           }\n'
            html += '           .modal {\n'
            html += '             display: none; /* Hidden by default */\n'
            html += '             position: fixed; /* Stay in place */\n'
            html += '             z-index: 1; /* Sit on top */\n'
            html += '             padding-top: 100px; /* Location of the box */\n'
            html += '             left: 0;\n'
            html += '             top: 0;\n'
            html += '             width: 100%; /* Full width */\n'
            html += '             height: 100%; /* Full height */\n'
            html += '             overflow: auto; /* Enable scroll if needed */\n'
            html += '             background-color: rgb(0,0,0); /* Fallback color */\n'
            html += '             background-color: rgba(0,0,0,0.4); /* Black w/ opacity */\n'
            html += '           }\n'
            html += '           \n'
            html += '           /* Modal Content */\n'
            html += '           .modal-content {\n'
            html += '             background-color: #fefefe;\n'
            html += '             margin: auto;\n'
            html += '             padding: 20px;\n'
            html += '             border: 1px solid #888;\n'
            html += '             width: 100%;\n'
            html += '             max-width: 800px;\n'
            html += '           }\n'
            html += '       </style>\n'
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
            html += '    <nav class="navbar navbar-light navbar-expand-md navigation-clean-search">\n'
            html += '        <div class="container">\n'
            html += '            <div class="collapse navbar-collapse">\n'
            html += '                <ul class="navbar-nav">\n'
            html += '                    <li class="nav-item">\n'
            html += '                        <a class="nav-link" href="products.py">Products</a>\n'
            html += '                    </li>\n'
            html += '                    <li class="nav-item">\n'
            html += '                        <a class="nav-link" href="flags.py">Flags</a>\n'
            html += '                    </li>\n'            
            html += '                    <li class="nav-item">\n'
            html += '                        <a class="nav-link" href="aboutus.py">About</a>\n'
            html += '                    </li>\n'
            html += '                </ul>\n'
            html += '                <form class="form-inline mr-auto" action="products.py" target="_self">\n'
            html += '                    <div class="form-group"><label for="search-field"></label><i class="fa fa-search"></i><input class="form-control search-field" type="search" id="search-field" name="search" placeholder="Search..."></div>\n'
            html += '                </form>\n'
            html += '            </div>\n'
            html += '        </div>\n'
            html += '    </nav>\n'
            html += '   <div class="Main">\n'
            html += '       <div style="margin-left:25%;padding:0px 20px;">\n'
            html += '          <div class= "main-content">\n'

            if error_msg != '':
                html += '              <div class="error">Failed: ' + error_msg + '</div>\n'
            elif succes_msg != '':
                html += '              <div class="succes">' + succes_msg + '</div>\n'

            html += '              <section id="section1">\n'
            html += '                  <form action="upload-pp.py" method="post" enctype="multipart/form-data">\n'
            html += '                      <h3>Upload Profile Picture</h3>\n'
            html += '                      <input class="ButtonSmall" type="submit" value="Upload">\n'
            html += '                      <input type="file" name="pp" required>\n'
            html += '                      <br>\n'
            html += '                  </form>\n'
            html += '                  <form action="account-update.py" method="post">\n'
            html += '                      <h3>Basic info</h3>\n'
            html += '                      Display Name : <input type="text" class="input" name="displayname" value="' + displayname + '" required>\n'
            html += '                      <br>\n'
            html += '                          <br>\n'
            html += '                      E-mail : <input type="text" class="input" name="email" value="' + emailVal + '" required>\n'
            html += '                      <br>\n'
            html += '                      <input class="ButtonSmall" type="submit" value="Update">\n'
            html += '                  </form>\n'
            html += '              </section>\n'
            html += '              <section id="section2">\n'
            html += '                  <h2>Delete Account</h2>\n'
            html += '                  <button class="ButtonSmall" onclick="document.getElementById(' + "'id01'" + ').style.display=' + "'block'" + '">Delete</button>\n'
            html += '                  <div id="id01" class="modal" style="display: none;">\n'
            html += '                      <span onclick="document.getElementById(' + "'id01'" + ').style.display=' + "'none'" + '" class="close" title="Close Modal">×</span>\n'
            html += '                      <form class="modal-content" action="account-delete.py" method="post">\n'
            html += '                          <div class="container">\n'
            html += '                            <h1>Delete Account</h1>\n'
            html += '                            <p>Are you sure you want to delete your account?</p>\n'
            html += '                            <div>\n'
            html += '                                <button type="button" onclick="document.getElementById(' + "'id01'" + ').style.display=' + "'none'" + '" class="cancelbtn">Cancel</button>\n'
            html += '                                <button type="submit">Delete</button>\n'
            html += '                            </div>\n'
            html += '                          </div>\n'
            html += '                      </form>\n'
            html += '                  </div>\n'
            html += '                  <script>\n'
            html += '                  // Get the modal\n'
            html += '                  var modal = document.getElementById(' + "'id01'" + ');\n'
            html += '                  // When the user clicks anywhere outside of the modal, close it\n'
            html += '                  window.onclick = function(event) {\n'
            html += '                    if (event.target == modal) {\n'
            html += '                      modal.style.display = "none";\n'
            html += '                    }\n'
            html += '                  }\n'
            html += '                  </script>\n'
            html += '              </section>\n'
            html += '              </div>\n'
            html += '          </div>\n'
            html += '       </div>\n'
            html += '    </div>\n'
            html += '    </body>\n'
            html += '    <script src="../assets/js/jquery.min.js"></script>\n'
            html += '    <script src="../assets/bootstrap/js/bootstrap.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js"></script>\n'
            html += '    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.min.js"></script>\n'
            html += '</html>\n'

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
