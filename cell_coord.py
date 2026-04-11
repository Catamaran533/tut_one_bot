from ForCrashes import *

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COUNT_ENGLISH_LETTERS = len(ENGLISH_ALPHABET)
convert_letters_to_numbers = dict()

cnt = 1
for i in ENGLISH_ALPHABET:
    convert_letters_to_numbers[i] = cnt
    cnt += 1

for i in ENGLISH_ALPHABET:
    for j in ENGLISH_ALPHABET:
        convert_letters_to_numbers[i + j] = cnt
        cnt += 1

convert_numbers_to_letters = dict()
for i in convert_letters_to_numbers.keys():
    convert_numbers_to_letters[convert_letters_to_numbers[i]] = i


class CellCoord:
    def __init__(self, letters_or_number, number):
        if isinstance(letters_or_number, str):
            self.__letters_coord = convert_letters_to_numbers[letters_or_number]
        elif isinstance(letters_or_number, int):
            self.__letters_coord = letters_or_number
        else:
            crush_message = f"Косяк в CellCoord. Чё за тип вы передали в letters_or_number? {letters_or_number}"
            print_crash(crush_message)
            self.__letters_coord = 1

        if isinstance(number, int):
            self.__number_coord = number
        else:
            crush_message = f"Косяк в CellCoord. Чё за тип вы передали в number? {number}"
            print_crash(crush_message)
            self.__number_coord = 1

    def add_val_to_letters_coord(self, x):
        self.__letters_coord += x
        if self.__letters_coord < 1:
            crush_message = "Косяк в CellCoord. letters_cord стал < 1. add_val_to_letters_coord"
            print_crash(crush_message)
        return self

    def add_val_to_number_coord(self, x):
        self.__number_coord += x
        if self.__number_coord < 1:
            crush_message = "Косяк в CellCoord. number_coord стал < 1. add_val_to_number_coord"
            print_crash(crush_message)
        return self

    def get_cell_address(self):
        if self.__letters_coord < 1 or self.__number_coord < 1:
            crush_message = "Косяк в CellCoord. letters_coord или number_coord стал < 1. get_cell_address"
            print_crash(crush_message)
            return "ERROR"
        return convert_numbers_to_letters[self.__letters_coord] + str(self.__number_coord)

    def get_letters_coord(self):
        return self.__letters_coord

    def get_numbers_coord(self):
        return self.__number_coord

    def copy(self):
        return CellCoord(self.__letters_coord, self.__number_coord)

    def __str__(self):
        return self.get_cell_address()