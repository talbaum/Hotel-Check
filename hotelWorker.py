import sqlite3
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
con = sqlite3.connect(dir_path+'/'+'cronhoteldb.db')
c = con.cursor()


def dohoteltask (taskname, parameter):
    if taskname == 'wakeup':
        c.execute('SELECT FirstName FROM Residents WHERE RoomNumber=(?)', (parameter,))
        firstname = c.fetchone()[0]
	c.execute('SELECT LastName FROM Residents WHERE RoomNumber=(?)', (parameter,))
        lastname = c.fetchone()[0]
        mytime = str(time.time())
        print str(firstname) + ' ' + str(lastname) + ' in room ' + \
                str(parameter) + ' received a wakeup call at ' + mytime
        return mytime

    elif taskname == 'breakfast':
        c.execute('SELECT FirstName FROM Residents WHERE RoomNumber=(?)', (parameter,))
        firstname = c.fetchone()[0]
	c.execute('SELECT LastName FROM Residents WHERE RoomNumber=(?)', (parameter,))
        lastname = c.fetchone()[0]
        mytime = str(time.time())
        print str(firstname) + ' ' + str(lastname) + ' in room ' + \
              str(parameter) + ' has been served breakfast at ' + mytime
        return mytime

    elif taskname == 'clean':
        c.execute('SELECT RoomNumber FROM Rooms')
        allrooms = c.fetchall()

        dontcleanlist = []
        for room in allrooms:
                c.execute('SELECT RoomNumber FROM Residents WHERE RoomNumber=(?)', (room[0],))
                dontcleanlist.append(c.fetchone())

        cleanlist=[]
        for room in allrooms:
            if dontcleanlist.count(room) == 0:
                cleanlist.append(room)

        cleanlist.sort()
        mytime = str(time.time())
        clean_rooms = str([i[0] for i in cleanlist])
        print 'Rooms ' + clean_rooms[1:len(clean_rooms)-1] + ' were cleaned at ' + mytime
        return mytime
