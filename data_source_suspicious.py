from data_source import DataSource


class DataSourceSuspicious(DataSource):
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
                                              PRIMARY KEY (Host,Away,DateOfMatch,OddNumber)
                                             )""")
        self.conn.commit()

    def get_len_specific_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? and IsSuspectOdd=1 ',
                       (date, host, away))
        self.conn.commit()
        return len(self.c.fetchall())

    def insert_data(self, host, away, date):
        self.c.execute('UPDATE Odds SET IsSuspectOdd=1 WHERE Host=? and Away=? and DateOfMatch=? ', (host, away, date))
        self.conn.commit()

    def get_data(self):
        self.c.execute('SELECT * FROM Odds WHERE IsSuspectOdd=1')
        self.conn.commit()
        return self.c.fetchall()

    def get_parametr_data(self, host, away, date):
        self.c.execute(
            'SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsSuspectOdd=1 ORDER BY OddNumber',
            (date, host, away))
        self.conn.commit()
        return self.c.fetchall()

    def get_parametr_data_new(self, host, away, date):
        self.c.execute(
            'SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsSuspectOdd=1 ORDER BY OddNumber DESC ',
            (date, host, away))
        self.conn.commit()
        return self.c.fetchone()

    def delete_specific_data(self, host, away, date):
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsSuspectOdd=1',
                       (date, host, away))
        self.conn.commit()

    def get_data_just_names_and_dates(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsSuspectOdd=1 and OddNumber=0')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_date(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsSuspectOdd=1 and OddNumber=0 ORDER BY DateOfMatch ASC, TimeOfBegin ASC')
        return self.c.fetchall()

    def get_data_just_names_and_dates_sort_by_price(self):
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsSuspectOdd=1 and OddNumber=0 ORDER BY Max(OddForHost, OddForAway, OddForDraw), TimeOfBegin DESC')
        return self.c.fetchall()
