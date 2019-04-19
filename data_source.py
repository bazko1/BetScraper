import sqlite3


class DataSource(object):
    '''inicjalizacja kursora'''
    def __init__(self):
        self.conn = sqlite3.connect('sts',check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()
    '''stworzenie tabeli'''
    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS Odds (
                                          DateOfMatch  Date NOT NULL ,
                                          TimeOfBegin TIME NOT NULL ,
                                          Host VARCHAR NOT NULL ,
                                          Away VARCHAR NOT NULL ,
                                          OddForHost FLOAT NOT NULL ,
                                          OddForAway FLOAT NOT NULL ,
                                          OddForDraw FLOAT  NULL ,
                                          IsActual INTEGER NOT NULL ,
                                          IsSuspectOdd INTEGER NOT NULL ,
                                          OddNumber INTEGER NOT NULL ,
                                          ResultHost NULL,
                                          ResultAway NULL,
                                          PRIMARY KEY (Host,Away,DateOfMatch,TimeOfBegin, OddNumber)

                                         )""")
        self.conn.commit()

    '''pomocniczna funkcja do funkcji insert'''
    def get_len_specific_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ', (date, host, away))
        self.conn.commit()
        return len(self.c.fetchall())

    '''dodanie danych'''
    def insert_data(self,tup):
        date = tup[0].replace('.', '-')
        if tup[3] == 'X':
            number = self.get_len_specific_data(host=tup[2], away=tup[4], date=date)
            self.c.execute('INSERT INTO Odds VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                           (date, tup[1], tup[2], tup[4], tup[5], tup[7], tup[6], 1, 0, number, None, None))
        else:
            number = self.get_len_specific_data(host=tup[2], away=tup[3], date=date)
            self.c.execute('INSERT INTO Odds VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                           (date, tup[1], tup[2], tup[3], tup[4], tup[5], None, 1, 0, number, None, None))
        self.conn.commit()

    def insert_result(self, tup):
        self.c.execute('UPDATE Odds SET ResultHost=?, ResultAway=? WHERE DateOfMatch=? and Host=? and Away=?',
                       (tup[3],tup[4],tup[0],tup[1], tup[2]))
        self.conn.commit()
    '''zwrocenie danych'''
    def get_data(self):
        self.c.execute('SELECT * FROM Odds')
        self.conn.commit()
        return self.c.fetchall()
    '''zwrocenie danych z parameterem '''
    def get_parametr_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ORDER BY OddNumber',
                       (date, host, away))
        self.conn.commit()
        return self.c.fetchall()

    '''zwrocenie ostatniego kursu z meczow'''
    def get_parametr_data_new(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ORDER BY OddNumber DESC ',
                       (date, host, away))
        self.conn.commit()
        return (self.c.fetchall()[0])
    '''usuneicie danych z parametrem'''
    def delete_specific_data(self, host, away, date):
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? and Host=? and Away=?', (date, host, away))

    def get_data_just_names_and_dates(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_date(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0 ORDER BY DateOfMatch DESC TimeOfBegin ASC')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_price(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0 ORDER BY Max(OddForHost, OddForAway, OddForDraw), TimeOfBegin DESC')
        return self.c.fetchall()
