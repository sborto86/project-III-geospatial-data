from src.criteria import conditions, score_calculator
from src.queries import foursquare
if "pd" not in dir():
    import pandas as pd
from geopy.distance import geodesic

def get_close_places (df, df_com, max_distance):
    '''
    Function that generates a pd.Series with the inteseccion of 2 dataframes of locations for a given distance.
    Parameters:
        df: pd.DataFrame
            Dataframe to find close places with a list of places with longitude and latitude
        df_com: pd.DataFrame
            Dataframe with a list of places to intersect with df (must contain longitude and latitude)
        max_distance: int
            Maximum distance in Km to interesect the 2 dataframes 
    '''
    new_col = []
    for row in df.itertuples():
        closeplaces=[]
        position1 = (row.latitude, row.longitude)
        for e in df_com.to_dict('records'):
            position2 = (e['latitude'], e['longitude'])
            distance = geodesic(position1, position2).km
            if distance > 0 and distance < max_distance or distance == 0 and row.name != e['name']:
                place = e
                place['distance']= distance
                closeplaces.append(place)
        places = sorted(closeplaces, key=lambda x: x['distance'])
        new_col.append(places)
    return pd.Series(new_col)

def add_score(df, condition):
    '''
    Function to add 2 columns in a dataframe for a given condition (imported from criteria.py)
        condition(num)_results: Dictionary with all the locations that meet the criteria of the given condition 
        condition(num)_score: Score given to the location for the given criteria (calculated with score_calculator)
    '''
    cr = conditions[condition]
    if cr["source"] == "Foursquare":
        new_col = []
        for index, row in df.iterrows():
            location=(row["latitude"], row["longitude"])
            places = foursquare(location, condition, sort="DISTANCE")

    elif cr["source"] == "OurAirports":
        try:
            df_com = pd.read_csv('./data/airports.csv')
        except:
            from src.database import airports
            df_com = airports(save=True)
        df[f"condition{condition}_results"] = get_close_places(df, df_com, cr["max_dist"])
    elif cr["source"] == "Crunchbase":
        if cr["query"] == "More than 1,000,000":
            try:
                df_com = pd.read_csv('./data/companies_1m.csv')
            except:
                from src.database import companies_1m
                df_com = companies_1m(save=True)
            df[f"condition{condition}_results"] = get_close_places(df, df_com, cr["max_dist"])
        elif cr["query"] == "design":
            try:
                df_com = pd.read_csv('./data/companies_design.csv')
            except:
                from src.database import companies_design
                df_com = companies_design(save=True)
            df[f"condition{condition}_results"] = get_close_places(df, df_com, cr["max_dist"])
        else:
            print("There is a problem in the conditions dictionary")
            return df
    scores = []
    for e in df[f"condition{condition}_results"]:
        if e:
            score = score_calculator(condition, len(e), e[0]["distance"])
        else:
            score = 0
    return df
