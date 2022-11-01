# Inporting libraries

import pandas as pd
from src.criteria import conditions, staff
from src.database import airports, offices_list, companies_design, companies_1m
from src.score import add_score, total_score

# Creating Databases

offices = offices_list()
airports = airports()
companies_design = companies_design()
companies_1m = companies_1m()

# Evaluating offices for conditions 1, 3 and 5

offices_score = add_score(offices, 1)
offices.to_csv('./data/offices_score.csv')

offices_score = add_score(offices_score, 3)
offices.to_csv('./data/offices_score.csv')

offices_score = add_score(offices_score, 5)
offices.to_csv('./data/offices_score.csv')

# Selecting the Top 200 companies

offices_score = total_score(offices_score)
top_offices = offices2[:200].copy(deep = True)
top_offices.reset_index(drop=True, inplace=True)

# Adding the other scores

top_offices = add_score(top_offices, 2)
top_offices.to_csv('./data/topoffices_score.csv')

top_offices = add_score(top_offices, 4)
top_offices.to_csv('./data/topoffices_score.csv')

top_offices = add_score(top_offices, 6)
top_offices.to_csv('./data/topoffices_score.csv')

top_offices = add_score(top_offices, 7)
top_offices.to_csv('./data/topoffices_score.csv')

top_offices = add_score(top_offices, 8)
top_offices.to_csv('./data/topoffices_score.csv')

top_offices = add_score(top_offices, 9)
top_offices.to_csv('./data/topoffices_score.csv')

#Final Score

top_offices = total_score(top_offices)
top_offices.to_csv('./data/topoffices_score.csv')

print(top_offices.head(3))

# Plotting

pl = input("Do you want to plot the offices(y/n)?")
if pl = "y":
    from src.plot import plot_map, to_dic

    loc1 = to_dic(top_offices, 0)
    loc2 = to_dic(top_offices, 1)
    loc3 = to_dic(top_offices, 2)

    loc1_map = plot_map(loc1, save=True)
    loc2_map = plot_map(loc2, save=True)
    loc3_map = plot_map(loc3, save=True)