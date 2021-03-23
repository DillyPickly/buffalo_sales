import pandas as pd
import numpy as np

# import time
# import logging
# start = time.time()
# done = time.time()
# logging.info("Process Data: {:.2f}s".format(done-start))


def process_data():
    
    orin_file = 'data/buffalo_assessment_2020-2021.csv'
    new_file  = 'data/modified_buffalo_assessment_2020-2021.csv'

    def df_wgs84_to_web_mercator(df, lon="LONGITUDE", lat="LATITUDE"):

        k = 6378137
    #     df["x"] = df[lon] * (k * np.pi/180.0)
    #     df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k

        df.loc[:,'x'] = df.loc[:,lon] * (k * np.pi/180.0)
        df.loc[:,'y'] = np.log(np.tan((90 + df.loc[:,lat]) * np.pi/360.0)) * k
        
        return df


    # Read Data
    df = pd.read_csv(orin_file,sep=',',header=0,index_col=0)

    print('BEFORE: Number of rows   : ', df.shape[0])
    print('BEFORE: Number of columns: ', df.shape[1])

    # Filter Locations
    df = df.loc[df.loc[:,'LOCATION'].notnull(),:]
    # Create Mercator Coords
    df = df_wgs84_to_web_mercator(df)
    # Filter Bad Date
    bad_str = df['DEED DATE'][0] # Bad Date
    df = df.loc[(df.loc[:,'DEED DATE'] != bad_str),:]
    # Add Deed Year Column
    df.loc[:,'DEED YEAR'] = df.apply(lambda row: int(row.loc['DEED DATE'].split(' ')[0].split('/')[-1]), axis = 1)
    df = df.loc[(df.loc[:,'DEED YEAR'] > 1990),:]
    # Remove Low Sale Prices
    df = df.loc[(df.loc[:,'SALE PRICE'] > 10000),:]
    # Remove property type other than residentail, vacant land, and commercial
    df = df[df['PROPERTY CLASS'] < 500]

    # Remove Columns ## we need 
    # print(df.columns)
    df = df[['x','y','DEED YEAR','PROPERTY CLASS','SALE PRICE','PROP CLASS DESCRIPTION','ADDRESS']]

    print('AFTER: Number of rows   : ', df.shape[0])
    print('AFTER: Number of columns: ', df.shape[1])

    
    df.to_csv(new_file)

    return df

def load_data(uri):
    df = pd.read_csv(uri,sep=',',header=0,index_col=0)
    return df


if __name__ == "__main__":
    process_data()