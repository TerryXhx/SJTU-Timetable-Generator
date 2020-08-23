import json
import icalendar
import re
from datetime import timedelta, datetime
from uuid import uuid1

def week_info_processing(week_range,dividend,remainder):
    if week_range.isdigit():
        return [int(week_range)]
    else:
        start_week = int(week_range.split('-')[0])
        end_week = int(week_range.split('-')[1])
        return list(filter(lambda x: x % dividend == remainder, range(start_week, end_week + 1)))


def parse_week_string(week_string):
    res = re.match('^(\d+)-(\d+)周(\((单|双)\))?$',week_string)
    if res:
        return list(range(int(res[1]),int(res[2]) + 1,2 if res[3] else 1))
    else:
        return [int(week) for week in week_string.replace('周','').split(',')]


data_path = "data.json"

ONE_COURSE = timedelta(minutes=45)
ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(weeks=1)

day_dict = {
    '星期日': 0,
    '星期一': 1,
    '星期二': 2,
    '星期三': 3,
    '星期四': 4,
    '星期五': 5,
    '星期六': 6,
}

course_time_dict = {
    1:  timedelta(hours=8,  minutes=0),
    2:  timedelta(hours=8,  minutes=55),
    3:  timedelta(hours=10, minutes=0),
    4:  timedelta(hours=10, minutes=55),
    5:  timedelta(hours=12, minutes=00),
    6:  timedelta(hours=12, minutes=55),
    7:  timedelta(hours=14, minutes=0),
    8:  timedelta(hours=14, minutes=55),
    9:  timedelta(hours=16, minutes=0),
    10: timedelta(hours=16, minutes=55),
    11: timedelta(hours=18, minutes=0),
    12: timedelta(hours=18, minutes=55),
    13: timedelta(hours=19, minutes=35),
    14: timedelta(hours=20, minutes=15)
}

if __name__ == '__main__':
    file = open(data_path, encoding='UTF-8')
    data = json.load(file)

    semester_start_day = datetime(2020,9,7)
    stu_name = data['xsxx']['XM']
    course_info = data['kbList']

    parsed_course_data = []

    for i in course_info:
        name = i['kcmc']
        id = i['jxbmc'].split('-')[3]
        credit = i['xf']
        teacher = i['xm']

        week_str = i['zcd']
        weeks = parse_week_string(week_str)
        day = day_dict[i['xqjmc']]
        period = i['jc'][:-1].split('-')
        start_time = int(period[0])
        end_time = int(period[1])
        location = i['cdmc']
        note = i['xkbz']

        parsed_one_course_data = {
            'id': id,
            'name': name,
            'credit': credit,
            'teacher': teacher,
            'location': location,
            'weeks': weeks,
            'day': day,
            'period': [start_time, end_time],
            'note': note
        }
        parsed_course_data.append(parsed_one_course_data)
    file.close()

    cal = icalendar.Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//TerryXhx//SJTU_Calender//CN'
    cal['X-WR-TIMEZONE'] = 'Asia/Shanghai'
    cal['X-WR-CALNAME'] = '课表'

    for course in parsed_course_data:
        for week in course['weeks']:
            date = semester_start_day + (week - 1) * ONE_WEEK + (course['day'] - 1) * ONE_DAY
            start_datetime = date + course_time_dict[course['period'][0]]
            end_datetime = date + course_time_dict[course['period'][1]] + ONE_COURSE
            print(course['name'], start_datetime, end_datetime)
            event = icalendar.Event()
            event.add('summary','{}.{}'.format(course['id'],course['name']))
            event.add('uid',str(uuid1()) + '@SJTU')
            event.add('dtstart',start_datetime)
            event.add('dtend',end_datetime)
            event.add('location',course['location'])
            event.add('description','任课教师:{}\r\n学分:{}\r\n备注:{}'.format(course['teacher'], course['credit'], course['note']))
            cal.add_component(event)

    with open('Curricular for {}.ics'.format(stu_name),'wb') as ics:
        ics.write(cal.to_ical())

