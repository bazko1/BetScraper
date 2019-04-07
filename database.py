import sqlite3
import sqlite3

location = 'data'
table_name = 'table_name'


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('sts')
        self.c = self.conn.cursor()

    def close(self):
        """close sqlite3 connection"""
        self.conn.close()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS Odds37 (
                                          DateOfMatch  Date NOT NULL ,
                                          TimeOfBegin TIME NOT NULL ,
                                          Host VARCHAR NOT NULL ,
                                          Away VARCHAR NOT NULL ,
                                          OddForHost FLOAT NOT NULL ,
                                          OddForAway FLOAT NOT NULL ,
                                          OddForDraw FLOAT  NULL ,
                                          Current_Historical INTEGER NOT NULL ,
                                          OddNumber INTEGER NOT NULL 
                                          PRIMARY key (Host,Away,DateOfMatch,OddNumber)

                                          )""")
        self.conn.commit()

    def insert(self, tup):
        self.c.execute(
            'INSERT INTO Odds37 VALUES (?,?,?,?,?,?,?,?,?)',
            (tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
        self.conn.commit()

    def select(self):
        self.c.execute('select * from Odds37')
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


tup = ('29.03.2019', '18:00', 'W. Płock', 'X', 'Lubin', 2.40, 3.30, 3.00, 0, 0)
tup = ('29.04.2019', '19:00', 'A', '', 'Lubin', 2.40, 3.30, 3.00, 0, 0)
with Database() as db:
    db.create_table()
    db.insert(tup)
    db.select()

a = Database()
a.insert()