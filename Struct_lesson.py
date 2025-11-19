class Lesson:
    def __init__(self, number, subject, teachers, rooms):
        self.__number = number
        self.__subject = subject
        self.set_teachers(teachers)
        self.set_rooms(rooms)
    def get_number(self):
        return self.__number
    def set_number(self, new_number):
        self.__number = new_number
    def get_subject(self):
        return self.__subject
    def set_subject(self, new_subject):
        self.__subject = new_subject
    def get_teachers(self):
        return self.__teachers
    def set_teachers(self, new_teachers):
        if isinstance(new_teachers, str): # Если строка (например, "зачиняев")
            self.__teachers = [new_teachers]
        elif isinstance(new_teachers, list): # Если список (["зачиняев", "абакумова"])
            self.__teachers = new_teachers
        else:
            self.__teachers = []
    def get_rooms(self):
        return self.__rooms
    def set_rooms(self, new_rooms): # тут тоже самое
        if isinstance(new_rooms, str):
            self.__rooms = [new_rooms]
        elif isinstance(new_rooms, list):
            self.__rooms = new_rooms
        else:
            self.__rooms = []
    def add_teacher(self, teacher_name): # добавить учителя к предмету
        if teacher_name not in self.__teachers:
            self.__teachers.append(teacher_name)
    def add_room(self, room_number): # добавить кабинет к предмету
        if room_number not in self.__rooms:
            self.__rooms.append(room_number)

def null_lesson():
    return Lesson(-1, "Нет урока", [], [])