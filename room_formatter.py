def format_rooms(lesson_rooms):
    if not lesson_rooms:
        return "не известно."
    room_numbers = []
    school_rooms = []
    i = 0
    while i < len(lesson_rooms):
        item = str(lesson_rooms[i]).strip()
        if item.isdigit() and len(item) == 3:
            room_numbers.append(item)
        elif item.lower() == 'школа' and i + 1 < len(lesson_rooms):
            next_item = str(lesson_rooms[i + 1]).strip()
            if next_item.isdigit():
                school_rooms.append(f"школа {next_item}")
                i += 1
        i += 1
    if school_rooms:
        return ', '.join(school_rooms)
    if room_numbers:
        return ', '.join(room_numbers)
    return "не известно."