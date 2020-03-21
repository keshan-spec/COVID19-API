## COVID-19 API 
This API was built on Python and Node js, it has some
functionality. This was mainly made for informative purposes. 

## Getting started
You will need to install the dependencies for Node js 
``npm install``

And also run ``pip install -r requirements.txt``

## Usage
Here are the available routes to this API
````
GET - /updates            => returns a json of the global numbers about the virus
GET - /show/:countryname  => returns a json of the numbers of the  given country
GET - /show/all           => returns a huge json of 180+ countries current state
GET - /show/stats/:opt    => returns the query opt given, ex; death, returns the country and deaths that are at the highest currently
````

## Data
All data is scraped from [worldmeters website](https://www.worldometers.info/coronavirus/)
 
 

**Author** _[keshan-spec](https://github.com/keshan-spec/)_