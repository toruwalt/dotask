import calendar
from datetime import datetime
from dotask.models import User, Task,  user_task, Notification, user_notification
from dotask import login_manager, current_user, login_user, login_required, logout_user


class CustomHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, today=None):
        super().__init__()
        # Ensure that `self.today` is a datetime object
        self.today = today if isinstance(today, datetime) else datetime.now()

    def formatday(self, day, weekday, month, year):
        day_str = f'{day:02}'
        month_str = f'{month:02}'

        if current_user and current_user.tasks:
          for task in current_user.tasks:
              if task.due_date and str(task.due_date) != str(self.today.strftime('%Y-%m-%d')) and task.due_date.year == year and task.due_date.month == month and task.due_date.day == day:
                  # Apply background color if deadline matches
                  return f'<td id="deadline-day"><a href="/calendar/?year={year}&month={month_str}&day={day_str}">{day}</a></td>'


        if day == self.today.day and month == self.today.month and year == self.today.year:
            return f'<td id="today">{day}</td>'
        elif day != 0:
            return f'<td><a href="/calendar/?year={year}&month={month_str}&day={day_str}">{day}</a></td>'
        return '<td></td>'
    
    def formatweek(self, theweek, month, year):
        week_html = ''.join(self.formatday(d, wd, month, year) for (d, wd) in theweek)
        return f'<tr>{week_html}</tr>'

    def formatmonth(self, year, month, withyear=True):
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(year, month, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(year, month):
            a(self.formatweek(week, month, year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
