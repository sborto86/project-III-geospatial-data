from src.queries import mongo_con
if "pd" not in dir():
    import pandas as pd

### DATAFRAME MANIPULATION FUNCTIONS

def clean_money (string):
    '''
    Function to convert to an aomount in USD the string located in the field total_money_raised of the Crunchbase database.
    If can't be converted prints the string
    '''
    money = ""
     # Currency convertion value 29/10/2022
    if "C$" in string:
        multi = 0.73
        string = string.replace("C$", "")
    elif "$" in string:
        multi = 1
        string = string.replace("$", "")
    elif "€" in string:
        multi = 1
        string = string.replace("€", "")
    elif "£" in string:
        multi = 1.16
        string = string.replace("£", "")
    elif "¥" in string:    
        multi = 0.0068 #All companies that contain ¥ are located in Japan
        string = string.replace("¥", "")
    elif "kr" in string:
        multi = 0.091
        string = string.replace("kr", "")
    # Transforming string to a number
    for i in string:
            if i.isdigit() or i== ".":
                money = money + i
            elif i == 'K' or i == 'k':
                multi = 1000
            elif i == 'M' or i == 'm':
                multi = 1000000
            elif i == 'B' or i == 'b':
                multi = 1000000000
            else:
                print(string)
                return (string)
    return float(money)*multi

### DATABASE CREATION

def companies_1m (save=False, coll="lab"):
    
    '''
    Creates a list of office locations from companies that raised more than 1 M USD
        Parameters:
            save: bool (Default: False)
                Save to csv the dataframe created
            coll: str (Default: "lab")
                collection where Crunchbase database is stored
    '''
    
    #Establishing conection with MongoDB
    
    c= mongo_con(coll)

    # Quering Database

    query = {"total_money_raised":{"$exists":"true"}}
    projection = {"name":1, "total_money_raised":1, "offices":1, "_id":0}
    companies = list(c.find(query, projection))

    # Cleaning database
    
    companies_df = pd.DataFrame(companies)
    companies_df.dropna(inplace=True)

    # Filtering by money raised

    companies_df["total_money_raised"] = companies_df["total_money_raised"].apply(clean_money)
    companies_df = companies_df[companies_df["total_money_raised"] > 1000000]

    # Creating a database of all offices from companies with more than 1 Million raised

    offices_df = []
    for i, v in companies_df.iterrows():
        for e in v["offices"]:
            office = {}
            office['name'] = v['name']
            office['country_code'] = e['country_code']
            office['city'] = e['city']
            office['latitude'] = e['latitude']
            office['longitude'] = e['longitude']
            offices_df.append(office)
    offices_df = pd.DataFrame(offices_df)
    offices_df.dropna(inplace=True)
    offices_df.reset_index(drop=True, inplace=True)
    if save:
        offices_df.to_csv('./data/companies_1m.csv')
    return offices_df

def companies_design (save=False, coll="lab"):

    '''
    Creates a list of offices locations from design companies
        Parameters:
            save: bool (Default: False)
                Save to csv the dataframe created
            coll: str (Default: "lab")
                collection where Crunchbase database is stored
    '''

    #Establishing conection with MongoDB
    
    c= mongo_con(coll)

    # Quering Database

    query = {"$or": [{"tag_list":{"$regex" : "[Dd]esign"}}, {"description":{"$regex" : "[Dd]esign"}}, {"name":{"$regex" : "design"}}]}
    projection = {"name":1, "offices":1, "_id":0}
    companies = list(c.find(query, projection))

    # Cleaning database
    
    companies_df = pd.DataFrame(companies)
    companies_df.dropna(inplace=True)

    # Creating a database of all offices from design companies

    offices_df = []
    for i, v in companies_df.iterrows():
        for e in v["offices"]:
            office = {}
            office['name'] = v['name']
            office['country_code'] = e['country_code']
            office['city'] = e['city']
            office['latitude'] = e['latitude']
            office['longitude'] = e['longitude']
            offices_df.append(office)
    offices_df = pd.DataFrame(offices_df)
    offices_df.dropna(inplace=True)
    offices_df.reset_index(drop=True, inplace=True)
    if save:
        offices_df.to_csv('./data/companies_design.csv')
    return offices_df

def airports (save=False, file="airports_raw.csv"):

    '''
    Function to clean aiport data from OurAirports database
    Parameters: 
        save: bool (Default: False)
            save a csv file with the clean database
        file: str
            name of the raw file dowloaded from OurAirports
    '''        
    airports = pd.read_csv(f"./data/{file}")
    
    # removing unnecessary columns and rows
    
    airports = airports[(~airports.iata_code.isna())&(airports.type != "closed")&(airports.type != "heliport")&(airports.type != "seaplane_base")]
    airports = airports[["name", "iata_code", "iso_country","latitude_deg", "longitude_deg"]]

    # Reformating dataframe

    airports.reset_index(drop=True, inplace=True)
    airports.rename(columns={'latitude_deg': 'latitude',
                            'longitude_deg': 'longitude'},
                    inplace=True, errors='raise')
    # save file
    if save:
        airports.to_csv('./data/airports.csv')
    
    return airports

def offices_list (save=True, coll="lab"):
    
    '''
    Creates a list of office locations
        Parameters:
            save: bool (Default: False)
                Save to csv the dataframe created
            coll: str (Default: "lab")
                collection where Crunchbase database is stored
    '''
    #Establishing conection with MongoDB
    
    c= mongo_con(coll)

    # Quering Database and crating DataFrame

    query = {"offices":{"$exists":"true"}}
    projection = {"name":1, "offices":1, "_id":0}
    companies = list(c.find(query, projection))
    companies_df = pd.DataFrame(companies)

    # Creating a database of all offices

    offices_df = []
    for i, v in companies_df.iterrows():
        for e in v["offices"]:
            office = {}
            office['name'] = v['name']
            office['country_code'] = e['country_code']
            office['city'] = e['city']
            office['latitude'] = e['latitude']
            office['longitude'] = e['longitude']
            offices_df.append(office)
    offices_df = pd.DataFrame(offices_df)
    # Cleaning Database
    offices_df.dropna(inplace=True)
    offices_df.reset_index(drop=True, inplace=True)
    if save:
        offices_df.to_csv('./data/offices.csv')
    return offices_df