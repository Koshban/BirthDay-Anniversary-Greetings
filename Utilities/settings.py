""" SetUp various central variables"""
import os
import subprocess
import sys
from datetime import datetime

""" SetUp Paths"""
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
username = ''  # your Windows User Id under  C:\Users\{userid}

""" Scaling Factor of your screen, you might have to figure it out yourself
    Use currentMouseX, currentMouseY = pyautogui.position()
    print(currentMouseX, currentMouseY)
    while putting your cursor on the WhatsApp Web Message Bar to get what exactly you will need"""
sfw, sfh = 0.58, 0.914

"""If you are using Google Sheets Instead of .csv"""
use_google_sheet = False  # Not enabled yet, will be done in next iteration
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '' # spreadSheet ID of your G Sheet
SAMPLE_RANGE_NAME = '{0}!A1:G100'  # Change Range if you have lot more names
tab_names = [""]

if os.name == 'nt':
    log_file = f"{BASE_DIR}\\logfile.txt"
    util_dir = f"{BASE_DIR}\\Utilities"
    names_file = f"{util_dir}\\names.csv"
    today_date = datetime.today().strftime('%#m%d %H:%M')  # #m on Windows and -m on Linux

else:
    log_file = f"{BASE_DIR}/logfile.txt"
    util_dir = f"{BASE_DIR}/Utilities"
    names_file = f"{BASE_DIR}/names.csv"
    today_date = datetime.today().strftime('%-m%d %H:%M:%S')  # #m on Windows and -m on Linux
    my_sub_process = subprocess.run(f"mkdir -p {util_dir}", shell=True, text=True, capture_output=True)
    if my_sub_process.returncode != 0:
        print(f'Unable to create Directory , please check : {util_dir}. Create manually if required.')
        sys.exit()