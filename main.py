import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_token
import cell
import cell_cord

a = cell_cord.CellCoord(1, 1)

print(a.get_cell_address())

b = cell.Cell(cell_cord.CellCoord(1, 1))

print(b.get_text())