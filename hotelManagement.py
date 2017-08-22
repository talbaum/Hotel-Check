import sqlite3
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect('cronhoteldb.db')
with conn:
    c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS TaskTimes(TaskId integer PRIMARY KEY NOT NULL,'
    'DoEvery integer NOT NULL, NumTimes int NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS Tasks(TaskId integer REFERENCES TaskId(TaskId),'
    'TaskName VARCHAR(20) NOT NULL, Parameter integer NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS Rooms(RoomNumber integer PRIMARY KEY NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS Residents(RoomNumber integer NOT NULL REFERENCES Rooms(RoomNumber),'
              'FirstName VARCHAR(20) NOT NULL, LastName VARCHAR(20) NOT NULL)')


def readconf():

    lines = [line.rstrip('\n') for line in open(dir_path+'/'+sys.argv[1])]
    taskid=1
    for line in lines:
        myline = line.split(',')
        if myline[0] == 'room':
            if len(myline) == 2:
                c.execute('INSERT INTO Rooms VALUES(?)', (int(myline[1]),))
            elif len(myline) == 4:
                c.execute('INSERT INTO Rooms VALUES(?)', (myline[1],))
                c.execute('INSERT INTO Residents VALUES(?,?,?)', (int(myline[1]), myline[2], myline[3]))

        elif myline[0] == 'breakfast' or myline[0] == 'wakeup':
            c.execute('INSERT INTO TaskTimes VALUES(?,?,?)', (taskid, myline[1], myline[3]))
            c.execute('INSERT INTO Tasks VALUES(?,?,?)', (taskid, myline[0], myline[2]))
            taskid += 1

        elif myline[0] == 'clean':
            c.execute('INSERT INTO TaskTimes VALUES(?,?,?)', (taskid, myline[1], myline[2]))
            c.execute('INSERT INTO Tasks VALUES(?,?,?)', (taskid, myline[0], 0))
            taskid += 1
    conn.commit()
    conn.close()


def main() :
    create_table()
    readconf()



if __name__ == '__main__':
    main()