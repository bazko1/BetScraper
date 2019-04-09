from data_source import DataSource
from data_source_actuall import DataSourceActuall
from data_source_historical import DataSourceHistorical
from data_source_suspicious import DataSourceSuspicious
a=DataSource()
a.insert_data(('09.04.2019', '03:20', 'Virginia Cavaliers', 'Virginia Cavaliers', '1.70', '1.90'))
print('two gets')
print(a.get_data())
print(a.get_parametr_data_new('Virginia Cavaliers', 'Texas Tech','09-04-2019'))
a=DataSourceActuall()
a.insert_data(('10.04.2019', '21:00', 'Manch. Utd', 'X', 'Barcelona', '3.58', '3.50', '2.05'))
print(a.get_data())
print(a.get_parametr_data(host='Manch. Utd',away='Barcelona',date='10-04-2019'))
a=DataSourceHistorical()
a.insert_data(host='Manch. Utd',away='Barcelona',date='10-04-2019')
print(a.get_data())
a=DataSourceSuspicious()
a.insert_data(host='Virginia Cavaliers',away='Virginia Cavaliers',date='09-04-2019')
print(a.get_data())