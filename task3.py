from flask import Flask

app = Flask(__name__)


@app.route('/')
def appearance_web_api():
    answers_dict = {}
    for i, test in enumerate(tests):
        answer = appearance(test['data'])
        answers_dict[i + 1] = answer
    return answers_dict


def appearance(intervals):
    lesson = intervals.get('lesson')
    pupil = refactoring(intervals.get('pupil'), lesson)
    tutor = refactoring(intervals.get('tutor'), lesson)
    pupil_ranges = make_ranges(pupil)
    tutor_ranges = make_ranges(tutor)
    together_time_list = []
    check = []
    check += pupil
    check += tutor
    for time in check:  # если time есть в диапазоне присутствия ученика и учителя, то оно добавляется в список
        pupil_result = check_etering(time, pupil_ranges)
        tutor_result = check_etering(time, tutor_ranges)
        if pupil_result and tutor_result:
            together_time_list.append(time)
    print(together_time_list)
    together_time_list.sort()  # сортируем список для того, чтобы числа встали правильно на числовой прямой
    together_time = 0
    for i in range(1, len(together_time_list), 2):
        time_delta = together_time_list[i] - together_time_list[i - 1]
        together_time += time_delta
    return together_time


def make_ranges(intervals):  # создание "диапазонов присутствия" для дальнешей работы с ними
    range_list = []
    for i in range(1, len(intervals), 2):
        range_list.append(range(intervals[i - 1], intervals[i] + 1))

    return range_list


def check_etering(time, ranges):  # функция проверки вхождения во все инервалы присутствия определенного времени time
    for t in ranges:
        if time in t:
            return True


# в эту  функцию мы передаем время начало и конца урока, а также списки с временем входа и выхода
# и эта функция укорачивает интервал присутствия человека на платформе, если он был на ней дольше, чем длился урок
def refactoring(interval, lesson):
    refactoring_list = []
    start_lesson = lesson[0]
    stop_lesson = lesson[1]
    lesson_range = range(start_lesson, stop_lesson + 1)
    for i in range(1, len(interval), 2):
        if interval[i - 1] in lesson_range:
            if interval[i] in lesson_range:
                refactoring_list.append(interval[i - 1])
                refactoring_list.append(interval[i])
            else:
                if interval[i] >= stop_lesson:
                    refactoring_list.append(interval[i - 1])
                    refactoring_list.append(stop_lesson)
        else:
            if interval[i - 1] <= start_lesson:
                if interval[i] in lesson_range:
                    refactoring_list.append(start_lesson)
                    refactoring_list.append(interval[i])
                elif interval[i] >= stop_lesson:
                    refactoring_list.append(start_lesson)
                    refactoring_list.append(stop_lesson)
    return refactoring_list


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    app.run(debug=True)
