import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_token
from GoogleSheet import *


a = SCHOOL_TABLE.get_cell(CellCoord('E', 11))
b = SCHOOL_TABLE.get_cell(CellCoord('E', 12))
print(a.get_color(), b.get_color())
print([a.get_text(), b.get_text()])



