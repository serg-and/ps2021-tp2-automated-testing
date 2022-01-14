# creert random usernames en wachtwoorden voor de databases
# plaatst deze credentials in de docker-compose file
# voegt deze credentials toe aan de secrets bestanden

import os
import secrets
import yaml
import json

# credentials voor website database
db_usr = secrets.token_urlsafe(32)
db_passw = secrets.token_urlsafe(32)
db_root_passw = secrets.token_urlsafe(32)
db_login = {"MYSQL_ROOT_PASSWORD": db_root_passw, "MYSQL_USER": db_usr, "MYSQL_PASSWORD": db_passw}

# credentials voor papa database
papa_usr = secrets.token_urlsafe(32)
papa_passw = secrets.token_urlsafe(32)
papa_root_passw = secrets.token_urlsafe(32)
papa_login = {"MYSQL_ROOT_PASSWORD": papa_root_passw, "MYSQL_USER": papa_usr, "MYSQL_PASSWORD": papa_passw}

# plaatst de gegenereerde login credentials in docker-compose.yml
with open('docker-compose.yml') as stream:
    data = yaml.safe_load(stream)

# update website database variabelen
for key in db_login:
    data['services']['mysql']['environment'][key] = db_login[key]
# update papa database variabelen
for key in papa_login:
    data['services']['papa']['environment'][key] = papa_login[key]

with open('docker-compose.yml', 'wb') as stream:
    yaml.safe_dump(data, stream, default_flow_style=False, explicit_start=True, allow_unicode=True, encoding='utf-8')

# plaatst de gegenereerde login credentials in de behoorende json secret file
out_file = open("./secrets/db_login.json", "w")
json.dump(db_login, out_file, indent=4)
out_file.close()

out_file = open("./secrets/papa_login.json", "w")
json.dump(papa_login, out_file, indent=4)
out_file.close()

# start docker-compose instantie
if os.name == 'posix':
    # linux, probeer te runnen met sudo
    try:
        os.system('sudo docker-compose up --build')
    except:
        print("sudo not installed, trying without sudo")

    try:
        os.system('docker-compose up --build')
    except:
        print("Failed, possibly wrong permissions!")
else:
    # Windows / OSX
    os.system('docker-compose up --build')
