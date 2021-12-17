# SI507_Final_Project: mini-Yelp

## Project code
Link to github repo for project code: https://github.com/ronnie14165/SI507_Final_Project.   

The required README file are posted on github.    

The required Python packages for the project is: requests. 

## Data sources
### [Yelp Fusion](https://fusion.yelp.com/):
In this application, I use yelp fusion as one of the main data sources. After caching data through this api, I build a binary search tree to judge the highest rating restaurants, according to whether the user refers to the ranking.    

Two python files access the information through those two api: construct_yelp_json.py and construct_exchange_rate_json.py and two json files store those data locally.       


The number for records in yelp json file is about 500, in exchange rate json file is about 200.      


In the yelp json file, the information about restaurant location, rating, address1-3, zip_code, alias, name are important in this application. In the exchange rate json file, only the certain rate that the user chooses is critical.  




### [Exchange rate api](https://www.exchangerate-api.com/):
I chose this api as a part of the data resource because sometimes, foreign tourists do not have enough local currency when traveling, so they can only use a credit card to pay in the local currency at the real-time exchange rate(lots of companies support this). So, using this api to calculate the payment regarding their currency gives them a more intuitive dining experience.

## Interaction and Presentation Options
Description of the user-facing capabilities : At the beginning, there is a brief introduction about this application, it tells users to choose one city among the city list. After the user has done that, the system will list all the corresponding Chinese restaurants it has in the system. Then, ask the user if he(she) needs the recommendation system, which is, using the binary search tree to find the best restaurant according to the rating, then post it on the screen, with its name, address and rating. Later, ask the user if he(she) needs to pay in another currency, like CNY, GBP or Euro. If so, the system would ask the user what kind of currency he(she) has and how much USD is spent, finally giving the amount of corresponding payment the user should pay with the currency he(she) chooses, based on real time exchange rate.    

About the user input, while asking a question about yes or no, the user presses ‘y’ for yes and the other for no. Asking questions about choosing one item among some choices, the user input should be exactly one of the choices.

## [Demo Link](http://www.google.com/)

