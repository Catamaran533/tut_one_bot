'''import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow'''
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_token
import consts
from ForCrashes import *




class ColorRGB:
    def __init__(self, red=1.0, green=1.0, blue=1.0):
        self.__red = red
        self.__green = green
        self.__blue = blue


    def get_red(self):
        return self.__red
    def set_red(self, new_red):
        self.__red = new_red

    def get_green(self):
        return self.__green
    def set_green(self, new_green):
        self.__green = new_green

    def get_blue(self):
        return self.__blue
    def set_blue(self, new_blue):
        self.__blue = new_blue


    def __eq__(self, other):                #==
        colors = [self.__red, self.__green, self.__blue]
        other_colors = [other.get_red(), other.get_green(), other.get_blue()]
        for i in range(len(colors)):
            if abs(colors[i] - other_colors[i]) > consts.EPSILON:
                return False
        return True


    def __ne__(self, other):                #!=
        colors = ColorRGB(self.__red, self.__green, self.__blue)
        return not (colors == other)






#cell_address - строка, обозначающая позицию ячейки в гугл-таблице, например, "A1"
class Cell:
    def __init__(self, cell_address, spreadsheet_id = consts.SPREADSHEET_ID, sheet_name = consts.SHEET_NAME):
        try:                                        #Беру креды и радиус работы
            creds = google_token.create_token()
            service = build("sheets", "v4", credentials=creds)

            # Запрашиваю данные в ячейке
            response = service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                ranges=[f"{sheet_name}!{cell_address}"],
                includeGridData=True
            ).execute()
        except HttpError:
            crash_message = "Проверить доступ к Google Cloud Console, косяк в cell.py."
            print_crush(crash_message)
            raise HttpError

        try:
            cell = response['sheets'][0]['data'][0]['rowData'][0]['values'][0]
            text = cell.get('formattedValue', '')

            # Цвет фона (по умолчанию белый), get просто на всякий пожарный стоит

            background = cell.get('effectiveFormat', {}).get('backgroundColor', {})

            color = ColorRGB(background.get('red', 1.0), background.get('green', 1.0), background.get('blue', 1.0))

            self.__text = text
            self.__color = color
        except IndexError:
            crash_message = f"Накосячил в модуле cell.py, проверить структуру ячейки, вышел за границы списка."
            print_crush(crash_message)
            raise IndexError
        except KeyError:
            crash_message = f"Накосячил в модуле cell.py, проверить структуру ячейки, обратился к несуществующему ключу."
            print_crush(crash_message)
            raise KeyError


    def get_text(self):
        return self.__text
    def set_text(self, new_text):
        self.__text = new_text

    def get_color(self):
        return self.__color
    def set_color(self, new_color):
        self.__color = new_color