from data_source import DataSource

class DataSourceActuall(DataSource):
    def __init__(self):
        super().__init__()
        self.create_table()

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
                                              URL VARCHAR,
                                              INTERVAL INTEGER,
                                              PRIMARY KEY (Host,Away,DateOfMatch,OddNumber)
                                             )""")
        self.conn.commit()

    def get_len_specific_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? and IsActual=1 ',
                       (date, host, away))
        self.conn.commit()
        return len(self.c.fetchall())

    def insert_data(self, tup):
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

    def get_data(self):
        self.c.execute('SELECT * FROM Odds WHERE IsActual=1')
        self.conn.commit()
        return self.c.fetchall()

    def get_parametr_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=1 ORDER BY OddNumber',
                       (date, host, away,))
        self.conn.commit()
        return self.c.fetchall()
        

    def get_parametr_data_new(self, host, away, date):
        self.c.execute(
            'SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=1 ORDER BY OddNumber DESC ',
            (date, host, away,))
        self.conn.commit()
        return self.c.fetchall()[0]

    def delete_specific_data(self, host, away, date):
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=1', (date, host, away))
        self.conn.commit()
        
    def get_data_just_names_and_dates(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=1 and OddNumber=0')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_date(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=1 and OddNumber=0 ORDER BY DateOfMatch ASC, TimeOfBegin ASC')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_price(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=1 and OddNumber=0 ORDER BY Max(OddForHost, OddForAway, OddForDraw), TimeOfBegin DESC')
        return self.c.fetchall()

