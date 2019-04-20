from data_source import DataSource
from data_source_actuall import DataSourceActuall
from data_source_historical import DataSourceHistorical
from data_source_suspicious import DataSourceSuspicious
a=DataSourceActuall()
#a.insert_data(('10.04.2019', '21:00', 'Manch. Utd', 'X', 'Barcelona', '10.01', '10.01', '10.01'))
#a.insert_data(('19.04.2019', '17:00', 'Warszawa', 'Jastrzębie', '10.01', '10.01'))
#a.insert_data(('17.04.2019', '17:30', 'Zawiercie', 'Kędzierzyn', '10.01', '10.01'))
#a.insert_data(('17.04.2019', '21:00', 'Manch. City', 'X','Tottenham', '10.01', '10.01', '10.01'))
#a.insert_data(('09.04.2019', '03:20', 'Virginia Cavaliers', 'Virginia Cavaliers', '10.01', '10.01'))
#print('two gets')
#print(a.get_data())
#print(a.get_parametr_data_new('Virginia Cavaliers', 'Texas Tech','09-04-2019'))
#a=DataSourceActuall()
#a.insert_data(('22.04.2019', '22:00', 'Manch. City', 'X','Tottenham', '10.01', '10.01', '10.01'))
#a.insert_data(('09.04.2019', '21:00', 'Virginia Cavaliers', 'Virginia Cavaliers', '10.01', '10.01'))
#a.insert_data(('21.04.2019', '22:00', 'Liverpool', 'X', 'Porto', '10.01', '10.01', '10.01'))
#a.insert_data(('9.04.2019', '21:00', 'Virginia Cavaliers', 'Virginia Cavaliers', '10.01', '10.01'))
#print(a.get_data())
#print(a.get_parametr_data(host='Manch. Utd',away='Barcelona',date='10-04-2019'))
#a=DataSourceHistorical()
#a.insert_data(host='Manch. Utd',away='Barcelona',date='10-04-2019')
# a.insert_data(host='Manch. Utd', away='Barcelona', date='10-04-2019')
# a.insert_data(host='Virginia Cavaliers', away='Virginia Cavaliers', date='09-04-2019')
# #print(a.get_data())
# a=DataSourceSuspicious()
# #a.insert_data(host='Virginia Cavaliers',away='Virginia Cavaliers',date='09-04-2019')
# a.insert_data(date='10-04-2019',host='Manch. Utd',away='Barcelona')
# a.insert_data(date='17-04-2019',host='Manch. City',away='Tottenham')
#print(a.get_data())

#print(a.get_data() )
#print( a.get_data() )
# print ( a.get_parametr_data('Nitra','Podbrezova','26-04-2019') )

#a.insert_url_int( ('20-04-2019','Feirense','Braga','aa',5) )

# print ( a.get_parametr_data(host='Nitra',away='Podbrezova',date='26-04-2019') )

#print(a.get_data() )
#print( a.get_data_byURL('https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=201&region=6582&league=4397&oppty=187482937') )
#print(a.get_data())
print( a.get_all_urlint() )