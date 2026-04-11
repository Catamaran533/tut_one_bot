from consts import *
BAD_SYMBOLS = [";", "(", ")", "+", "->", "<-", ","]

def get_teachers(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    teachers = []
    for i in text:
        only_letters = ''.join([c for c in i if c.isalpha() or c.isnumeric()])
        if len(only_letters) == 0:
            continue
        if only_letters[0].isupper():
            only_letters = only_letters.lower()
            if only_letters in MAP_WITH_TEACHERS_NAMES.keys():
                teachers.append(only_letters)
            elif only_letters in MAP_WITH_TEACHERS_ABBREVIATION.keys() and i.endswith('.'):
                teachers.append(MAP_WITH_TEACHERS_ABBREVIATION[only_letters])
    return teachers


def get_lesson(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    lesson_list = []
    for i in text:
        only_letters = ''.join([c for c in i if c.isalpha() or c.isnumeric()])
        if len(only_letters) == 0:
            continue
        if only_letters[0].isupper():
            only_letters = only_letters.lower()
            if only_letters in MAP_WITH_TEACHERS_NAMES.keys():
                break
            elif only_letters in MAP_WITH_TEACHERS_ABBREVIATION.keys() and i.endswith('.'):
                break
        lesson_list.append(i)
    lesson = ""
    for i in lesson_list:
        lesson += i + " "
    lesson = lesson.rstrip()
    return lesson

BAD_SYMBOLS_FOR_CABS = BAD_SYMBOLS + ["."]
allowed_cabs = ['зал']
def get_cabs(text: str):
    for i in BAD_SYMBOLS:
        text = text.replace(i, ' ')
    text = text.split()
    ans = []
    for i in text:
        if (i.isdigit()) or i in allowed_cabs:
            ans.append(i)
        else:
            only_letters = ''.join([c for c in i if c.isalpha()])
            only_letters = only_letters.lower()
            if only_letters in ["шк", "школа"]:
                ans.append("школа")
            if only_letters == "лицей":
                ans.append("лицей")
    ans1 = []
    for i in range(len(ans)):
        if i == 0:
            ans1.append(ans[i])
            continue
        if ans[i - 1] in ["шк", "школа", "лицей"]:
            ans1[len(ans1) - 1] += " " + ans[i]
        else:
            ans1.append(ans[i])

    ans2 = []
    for i in ans1:
        if i.isdigit() and len(i) != 3:
            continue
        ans2.append(i)

    if len(ans2) == 0:
        ans2 = ["не известно."]
    return ans2
