"""
the job of this service is to calculate teh new review date
"""
from datetime import datetime, timedelta, time, timezone
from zoneinfo import ZoneInfo

BASE_INTERVALS = [0, 1, 3, 7, 14, 28, 56, 112, 224, 365]

#Grabs the current interval of the flash and set's the next one depending on user choice
def calculate_next_interval(current_interval, decision):
    current_index = BASE_INTERVALS.index(current_interval)

    if current_index == len(BASE_INTERVALS) - 1:
        return current_interval
    if decision == "AGAIN":
        return BASE_INTERVALS[0]
    elif decision == "OK":
        return BASE_INTERVALS[current_index + 1]
    elif decision == "EASY":
        next_index = min(
            current_index + 2,
            len(BASE_INTERVALS) - 1
        )
        return BASE_INTERVALS[next_index]
    else:
        raise ValueError("Invalid decision")
"""
interval_days - number od days until the next review, will get it from calculate_next_interval
now = the current moment (datetime Obj)
timezone_name - name of the timezone the user is in
"""
def schedule_next_review(interval_days, now, timezone_name):
    #Gets the timezone rules for Dublin automatically, includes stuff like daylight-saving rules
    #(the string timezone_name is passed into the ZoneInfo object)
    user_timezone = ZoneInfo(timezone_name)


    #takes the current moment and expressesit in the user's timezone, so that we can calculate the next review date in the user's local time

    """
    If now is 18:30 UTC, for a User in Dublin that would be 19:30
    (Same time instant, changed representation)
    """
    local_now = now.astimezone(user_timezone)

    #If the user pressed "Again"
    if interval_days == 0:
        return now


    target_date = local_now.date() + timedelta(days=interval_days)
    #adds the 00:00 time to the target_date
    local_midnight = datetime.combine(target_date, time.min, tzinfo=user_timezone)

    #Returns eg. 2026-09-19 00:00 Europe/Dublin
    return local_midnight.astimezone(timezone.utc)

#Fuction that combines the results of the 2 previous functions and returns the result
def process_review(current_interval, decision, now, timezone_name):
    next_interval = calculate_next_interval(current_interval, decision)

    next_review_at = schedule_next_review(next_interval, now, timezone_name)

    return {
        "interval_days": next_interval,
        "next_review_at": next_review_at
    }






