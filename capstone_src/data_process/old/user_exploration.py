import pandas as pd


def anlise_1(db_conn):

    query = "SELECT TOP 10 * FROM dbo.AllSessions"

    data_frame = pd.read_sql(query, db_conn)

    if data_frame is not None:
        print(data_frame.head())
        
        print(data_frame.info())
        
        print(data_frame.describe())

        print(data_frame.nunique())
    
    else :
        print("No data returned")

def anlise_2(db_conn):

    query = "SELECT *, LOWER(" + \
               "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(" + \
               "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(" + \
               " REPLACE(REPLACE(City," + \
               "'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')," + \
               "'à', 'a'), 'è', 'e'), 'ì', 'i'), 'ò', 'o'), 'ù', 'u')," + \
               "'â', 'a'), 'ê', 'e'), 'î', 'i'), 'ô', 'o'), 'û', 'u')," + \
               "'ã', 'a'), 'õ', 'o')," + \
               "'ç', 'c') ) as city_new " + \
	        "FROM dbo.[Users-21-05-24] u"
    
    print( query)

    data_frame = pd.read_sql(query, db_conn)

    if data_frame is not None:

        data_frame['city_new'] = data_frame['city_new'].astype('category')
        data_frame['Device'] = data_frame['Device'].astype('category')
        data_frame['OS_version'] = data_frame['OS_version'].astype('category')
        data_frame['Platform'] = data_frame['Platform'].astype('category')
        data_frame['App_version'] = data_frame['App_version'].astype('category')
        data_frame['Device_class'] = data_frame['Device_class'].astype('category')

        print(data_frame.memory_usage(deep=True))
    
    else :
        print("No data returned")


def anlise_3(db_conn):

    data_frame = pd.read_csv('data_files/users.csv')

    if data_frame is not None:

        data_frame['city_new'] = data_frame['city_new'].astype('category')
        data_frame['Device'] = data_frame['Device'].astype('category')
        data_frame['OS_version'] = data_frame['OS_version'].astype('category')
        data_frame['Platform'] = data_frame['Platform'].astype('category')
        data_frame['App_version'] = data_frame['App_version'].astype('category')
        data_frame['Device_class'] = data_frame['Device_class'].astype('category')

        data_frame['Sessions'] = data_frame['Sessions'].astype('int')
        data_frame['Time_in_seconds'] = data_frame['Time_in_seconds'].astype('int')
        data_frame['Gestures_as_int'] = data_frame['Gestures_as_int'].astype('int')
        data_frame['Screens'] = data_frame['Screens'].astype('int')
        data_frame['Events'] = data_frame['Events'].astype('int')
        data_frame['Gestures'] = data_frame['Gestures'].astype('int')
        data_frame['Rage_gestures'] = data_frame['Rage_gestures'].astype('int')

        print(data_frame.memory_usage(deep=True))
        print(data_frame.memory_usage(deep=True).sum())
    
    else :
        print("No data returned")
