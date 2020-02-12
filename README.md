## New York City Lead Locator


### The New York City Lead Locator is an application that uses public housing and U.S. Census records to predict the locations of lead water service lines in New York City. 


#### Link to the web app: http://nyc-lead-water-service.herokuapp.com/ 


#### The data used in this project:


* [Lead Service Lines](https://data.cityofnewyork.us/Environment/Lead-Service-Line-Location-Coordinates/bnkq-6un4 "Lead Service Line Locations")

* [Property Value/Tax Data](https://data.cityofnewyork.us/City-Government/Property-Valuation-and-Assessment-Data/yjxr-fw8i "Property")

* [Construction Year Data](https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh "Construction Year")

* [American Community Survey](https://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml "ACS")


#### Descriptions of files in this repository:
 
**app.py** - File to create a Dash-based web app deployed to Heroku (see link to web app above)
 
**obtaining_the_data.ipynb** - Jupyter notebook outlining the API use and cleaning the data. Plus geospatial feature engineering.
 
**model_evaluation.ipynb** - Jupyter notebook using the prepared dataset for training models with logistic regression, random forest, and naive Bayes.
