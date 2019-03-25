class data_source:
    def __init__(self):
        self.data = []

    '''
    struktura krotki (odpowiada wierszowi w bazie danych)
    jak rozumiem ze data_source jest abstrakcja
    aktualne zakłądy i historyczne zakłady mają jedną wspołna ceche tj.
    gospodarz, gość i data meczu
    dlatego kazdy wiersz musi zawierac te trzy atrybuty
    wiec kazdy wiersz jest postaci 
    (gospodarze, goscie, data_rozegrania meczu     
    '''

    def insert_data(self, tup):
        self.data.append(tup)

    def get_data(self):
        return self.data

    def get_specific_data(self, host, away, date):
        return list(filter(lambda tup:tup[0]==host and tup[1]==away and tup[2]==date,self.data))

    def delete_data(self,host, away, date):
        self.data=[dd for dd in self.data if dd[0]!=host or dd[1]!=away or dd[2]!=date]


t=data_source()
t.insert_data(('a','b','21-10-2019'))
t.insert_data(('a','b','21-10-2019'))
t.insert_data(('a','b','21-10-2019'))
t.insert_data(('a','c','22-10-2019'))
t.insert_data(('a','d','22-10-2019'))
print(t.get_data())
print(t.get_specific_data('a','b','21-10-2019'))
t.delete_data('a','b','21-10-2019')
print(t.get_data())