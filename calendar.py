import datetime
import sqlite3

def save_event(name, day, hour_starts, hour_finish):
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM events")
    except Exception:
        cursor.execute("CREATE TABLE events (name VARCHAR(255), day VARCHAR(255), hour_starts VARCHAR(255), hour_finish VARCHAR(255))")

    day = day.split("-")
    day = str(datetime.date(int(day[0]),int(day[1]),int(day[2])))

    cursor.execute("INSERT INTO events VALUES (:name, :day, :hour_starts, :hour_finish)", {"name": name, "day": day, "hour_starts": hour_starts, "hour_finish": hour_finish})

    connection.commit()
    cursor.close()


def show_events_near():
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM events")
    except Exception:
        cursor.execute("CREATE TABLE events (name VARCHAR(255), day VARCHAR(255), hour_starts VARCHAR(255), hour_finish VARCHAR(255))")

    today = datetime.date.today()

    offset = (today.day + 1)
    print(offset)

    date_offset = datetime.date(int(today.year), int(today.month), int(offset))
    print(date_offset)

    cursor.execute("SELECT name from events WHERE day = :date", {"date": date_offset})
    events_near = cursor.fetchall()

    connection.commit()
    cursor.close()

    if events_near:
        yield events_near
    else:
        return False
