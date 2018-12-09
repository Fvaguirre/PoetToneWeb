import pandas as pd
import sqlalchemy
# RUN THIS TO LOAD DATA FROM CSV INTO POSTGRES DB
# BEFORE RUNNING THIS SCRIPT YOU SHOULD HAVE:
# 1.) INSTALLED POSTGRESQL
# 2.) INSTALLED ALL REQS
# 3.) MADE A DB CALLED "PoetTone"
# 4.) HAVE YOUR POSTGRESQL PASSWORD AND USERNAME
# 5.) ALTERED THE "engine" variable below to match your POSTGRESQL setup
if __name__=='__main__':
    data = pd.read_csv("app/poems_data.csv")
    # Preview the first 5 lines of the loaded data
    data1 = (data[['title', 'author', 'url', 'poem', 'tags', 'source']])

    #connect to db
    engine = sqlalchemy.create_engine('postgresql://YOUR_DB_USERNAME:YOUR_DB_PASSWORD@localhost:5432/PoetTone')

    drop = []
    for i in range(0, len(data1)):
        if type(data1.loc[i]['poem']) is float:
            drop.append(i)
            continue
        elif len(data1.loc[i]['poem']) > 5120:
            print(i)
            print(data1.loc[i]['title'])
            drop.append(i)
        elif len(data1.loc[i]['title']) > 128:
            drop.append(i)

    data1.drop(data1.index[drop]).rename(columns={'author': 'poet', 'poem': 'text'}).to_sql(name='poem', con=engine, index=False,
        if_exists='append')


