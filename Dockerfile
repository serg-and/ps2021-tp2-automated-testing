FROM httpd:2.4-alpine
RUN apk add apache2-mod-wsgi
RUN apk add py3-mysqlclient
RUN apk add py3-bcrypt
RUN apk add py3-six
RUN apk add py3-cffi
COPY \public_html\ /usr/local/apache2/htdocs/
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
