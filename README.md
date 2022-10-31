# Best Location for a Gamming Company

## Basic Information:
- Author: Sergi Portolés
- Project III for the Data Analytics Bootcamp in Ironhack (geospatial data)

## Main Objective of the Project:

Find the best location for a Gaming Company given the following conditions:

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, give them some place to go party.
- The CEO is vegan.
- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.
- The office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.

Company staff:

- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 1 Maintenance guy that loves basketball
- 10 Executives
- 1 CEO/President.

## Data Sources Used:
| Source   |      Type      |  Data extracted  |
|----------|:-------------:|------:|
| [Crunchbase](https://www.crunchbase.com/)|  MongoDB<sup>1</sup> | Database of start-ups |
| [Foursquare](https://foursquare.com/) | API | Places near location |
|[Bing](https://www.bing.com/)|Web Scrapping|Seacrh for Booking URL for a certain city
| [OurAirports](https://ourairports.com/) | CSV<sup>1</sup> | Airport location database |
 
<sup>1</sup> Files not included in the repository
 
## Python Libraries Used:
 
| Library   |      Use     |
|----------|:-------------:|
| Pandas | Data Frame manipulation |
| Requests | HTTP Calls |
| Pymongo | MongoDB queries |
| Time | Sleep Function |
| Urllib | Url encode |
| dotenv | Import tokens |
| Os | Set paths |
| Tqdm | Show progress bar |

## File Structure:

### *main.py*

Python file that returns the best 3 locations <sup>1</sup>

<sup>1</sup>***Important**: Running this file might require a long processing time*

### ./src/

- ***criteria.py*** &rarr; This file generates all the paramters used to evaluate the locations
- ***database.py*** &rarr; This file contains the functions to generate and save (csv format) the datasets for the condition 1, 3 and 5
- ***queries.py*** &rarr; This file contains the functions needed to query MongoDB and Foursquare API
- ***score.py***  &rarr; This file contains all the functions needed to calculate the score of each location

### ./data/

This folder contains all the databases generated in format csv:
- World Airports database
- Companies that raised more than 1 million USD database
- Offices for design companies database
- Offices locations database
- Offices locations database with scores for conditions 1, 3 and 5
- Top 200 offices locations database with total score
## Criteria to Find the Best Locations

### Initial considerations:

1. All the workers are considered equal (including the dog)
2. The closest is a location the better
3. The more locations that meet the criteria the better until a maximum number where more locations do not give an extra value

With this consideration a formula was generated

### Score formula

![Score Formula](./img/score-function.png)

**condition(x)** &rarr; Conditions score from x=1 to x=9.

**ocu** &rarr; Number of occurrences for a given condition to a maximum "max(ocu)".

**max(ocu)** &rarr; Maximum number of locations that are considered enough to satisfy a given condition.

**dis** &rarr; Distance between two locations.

**min(dis)** &rarr; Minimum distance from the location and places that meet the condition.

**min(dis)** &rarr; Maximum distance from the location that can be situated a place that meets the condition.

**people** &rarr; Number of people in the company that satify a given condition

**max(score)** &rarr; The maximum score possible of the sum of all conditions score

![Total](./img/total-score-formula.png)

## Process to Find the Best Locations:

### 1. Definig Conditions Parameters:

### 2. Generating Databases for conditions 1, 3 and 5

1) Upload crunchbase database to MongoDB
2) Query MongoDB
3) Clean queries to generate a list of offices locations (10,743 entries)
4) Clean queries to generate a list of offices from Design companies (498 entries)
5) Clean queries to generate a list of offices from companies that raised more than 1 million USD (3,253 entries)
6) Download and clean database of airports from [OurAirports](https://ourairports.com/) (8,636 entries)

### 3. Calculating Score Using the Conditions 1, 3 and 5

Using the database of offices the score formula is applied for the conditions 1, 3 and 5

### 4. Get the 200 offices locations with best score
* Sort the new offices database by Total Score (conditon1 + condition3 + condition5)

### 5. Query FourSquare to Calculate the Total Score of the Top 200

* Using the FourSquare API retrive the locations that meet the criteria of the conditions 2, 4 , 6, 7, 8 and 9
* Apply the score formula to get the Final total Score.

### 6. Selecting the Top 3 Locations
* The 2 Location with higher score
* Location with higher score that meet all the conditions

## Final Result



## Future Improvements:
- Improve efficieny of the code.
- Make easier to modify the parameters of the search.
- Update the company database.
- Use a better API than Foursquare to find locations