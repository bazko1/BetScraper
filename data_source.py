import sqlite3


class DataSource(object):
    '''inicjalizacja kursora'''
    def __init__(self):
        self.conn = sqlite3.connect('sts',check_same_thread=False,timeout=30)
        self.create_table()
    '''stworzenie tabeli'''
    def create_table(self):
        self.c = self.conn.cursor()
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
                                          URL VARCHAR,
                                          INTERVAL INTEGER,
                                          PRIMARY KEY (Host,Away,DateOfMatch,TimeOfBegin, OddNumber)

                                         )""")
        self.conn.commit()
        self.c.close()

    '''pomocniczna funkcja do funkcji insert'''
    def get_len_specific_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ', (date, host, away))
        self.conn.commit()
        o = len(self.c.fetchall())
        self.c.close()
        return o
        
        

    '''dodanie danych'''
    def insert_data(self,tup):
        self.c = self.conn.cursor()
        date = tup[0].replace('.', '-')
        if tup[3] == 'X':
            number = self.get_len_specific_data(host=tup[2], away=tup[4], date=date)
            self.c.execute('INSERT INTO Odds VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (date, tup[1], tup[2], tup[4], tup[5], tup[7], tup[6], 1, 0, number, None, None,None,None))
        else:
            number = self.get_len_specific_data(host=tup[2], away=tup[3], date=date)
            self.c.execute('INSERT INTO Odds VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (date, tup[1], tup[2], tup[3], tup[4], tup[5], None, 1, 0, number, None, None,None,None))
        self.conn.commit()
        self.c.close()

    def insert_result(self, tup):
        self.c = self.conn.cursor()
        self.c.execute('UPDATE Odds SET ResultHost=?, ResultAway=? WHERE DateOfMatch=? and Host=? and Away=?',
                       (tup[3],tup[4],tup[0],tup[1], tup[2]))
        self.conn.commit()
        self.c.close()

    def get_result(self, host,away,date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT ResultHost,ResultAway FROM Odds WHERE DateOfMatch=? and Host=? and Away=?',
        (date,host,away) )
        o = self.c.fetchone()
        self.c.close()
        return o


    'tup= (date,host,away,url,int)'
    def insert_url_int(self, tup):
        self.c = self.conn.cursor()
        self.c.execute('UPDATE Odds SET URL=?, INTERVAL=? WHERE DateOfMatch=? and Host=? and Away=?',
                       (tup[3],tup[4],tup[0],tup[1],tup[2]))
        self.conn.commit()
        self.c.close()
    
    '''zwrocenie danych'''
    def get_data(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds')
        self.conn.commit()
        o = self.c.fetchall()
        self.c.close()
        return o
        
    
    '''zwrocenie danych z parameterem '''
    def get_parametr_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ORDER BY OddNumber',
                       (date, host, away))
        self.conn.commit()
        o = self.c.fetchall()
        self.c.close()
        return o

    '''zwrocenie danych wyszukanych za pomoco pola URL '''
    def get_data_byURL(self, URL):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE URL=?', (URL,) )
        self.conn.commit()
        o = self.c.fetchall()
        self.c.close()
        return o



    '''zwrocenie ostatniego kursu z meczow'''
    def get_parametr_data_new(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? ORDER BY OddNumber DESC ',
                       (date, host, away))
        self.conn.commit()
        o = self.c.fetchall()[0]
        self.c.close()
        return o
    '''usuneicie danych z parametrem'''
    
    def delete_specific_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? and Host=? and Away=?', (date, host, away))
        self.conn.commit()
        self.c.close()

    def get_data_just_names_and_dates(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0')
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_data_just_names_and_dates_sort_by_date(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0 ORDER BY DateOfMatch ASC TimeOfBegin ASC')
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_data_just_names_and_dates_sort_by_price(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE OddNumber=0 ORDER BY Max(OddForHost, OddForAway, OddForDraw), TimeOfBegin DESC')
        o = self.c.fetchall()
        self.c.close()
        return o

    def set_data_historical(self,host,away,date):
        self.c = self.conn.cursor()
        self.c.execute('UPDATE Odds SET IsActual=0 WHERE DateOfMatch=? and Host=? and Away=?',
                       (date,host,away) )
        self.conn.commit()
        self.c.close()

    def set_data_suspicious(self,host,away,date):
        self.c = self.conn.cursor()
        self.c.execute('UPDATE Odds SET IsSuspectOdd=1 WHERE DateOfMatch=? and Host=? and Away=?',
                       (date,host,away) )
        self.conn.commit()
        self.c.close()

    'zwraca wszyszkie pary link czas odswiezania ktore nie sa w historycznych'
    def get_all_urlint(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT URL,INTERVAL from Odds WHERE URL!="" and IsActual=1')
        o = self.c.fetchall()
        self.c.close()
        return o
        

    'zwraca bety w kolejności pobierania'
    def get_all_BetValues(self,host,away,date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT OddForHost,OddForAway,OddForDraw from Odds WHERE DateOfMatch=? and Host=? and Away=?',
        (date,host,away)
        )
        o = self.c.fetchall()
        self.c.close()
        return o

    'zwraca link dla konkretnego meczu'
    def get_url(self,host,away,date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT URL from Odds WHERE DateOfMatch=? and Host=? and Away=? and URL !=""',
        (date,host,away))
        o = self.c.fetchall()
        self.c.close()
        return o

    
