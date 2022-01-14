import urllib.parse as urlparse
import MySQLdb
import json
import datetime

# this entire script only runs when there is being clicked on a button.

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

            params = urlparse.parse_qs(environ['QUERY_STRING'])
            value = params.get('val', [''])[0]
            productid = params.get('product', [''])[0]
            review_user = params.get('user', [''])[0]
            dateTime = params.get('time', [''])[0]

            cursor.execute("SELECT COUNT(*) FROM `Dislike` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
            disliked = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM `Like` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
            liked = cursor.fetchone()[0]

            # measures the time when pressed on button
            pressButtonTime = datetime.datetime.now()
            # time that the challenge has to be done, adds 1 second to the posted review datetime
            deltaChallengeReviewTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=1.5)
            if pressButtonTime < deltaChallengeReviewTime:
                updateFlagQuery = """UPDATE `Flags` SET `State` = 1 WHERE `challenge`= 'Challenge 1'"""
                cursor.execute(updateFlagQuery)
                db.commit()

            if value == 'dislike':
                if disliked > 0:
                    # User heeft comment al gedisliked, dislike wordt verwijderd
                    cursor.execute("DELETE FROM `Dislike` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
                    db.commit()
                elif disliked == 0 and liked == 0:
                    # User heeft comment nog niet gedisliked, dislike wordt toegevoegd
                    cursor.execute("INSERT INTO `Dislike` (`Review_Product_id`, `Review_User_id`, `Review_dateTime`, `User_id`) VALUES (%s, %s, %s, %s)", (productid, review_user, dateTime, user))
                    db.commit()
                elif disliked == 0 and liked > 0:
                    # User heeft comment al geliked, like wordt verwijderd, dislike wordt toegevoegd
                    cursor.execute("DELETE FROM `Like` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
                    db.commit()
                    cursor.execute("INSERT INTO `Dislike` (`Review_Product_id`, `Review_User_id`, `Review_dateTime`, `User_id`) VALUES (%s, %s, %s, %s)", (productid, review_user, dateTime, user))
                    db.commit()
            elif value == 'like':
                if liked > 0:
                    # User heeft comment al geliked, like wordt verwijderd
                    cursor.execute("DELETE FROM `Like` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
                    db.commit()
                elif liked == 0 and disliked == 0:
                    # User heeft comment nog niet geliked, like wordt toegevoegd
                    cursor.execute("INSERT INTO `Like` (`Review_Product_id`, `Review_User_id`, `Review_dateTime`, `User_id`) VALUES (%s, %s, %s, %s)", (productid, review_user, dateTime, user))
                    db.commit()
                elif liked == 0 and disliked > 0:
                    # User heeft comment al gedisliked, dislike wordt verwijderd, like wordt toegevoegd
                    cursor.execute("DELETE FROM `Dislike` WHERE `Review_Product_id`=%s AND `Review_User_id`=%s AND `Review_dateTime`=%s AND `User_id`=%s", (productid, review_user, dateTime, user))
                    db.commit()
                    cursor.execute("INSERT INTO `Like` (`Review_Product_id`, `Review_User_id`, `Review_dateTime`, `User_id`) VALUES (%s, %s, %s, %s)", (productid, review_user, dateTime, user))
                    db.commit()

            start_response('303 See Other', [('Location', 'product.py?id=' + productid + '#reviews')])

        cursor.close()
        db.close()

    return [bytes(html, 'utf-8')]
