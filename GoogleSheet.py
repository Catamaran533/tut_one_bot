from googleapiclient.discovery import build
from google_token import *
from cell_coord import *
from cell import *


class Sheet:
    def __init__(self, spreadsheet_id: str, sheet_name: str, start_range: CellCoord, end_range: CellCoord):
        self.__cells = {}
        self.__spreadsheet_id = spreadsheet_id
        self.__sheet_name = sheet_name
        self.__start_range = start_range
        self.__end_range = end_range
        self.__download_data()

    def __download_data(self):
        try:
            creds = create_token()
            service = build('sheets', 'v4', credentials=creds)

            range_name = f"{self.__sheet_name}!{self.__start_range.get_cell_address()}:{self.__end_range.get_cell_address()}"

            # Наш запрос
            sheet = service.spreadsheets()
            result = sheet.get(
                spreadsheetId=self.__spreadsheet_id,
                ranges=[range_name],
                includeGridData=True
            ).execute()

            if 'sheets' in result and len(result['sheets']) > 0:
                sheet_data = result['sheets'][0]
                if 'data' in sheet_data and len(sheet_data['data']) > 0:
                    grid_data = sheet_data['data'][0]

                    start_row = grid_data.get('startRow', 0)
                    start_column = grid_data.get('startColumn', 0)

                    if 'rowData' in grid_data:
                        for row_index, row_data in enumerate(grid_data['rowData']):
                            if row_data is not None and 'values' in row_data:
                                for col_index, cell_data in enumerate(row_data['values']):
                                    if cell_data is not None:
                                        abs_row = start_row + row_index + 1
                                        abs_col = start_column + col_index + 1

                                        cell_coord = CellCoord(abs_col, abs_row)
                                        cell_address = cell_coord.get_cell_address()

                                        self.__cells[cell_address] = cell_data

            #print(f"Загрузил {len(self.__cells)} ячеек из листа '{self.__sheet_name}'")

        except Exception as e:
            print_crash(f"Ошибка при загрузке данных из Google Sheets: {e}")
            self.__cells = {}

    def get_cell_info(self, cell_coord: CellCoord):

        cell_address = cell_coord.get_cell_address()
        return self.__cells.get(cell_address)

    def get_cell(self, cell_coord: CellCoord) -> Cell:

        cell_data = self.get_cell_info(cell_coord)


        text = ""

        if cell_data:
            if 'formattedValue' in cell_data:
                text = cell_data['formattedValue']
            elif 'effectiveValue' in cell_data:
                eff_value = cell_data['effectiveValue']
                if 'stringValue' in eff_value:
                    text = eff_value['stringValue']
                elif 'numberValue' in eff_value:
                    text = str(eff_value['numberValue'])
                elif 'boolValue' in eff_value:
                    text = str(eff_value['boolValue'])
            elif 'userEnteredValue' in cell_data:
                user_value = cell_data['userEnteredValue']
                if 'stringValue' in user_value:
                    text = user_value['stringValue']
                elif 'numberValue' in user_value:
                    text = str(user_value['numberValue'])
                elif 'boolValue' in user_value:
                    text = str(user_value['boolValue'])


        color = ColorRGB()
        color1 = ColorRGB()
        color2 = ColorRGB()
        color3 = ColorRGB()
        color4 = ColorRGB()



        if cell_data:


            if 'effectiveFormat' in cell_data:
                eff_format = cell_data['effectiveFormat']
                if 'backgroundColor' in eff_format:
                    bg = eff_format['backgroundColor']
                    red = bg.get('red', 1.0)
                    green = bg.get('green', 1.0)
                    blue = bg.get('blue', 1.0)
                    color1 = ColorRGB(red, green, blue)
                elif 'backgroundColorStyle' in eff_format:
                    bg_style = eff_format['backgroundColorStyle']
                    if 'rgbColor' in bg_style:
                        rgb = bg_style['rgbColor']
                        red = rgb.get('red', 1.0)
                        green = rgb.get('green', 1.0)
                        blue = rgb.get('blue', 1.0)
                        color2 = ColorRGB(red, green, blue)



            elif 'userEnteredFormat' in cell_data:
                user_format = cell_data['userEnteredFormat']
                if 'backgroundColor' in user_format:
                    bg = user_format['backgroundColor']
                    red = bg.get('red', 1.0)
                    green = bg.get('green', 1.0)
                    blue = bg.get('blue', 1.0)
                    color3 = ColorRGB(red, green, blue)
                elif 'backgroundColorStyle' in user_format:
                    bg_style = user_format['backgroundColorStyle']
                    if 'rgbColor' in bg_style:
                        rgb = bg_style['rgbColor']
                        red = rgb.get('red', 1.0)
                        green = rgb.get('green', 1.0)
                        blue = rgb.get('blue', 1.0)
                        color4 = ColorRGB(red, green, blue)

        if (color1 != WHITE_COLOR):
            color = color1
        elif (color2 != WHITE_COLOR):
            color = color2
        elif (color3 != WHITE_COLOR):
            color = color3
        else:
            color = color4

        return Cell(cell_coord, text, color)



SPREADSHEET_ID = "1oGQz-SCHoGgO0b-B0PwbbuaLxjf1bnHBX9eQjiISphE"
SHEET_NAME = "актуальное"

START_RANGE = CellCoord('A', 1)
END_RANGE = CellCoord('CF', 70)


def get_school_table_sheet():
    return Sheet(SPREADSHEET_ID, SHEET_NAME, START_RANGE, END_RANGE)

SCHOOL_TABLE = get_school_table_sheet()


