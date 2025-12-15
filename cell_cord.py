from ForCrashes import *

#индексация в файле с 1

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
        if (type(letters_or_number) == str):
            self.__letters_coord = convert_letters_to_numbers[letters_or_number]
        elif (type(letters_or_number) == int):
            self.__letters_coord = letters_or_number
        else:
            crush_message = "Косяк в CellCoord. Чё за тип вы передали в letters_or_number?"
            print_crush(crush_message, TypeError)


        if (type(number) == int):
            self.__number_coord = number
        else:
            crush_message = "Косяк в CellCoord. Чё за тип вы передали в number?"
            print_crush(crush_message, TypeError)

    def add_val_to_letters_coord(self, x):
        self.__letters_coord += x
        if (self.__letters_coord < 1):
            crush_message = "Косяк в CellCoord. letters_cord стал < 1. add_val_to_letters_coord"
            print(crush_message, IndexError)

    def add_val_to_number_coord(self, x):
        self.__number_coord += x
        if (self.__number_coord < 1):
            crush_message = "Косяк в CellCoord. letters_cord стал < 1. add_val_to_number_coord"
            print(crush_message, IndexError)

    def get_cell_address(self):
        return convert_numbers_to_letters[self.__letters_coord] + str(self.__number_coord)



