import datetime

wage = 13.13

class Shift:
    """
    Shift Class
    - The date of the shift
    - clock in time
    - clock out time
    - total number of hours worked that day
    - the amount of pay for that day
    """

    def __init__(self, date, start, end):
        self.date = date
        self.start_time = start
        self.end_time = end

    def get_shift(self):
        s = '{} at {}'
        date = str(self.date.month) + '-' + str(self.date.day) + '-' + str(self.date.year)

        start = self.start_time
        end = self.end_time
        time_frame = str(self.start_time) + ' - ' + str(self.end_time)

        if self.end_time.hour > self.start_time.hour:
            if self.end_time.hour > 12:
                hour = self.end_time.hour - 12
                time_frame = str(self.start_time) + ' - ' + str(datetime.time(hour, self.end_time.minute))

        if (self.start_time.hour > 12) and (self.end_time.hour > 12):
            start = self.start_time - 12
            end = self.end_time - 12
            time_frame = str(datetime.time(start, self.start_time.minute)) + ' - ' + str(datetime.time(end, self.end_time.minute))

        return s.format(date, time_frame)
    
    def get_hours(self):
        return (self.end_time.hour - self.start_time.hour) + (self.end_time.minute - self.start_time.minute)/60

    def calculate_pay(self):
        return round(self.get_hours() * wage, 2)