from data_source import DataSource

class DataSourceHistorical(DataSource):
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
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? and Host=? and Away=? and IsActual=0 ', (date, host, away))
        self.conn.commit()
        return len(self.c.fetchall())

    def insert_data(self,host,away,date):
        self.c.execute('UPDATE Odds SET IsActual=0 WHERE Host=? and Away=? and DateOfMatch=? and IsActual=1', (host, away, date))
        self.conn.commit()

    def get_data(self):
        self.c.execute('SELECT * FROM Odds WHERE IsActual=0')
        self.conn.commit()
        return self.c.fetchall()

    def get_parametr_data(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0 ORDER BY OddNumber',
                       (date, host, away))
        self.conn.commit()
        return self.c.fetchall()

    def get_parametr_data_new(self, host, away, date):
        self.c.execute('SELECT * FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0 ORDER BY OddNumber DESC ',
                       (date, host, away))
        self.conn.commit()
        return self.c.fetchall()[0]

    def delete_specific_data(self, host, away, date):
        self.c.execute('DELETE FROM Odds WHERE DateOfMatch=? AND Host=? AND Away=? AND IsActual=0', (date, host, away))
        self.conn.commit()