# instaleert dependencies (pyyaml, )
# start de bouw van de docker omgeving

import subprocess
import sys
import os

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
except:
    print('pip3 not installed, please install')

# start het launch script dat de docker-compose instantie start
print("All dependencies are installed, launching now")
if os.name == 'posix':
    # linux, probeer te runnen met sudo
    try:
        os.system('sudo python3 launch.py')
    except:
        print("sudo not installed, trying without sudo")

    try:
        os.system('python3 launch.py')
    except:
        print("Failed, possibly wrong permissions!")
else:
    # Windows / OSX
    os.system('python3 launch.py')
