import sqlite3
import sqlite3

location = 'data'
table_name = 'table_name'


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('sts')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS Odds37 (
                                          DateOfMatch  Date NOT NULL ,
                                          TimeOfBegin TIME NOT NULL ,
                                          Host VARCHAR NOT NULL ,
                                          Away VARCHAR NOT NULL ,
                                          OddForHost FLOAT NOT NULL ,
                                          OddForAway FLOAT NOT NULL ,
                                          OddForDraw FLOAT  NULL ,
                                          IsCurrent INTEGER NOT NULL ,
                                          IsSuspectOdd INTEGER NOT NULL ,
                                          OddNumber INTEGER NOT NULL ,
                                          PRIMARY key (Host,Away,DateOfMatch,OddNumber)

                                         )""")
        self.conn.commit()

    def insert_data(self, tup):
        number = self.get_len_specific_data(tup[2], tup[3], tup[0])
        if number==0:
            current=1
            susp=0
        else:
            t=self.get_specific_data(tup[2],tup[3],tup[0])
            current=t[0][7]
            susp=t[0][8]
        self.c.execute(
            'INSERT INTO Odds37 VALUES (?,?,?,?,?,?,?,?,?,?)',
            (tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], current, susp, number + 1))
        self.conn.commit()


    def get_data(self):
        self.c.execute('SELECT * FROM Odds37')
        return self.c.fetchall()

    def get_specific_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds37 WHERE DateOfMatch=? and Host=? and Away=? ORDER BY OddNumber',
                       (date, host, away))
        return self.c.fetchall()

    def get_len_specific_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds37 WHERE DateOfMatch=? and Host=? and Away=? ', (date, host, away))
        return len(self.c.fetchall())

    def delete_specific_data(self, host, away, date):
        self.c.execute('DELETE FROM Odds37 WHERE DateOfMatch=? and Host=? and Away=?', (date, host, away))

    def update_from_current_to_historical(self, host, away, date):
        self.c.execute('UPDATE Odds37 SET IsCurrent=? WHERE Host=? and Away=? and DateOfMatch=? and IsCurrent=?',
                       (0, host, away, date, 1))

    def update_to_suspect(self, host, away, date):
        self.c.execute('UPDATE Odds37 SET IsSuspectOdd=? WHERE Host=? and Away=? and DateOfMatch=? and IsSuspectOdd=?',
                       (1, host, away, date, 0))

    def get_actuall(self):
        self.c.execute('SELECT * FROM Odds37 WHERE IsCurrent=1')
        return self.c.fetchall()

    def get_historical(self):
        self.c.execute('SELECT * FROM Odds37 WHERE IsCurrent=0')
        return self.c.fetchall()

    def get_suspect(self):
        self.c.execute('SELECT * FROM Odds37 WHERE  IsSuspectOdd=1')
        return self.c.fetchall()

    def get_normal(self):
        self.c.execute('SELECT * FROM Odds37 WHERE  IsSuspectOdd=0')
        return self.c.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.c.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def close(self):
        self.conn.close()

tup = ('29.03.2019', '18:00', 'W. Płock', 'X', 'Lubin', 2.40, 3.30, 3.00, 0, 0)
tup1 = ('29.04.2019', '19:00', 'A', '', 'Lubin', 2.40, 3.30, 3.00, 0, 0)
with Database() as db:
    db.create_table()
    db.insert_data( tup)
    db.get_data()

a = Database()

