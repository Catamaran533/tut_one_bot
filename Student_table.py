from cell import *
from SplittingDays import *
from StudentLesson import *

# TODO переделать ВСЁ

HORIZONTAL_TABLE_SIZE = 4
MAX_LESSONS_PER_DAY = 8


for i in get_day("5мл", "ПН"):
    for j in i:
        print(j, end=" ")
        print()
    print()