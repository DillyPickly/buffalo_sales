import pandas as pd
import numpy as np

def process_data(uri):
    
    def df_wgs84_to_web_mercator(df, lon="LONGITUDE", lat="LATITUDE"):

        k = 6378137
    #     df["x"] = df[lon] * (k * np.pi/180.0)
    #     df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k

        df.loc[:,'x'] = df.loc[:,lon] * (k * np.pi/180.0)
        df.loc[:,'y'] = np.log(np.tan((90 + df.loc[:,lat]) * np.pi/360.0)) * k
        
        return df

    # Read Data
    df = pd.read_csv(uri,sep=',',header=0,index_col=0)
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

    return df