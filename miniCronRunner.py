import sqlite3
import hotelWorker
import os

def file_accessible(filepath, mode):
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True


def checking_if_left(cursor):
    cursor.execute('SELECT TaskId FROM TaskTimes WHERE NumTimes>0')
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True


def main():
    import time

    dir_path = os.path.dirname(os.path.realpath(__file__))
    condition = file_accessible(dir_path + '/' + 'cronhoteldb.db', 'r')

    if condition:
        conn = sqlite3.connect(dir_path + '/' + 'cronhoteldb.db')
        with conn:
            c = conn.cursor()
        first_it = True
        task_with_time = list()

        while condition and checking_if_left(c):
            if first_it:
                first_it = False
                c.execute('SELECT * FROM TaskTimes WHERE NumTimes>0')
                all_tasks = c.fetchall()
                for task in all_tasks:
                    c.execute('SELECT TaskName, Parameter FROM Tasks WHERE TaskId==(?)', (int(task[0]),))
                    task1 = c.fetchone()
                    time_ans = hotelWorker.dohoteltask(task1[0], task1[1])
                    c.execute('UPDATE TaskTimes SET NumTimes=NumTimes-1 WHERE TaskId=(?)', (int(task[0]),))
                    conn.commit()
                    task_with_time.append([int(task[0]), time_ans])
            else:
                c.execute('SELECT * FROM TaskTimes WHERE NumTimes>0')
                all_tasks = c.fetchall()

                for task in all_tasks:

                    c.execute('SELECT DoEvery FROM TaskTimes WHERE TaskId==(?)', (int(task[0]),))
                    how_often = c.fetchone()[0]
                    time1 = dict(task_with_time)[task[0]]
                    time1 = float(time1)
                    time_dif = time.time() - time1

                    if how_often-0.1 < time_dif < how_often+0.1:

                        c.execute('SELECT TaskName, Parameter FROM Tasks WHERE TaskId==(?)', (int(task[0]),))
                        another_call = c.fetchall()[0]
                        for i in range(len(task_with_time)):
                            if task_with_time[i][0] == task[0]:
                                task_with_time[i][1] = hotelWorker.dohoteltask(another_call[0], another_call[1])
                                c.execute('UPDATE TaskTimes SET NumTimes=NumTimes-1 WHERE TaskId=(?)', (int(task[0]),))
                                conn.commit()




if __name__ == '__main__':
    main()
