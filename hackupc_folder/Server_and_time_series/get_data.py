import urllib.parse
import urllib.request
import zlib
from io import StringIO
import pandas as pd
import numpy as np
import datetime

yesterday=datetime.date.today()-datetime.timedelta(days=1)
yesterday=yesterday.strftime('%Y%m%d')

url = yesterday

print("Calling the script...")
import subprocess
subprocess.call(['./get_data.sh' + " " + url], shell=True)
