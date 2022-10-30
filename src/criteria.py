# This file contains all the criteria to evaluate the project

# Dictionary of the staff in the company
staff = { 
"design": 20,
"uiux": 5,
"frontend": 10,
"data": 15,
"backend": 5,
"account": 20,
"maint": 1,
"exec": 10,
"ceo": 1,
"dog": 1
}

# Dictionary to with all the parameters used for evaluating a loaction

conditions = { 
            1: {
                "max_num": 10,
                "max_dist": 5,
                "people": staff["design"],
                "description": "Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.",
                "source": "Crunchbase",
                "categories": ["tags_list","description","name"],
                "query": "design"
            },
    
            2: {
                "max_num": 5,
                "max_dist": 3,
                "people": round((sum(staff.values())-1)*0.3),
                "description": "30% of the company staff have at least 1 child.",
                "source": "Foursquare",
                "categories": [12055, 12056, 12057, 12058, 12059, 12060, 12061, 12062],
                "query": None
             },

            3: {
                "max_num": 20,
                "max_dist": 20,
                "people": staff["frontend"] + staff["backend"],
                "description": "Developers like to be near successful tech startups that have raised at least 1 Million dollars.",
                "source": "Crunchbase",
                "categories": "total_money_raised",
                "query": "More than 1,000,000"
              },
            4: {
                "max_num": 1,
                "max_dist": 2,
                "people": staff["exec"],
                "description": "Executives like Starbucks A LOT. Ensure there's a starbucks not too far.",
                "source": "Foursquare",
                "categories":[13032],
                "query": "Starbucks"
                  
              },
            5: {
                "max_num": 1,
                "max_dist": 50,
                "people": staff["account"],
                "description": "Account managers need to travel a lot.",
                "source": "OurAirports",
                "categories": None,
                "query": None
              },

              6: {
                "max_num": 30,
                "max_dist": 3,
                "people": sum(staff.values())-1,
                "description": "Everyone in the company is between 25 and 40, give them some place to go party.",
                "source": "Foursquare",
                "categories":[13003, 10032],
                "query": None
              },

              7: {
                "max_num": 2,
                "max_dist": 2,
                "people": staff["ceo"],
                "description":"The CEO is vegan.",
                "source": "Foursquare",
                "categories":[13377],
                "query": None
              },

              8: {
                "max_num": 1,
                "max_dist": 10,
                "people": staff["maint"],
                "description": "If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.",
                "source": "Foursquare",
                "categories":[18008],
                "query": None
              },
              9: {
                  "max_num": 1,
                  "max_dist": 4,
                  "people": staff["dog"],
                  "description": "The office dog Dobby needs a hairdresser every month. Ensure there's one not too far away.",
                  "source": "Foursquare",
                  "categories":[11134],
                  "query": None
              },
}

# Formula to calculate scores

def score_calculator(condition, num, min_dist):
    '''
    This function calculates a score for a given condition:
    Parameters: 
        condition: int
            Number of conditions to get evaluated (1, 9)
        num: int
            The number of locations found that meet the condition.
        min_dist: float
            Distance in Km to the closest location that meets the condition 
    Criteria create the formula:
        1. All the workers are considered equal (including the dog)
        2. The closest the better
        3. The more locations that meet the criteria the better until a maximum number where more locations don't give an extra value     
    '''
    # calculating the maximum score 
    max_score = 0
    for c in conditions:
        max_score += c["people"]
    max_score = max_score * 2
    # calculating score of a given condition
    if num > 0:
        distance = 1 - (conditions[condition]["max_dist"]/ min_dist)
        if num >= conditions[condition]['max_num']:
            number = 1
        else:
            number = num / conditions[condition]['max_num']
        score = ((number + distance)*conditions[condition]["people"])/max_score
    else:
        score = 0
    return score