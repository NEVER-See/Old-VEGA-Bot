import string, datetime

def string_to_seconds(string):
    total_seconds, number_string = 0, ''
    string = string.lower().strip('-')
    multi = 1
    units = {
        "s": 1,
        "с": 1,
        "m": 60,
        "м": 60,
        "h": 3600,
        "ч": 3600,
        "d": 86400,
        "д": 86400,
        "w": 604800,
        "н": 604800,
        "y": 31536000,
        "г": 31536000,
        "л": 31536000
    }
    for char in string:
        if char.isdigit():
            number_string += char
        else:
            try:
                multi = units[char]
            except KeyError:
                multi = 1
            try:
                total_seconds += int(number_string) * multi
            except:
                pass
            number_string = ''
    if total_seconds < 0:
        total_seconds = 0
    return total_seconds

def word_correct(number: int, p1, p2, p3):
    number = str(number)
    ld = number[-2:]
    cases = {
        "0": "p3",
        "1": "p1",
        "2": "p2",
        "3": "p2",
        "4": "p2",
        "5": "p3",
        "6": "p3",
        "7": "p3",
        "8": "p3",
        "9": "p3"
    }
    if ld[0] == "1" and len(ld) > 1:
        case = "p3"
    else:
        if len(ld) == 1:
            case = cases[ld[0]]
        else:
            case = cases[ld[1]]

    words = {
        "p1": p1,
        "p2": p2,
        "p3": p3
    }
    return words[case]
def hms(sec: float):
    d = int(sec // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)
    
    if h > 0:
        display_h = f'{h} {word_correct( h, "час", "часа", "часов" )} '
    else:
        display_h = ''

    if m > 0:
        display_m = f'{m} {word_correct( m, "минута", "минуты", "минут" )} '
    else:
        display_m = ''

    if s > 0:
        display_s = f'{s} {word_correct(s, "секунда", "секунды", "секунд" )}'
    else:
        display_s = ''

    if sec < 1:
        return f'{ms} {word_correct( ms, "миллисекунда", "миллисекунды", "миллисекунд" )}'
    elif sec < 60:
        return f'{s} {word_correct( s, "секунда", "секунды", "секунд" )}'
    elif sec < 3600:
        return f'{m} {word_correct( m, "минута", "минуты", "минут" )} {display_s}'
    elif sec < 86400:
        return f'{h} {word_correct( h, "час", "часа", "часов" )} {display_m}{display_s}'
    else:
        return f'{d} {word_correct( d, "день", "дня", "дней" )} {display_h}{display_m}{display_s}'

def hms2(sec: float):
    d = int(sec // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)
    
    if h > 0:
        display_h = f'{h} {word_correct( h, "час", "часа", "часов" )} '
    else:
        display_h = ''

    if m > 0:
        display_m = f'{m} {word_correct( m, "минуту", "минуты", "минут" )} '
    else:
        display_m = ''

    if s > 0:
        display_s = f'{s} {word_correct(s, "секунду", "секунды", "секунд" )}'
    else:
        display_s = ''

    if sec < 1:
        return f'{ms} {word_correct( ms, "миллисекунду", "миллисекунды", "миллисекунд" )}'
    elif sec < 60:
        return f'{s} {word_correct( s, "секунду", "секунды", "секунд" )}'
    elif sec < 3600:
        return f'{m} {word_correct( m, "минуту", "минуты", "минут" )} {display_s}'
    elif sec < 86400:
        return f'{h} {word_correct( h, "час", "часа", "часов" )} {display_m}{display_s}'
    else:
        return f'{d} {word_correct( d, "день", "дня", "дней" )} {display_h}{display_m}{display_s}'

def oneof(string, list):
    found = False
    for l in list:
        if l in string.lower():
            found = True
            break
    return found, l

def ishs(string1):
    string1 = string1.lower()
    return oneof(string1, list('smhdwyсмчднгл'))[0] and oneof(string1, [str(n) for n in string.digits])[0]

def ago(dt):
    days = (datetime.datetime.now() - dt).days
    if days >= 365:
        d = f'{days//365} {word_correct(days//365, "год", "года", "лет")} назад'
    elif days >= 30:
        d = f'{days//30} {word_correct(days//30, "месяц", "месяца", "месяцев")} назад'
    elif days >= 7:
        d = f'{days//7} {word_correct(days//7, "неделю", "недели", "недель")} назад'
    elif days > 1:
        d = f'{days} {word_correct(days, "день", "дня", "дней")} назад'
    elif days == 1:
        d = 'вчера'
    elif days == 0:
        d = 'сегодня'
    return d