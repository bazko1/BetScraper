from data_source import DataSource

class DataSourceHistorical(DataSource):
    def __init__(self):
        super().__init__()
        self.create_table()

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
                                              PRIMARY KEY (Host,Away,DateOfMatch,OddNumber)
                                             )""")
        self.conn.commit()
        self.c.close()
    def get_len_specific_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? and IsActual=0 ',
                       (date, host, away))
        self.conn.commit()
        o = len(self.c.fetchall())
        self.c.close()
        return o

    def insert_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('UPDATE Odds SET IsActual=0 WHERE Host=? and Away=? and DateOfMatch=? and IsActual=1',
                       (host, away, date))
        self.conn.commit()
        sef.c.close()

    def get_data(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE IsActual=0')
        self.conn.commit()
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_parametr_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0 ORDER BY OddNumber',
                       (date, host, away))
        self.conn.commit()
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_parametr_data_new(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute(
            'SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0 ORDER BY OddNumber DESC ',
            (date, host, away))
        self.conn.commit()
        o = self.c.fetchall()[0]
        self.c.close()
        return o

    def delete_specific_data(self, host, away, date):
        self.c = self.conn.cursor()
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0', (date, host, away))
        self.conn.commit()
        self.c.close()
    def get_data_just_names_and_dates(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=0 and OddNumber=0')
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_data_just_names_and_dates_sort_by_date(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=0 and OddNumber=0 ORDER BY DateOfMatch ASC ,TimeOfBegin ASC')
        o = self.c.fetchall()
        self.c.close()
        return o

    def get_data_just_names_and_dates_sort_by_price(self):
        self.c = self.conn.cursor()
        self.c.execute('SELECT Host, Away, DateOfMatch, TimeOfBegin FROM Odds WHERE IsActual=0 and OddNumber=0 ORDER BY Max(OddForHost, OddForAway, OddForDraw), DateOfMatch, TimeOfBegin DESC')
        o = self.c.fetchall()
        self.c.close()
        return o


