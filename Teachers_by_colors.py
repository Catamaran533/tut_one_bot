from ForCrashes import *
from consts import *
from GoogleSheet import *
from SplittingDays import get_day

BAD_SYMBOLS = [";", ":", "()", "+", "->", "<-"]
DAYS_OF_THE_WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
CLASSES = ["5мл", "6мл", "7мл", "8м", "9м", "10м", "11м", "8хб", "9хб", "10хб", "11хб", "8г", "9г", "10г", "11г"]
MAX_LESSONS_PER_DAY = 8

def get_teachers_in_string(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    teachers = []
    for i in text:
        only_letters = ''.join([c for c in i if c.isalpha()])
        if (len(only_letters) == 0):
            continue
        if only_letters[0].isupper():
            only_letters = only_letters.lower()
            if only_letters in MAP_WITH_TEACHERS_NAMES.keys():
                teachers.append(only_letters)
            elif only_letters in MAP_WITH_TEACHERS_ABBREVIATION.keys():
                teachers.append(MAP_WITH_TEACHERS_ABBREVIATION[only_letters])
    return teachers





def get_teachers_and_colors():

    global SHEET_NAME, SCHOOL_TABLE

    SHEET_NAME = "постоянное"                   #конечно плохо константы менять, но я буду, хотя мне эта идея не нравится
    SCHOOL_TABLE = get_school_table_sheet()
    colors_and_teachers = []
    for class_name in CLASSES:
        for day_of_the_week in DAYS_OF_THE_WEEK:
            l = get_day(class_name, day_of_the_week)
            for i in range(MAX_LESSONS_PER_DAY):
                for j in [0, 2]:
                    teachers = get_teachers_in_string(l[i][j].get_text())
                    color = l[i][j].get_color()
                    if len(teachers) == 1:
                        for k in colors_and_teachers:
                            if (k[0] == color):
                                break
                        else:           #Да, это else к циклу))))))))
                            colors_and_teachers.append([color, teachers[0]])


    SHEET_NAME = "актуальное"
    SCHOOL_TABLE = get_school_table_sheet()


    return colors_and_teachers

COLORS_AND_TEACHERS = []
#COLORS_AND_TEACHERS = get_teachers_and_colors()
#for i in COLORS_AND_TEACHERS:
#    print("[", str(i[0]).ljust(50), ', "', i[1], '"],', sep="")

def have_color(color: ColorRGB):
    for i in COLORS_AND_TEACHERS:
        if i[0] == color:
            return True
    return False

def get_teacher_by_color(color: ColorRGB):
    for i in COLORS_AND_TEACHERS:
        if i[0] == color:
            return i[1]
    print_crash("попытка получить учителя по несуществующему цвету")
    return "BUG"


COLORS_AND_TEACHERS = [
    [ColorRGB(0.7411765, 0.7411765, 0.003921569), "данилова"],
    [ColorRGB(0.18039216, 0.48235294, 0.75686276), "минаева"],
    [ColorRGB(0.5686275, 0.54509807, 0.10980392), "левина"],
    [ColorRGB(1.0, 0.6392157, 0.2901961), "никифорова"],
    [ColorRGB(0.011764706, 0.16862746, 0.30980393), "цейтлин"],
    [ColorRGB(0.40784314, 0.20392157, 0.12156863), "коваленко"],
    [ColorRGB(1, 0.4, 1.0), "теслер"],
    [ColorRGB(0.07058824, 0.84313726, 0.011764706), "спицкая"],
    [ColorRGB(1, 0.43529412, 1), "абакумова"],
    [ColorRGB(0.6156863, 0.85490197, 0.5058824), "ершова"],
    [ColorRGB(0.21568628, 0.93333334, 0.7137255), "зиннурова"],
    [ColorRGB(1.0, 1.0, 1.0), "костюченко"],
    [ColorRGB(0.85882354, 0.5372549, 0.09019608), "шайдуров"],
    [ColorRGB(0.7607843, 0.48235294, 0.627451), "лужбинина"],
    [ColorRGB(0.45490196, 0.105882354, 0.2784314), "красоткина"],
    [ColorRGB(0.7058824, 0.654902, 0.8392157), "петерс"],
    [ColorRGB(0.91764706, 0.7607843, 0.8392157), "абросимова"],
    [ColorRGB(0.37254903, 0.8980392, 0.8980392), "бабакин"],
    [ColorRGB(0.57254905, 0.8039216, 0.8627451), "ремнёв"],
    [ColorRGB(0.8, 0.6, 1), "облендер"],
    [ColorRGB(0.7882353, 0.972549, 0.9490196), "антипов"],
    [ColorRGB(0.7058824, 0.37254903, 0.023529412), "щавелев"],
    [ColorRGB(0.4, 0.4, 0.6), "кузнецова"],
    [ColorRGB(0.83137256, 0.94509804, 0.19607843), "пронин"],
    [ColorRGB(0.21960784, 0.4627451, 0.11372549), "макарова"],
    [ColorRGB(0.70980394, 0.15686275, 0.70980394), "кряжева-чёрная"],
    [ColorRGB(0.94509804, 0.7607843, 0.19607843), "порецкий"],
    [ColorRGB(0.6, 1, 0.2), "пичугина"],
    [ColorRGB(0.6862745, 0.19215687, 0.03529412), "андрианова"],
    [ColorRGB(0.02745098, 0.2784314, 0.2784314), "михайлова"],
    [ColorRGB(0.32941177, 0.5529412, 0.83137256), "иванова"],
    [ColorRGB(0.16470589, 0.6666667, 0.5411765), "борзенкова"],
    [ColorRGB(0.95686275, 0.16078432, 1.0), "маковеев"],
    [ColorRGB(0.8980392, 0.45882353, 0.45882353), "клюев"],
    [ColorRGB(0.78431374, 0.29411766, 0.16470589), "богданова"],
    [ColorRGB(0.8352941, 0.6509804, 0.7411765), "раев"],
    [ColorRGB(1.0, 0.2, 1.0), "битюкова"],
    [ColorRGB(0.3764706, 1.0, 0.5019608), "прадун"],
    [ColorRGB(0.40392157, 0.30588236, 0.654902), "вдовиченко"],
    [ColorRGB(1.0, 0.5019608, 0.5019608), "артамонова"],
    [ColorRGB(0.5019608, 1.0, 1.0), "тишунин"],
    [ColorRGB(0.72156864, 0.1764706, 0.44705883), "туманова"],
    [ColorRGB(0.8, 1.0, 1.0), "прохоренко"],
    [ColorRGB(0.8509804, 0.8509804, 0.8509804), "иванов"],
    [ColorRGB(0.63529414, 0.76862746, 0.7882353), "холодилов"],
    [ColorRGB(1, 0.3764706, 0.3764706), "нанобашвили"],
    [ColorRGB(0.6, 1.0, 1), "пуеров"],
    [ColorRGB(0.41568628, 0.65882355, 0.30980393), "горных"],
    [ColorRGB(1, 0.6509804, 0.6509804), "теслер"],
    [ColorRGB(0.9882353, 0.8980392, 0.8039216), "рожков"],
    [ColorRGB(0.7137255, 0.84313726, 0.65882355), "александрова"],
    [ColorRGB(1, 0.7254902, 0.69803923), "травникова"],
    [ColorRGB(0.043137256, 0.2784314, 0.49019608), "крылова"],
    [ColorRGB(0.4, 0.4, 0.4), "дивенков"],
    [ColorRGB(1, 1, 0.6), "тарабукина"],
    [ColorRGB(0.2, 0.6, 0.4), "соловьева"]
]