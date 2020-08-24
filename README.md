# SJTU Timetable Generator


This is a semi-automated program for automatically export class table into calendar events.

This script requires you to grab data yourself.

And I referred to [sjtu-class-table-generator](https://github.com/skyzh/sjtu-class-table-generator) and [CalenderGenerator](https://github.com/Zxilly/CalenderGenerator) in the process.

## Main Step to Use it

###  1. Grab Timetable Date


1. Visit https://i.sjtu.edu.cn/

2. 信息查询 - 学生课表查询

3. In `Developer Tools`, find request with URL like `https://i.sjtu.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm={...}&su={...}`

4. Paste all data to `data.json`. It should be like:

   ```json
   {
       "kblx": 7,
       "xqbzxxszList": [],
       "xsxx": {
   		......
       },
       "sjkList": [],
       "xkkg": true,
       "xqjmcMap": {
           "1": "星期一",
           "2": "星期二",
           "3": "星期三",
           "4": "星期四",
           "5": "星期五",
           "6": "星期六",
           "7": "星期日"
       },
       "xskbsfxstkzt": "0",
       "kbList": [
           {
            ...
               "kcmc": "电路与电子学",
               ...
           }
           ...
       ]
   ```

   

### 	2. Change Some Parameters

1. semester_start_day     (line 61)      # The date of the beginning of the term

2. cal['prodid']                   (line 98)     #  This property specifies the identifier for the product that created the iCalendar object.



### 3. Run Program

Run the SJTU_timetable_generator.py 



### 4. Import to Calendar

Drag and drop `Curricular for {Your name}.ics` into your calendar app.



## Note

  I have only generated the timetable successfully with my own `data.json`. So if you find any porblem, please contact me through email.
