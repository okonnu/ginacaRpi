import os
import subprocess

def cleanchrome():
    os.chmod("cleanchrome.sh", 509)
    rc = subprocess.call("./cleanchrome.sh")
