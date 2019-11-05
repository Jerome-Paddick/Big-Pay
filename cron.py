"""
Background
Cron is a linux software utility which implements a time-based job scheduler.
Cron is most suitable for scheduling repetitive tasks.
Cron is driven by a crontab (i.e. cron table) file, a configuration file that specifies
shell commands to run periodically on a given schedule.
The syntax of each line in a crontab file expects a cron expression: A cron
expression comprises of five fields, followed by a shell command to execute.
The challenge:
You are required to implment a cron-style service in python.
A solution should comprise of the following
• a full copy of your source code
• instructions on how to use a working demo
• a report on your solution, including documentation on
– any assumptions you have made for your code implementation
– any limitations in your implementation
Recommended effort:
Take no more than 1 day’s effort on this.
Additional comments
• Ensure that you provide us with a We want to see how you would design
your implmentation
• keep in mind that, as a service, you want your implmentation to have as
minimum an impact on a system as possible
"""

"""
Decisions:
    STORAGE
    Needs - read and write to file, simple, easy to deploy, small footprint, fast
    -> sqlite3 offers a single file db which is simple and easily deployable
    -> file is read in aligned blocks of page-size bytes and read pages are stored in the page cache to minimize file
       reads which offers an advantage over solutions like stored JSON data in terms of overall file reads and footprint
    
    Autorun
    -> store launch file in 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'
    
    
    
       
"""
import sqlite3
import os


class Cron:
    def __init__(self):
        self.conn = sqlite3.connect('cron.db')
        self.c = self.conn.cursor()
        if os.path.exists("cron.db") and os.stat('cron.db').st_size == 0:
            self.create()

    def create(self):
        self.c.execute(
            """CREATE TABLE cron_table (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                date date,
                time text,
                job text
                )""")
        self.c.execute(
            """CREATE TABLE daily_cron_table (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                time text,
                job text
                )""")
        self.conn.commit()

    def check_exists(self, data_dict):
        self.c.execute("SELECT * from cron_table WHERE time=:time AND job=:job", data_dict)
        if self.c.fetchone():
            print("found")
            return True

    def insert(self, date, time, job, daily=False):
        data_dict = {"date": date, "time": time, "job": job}
        print(data_dict)
        if not self.check_exists(data_dict):
            with self.conn:
                if daily:
                    self.c.execute("INSERT INTO daily_cron_table (time, job) VALUES (:time, :job)", data_dict)
                else:
                    self.c.execute("INSERT INTO cron_table (date, time, job) VALUES (:date, :time, :job)", data_dict)

    def delete(self, id, daily=False):
        with self.conn:
            if daily:
                self.execute(f"DELETE FROM daily_cron_table WHERE id = {id};")
            else:
                self.execute(f"DELETE FROM cron_table WHERE WHERE id = {id};")

    def read_dates(self):
        self.c.execute("SELECT * FROM cron_table WHERE date > '2001-01-01' and date < '2010-01-01'")
        print(self.c.fetchall())

    def execute(self, statement):
        self.c.execute(statement)
        print(self.c.fetchall())

    def __exit__(self):
        self.conn.close()

if __name__ == "__main__":
    cron = Cron()
    cron.execute("SELECT * from cron_table")
    cron.read_dates()