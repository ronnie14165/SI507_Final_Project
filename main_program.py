import json
import construct_yelp_json
import secrets
import requests

max_rating = 0


class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def findMax(self):
        if self.right:
            self.right.findMax()
        else:
            global max_rating
            max_rating = self.data


def line(k = 1):
    for p in range(k):
        for q in range(117):
            print("=", end="")
        print("")


line(2)
print("Welcome to mini-Yelp application. In this application, you can search for restaurants  based on personal "
      "preferences.")
line(2)
f = open('data.json')
data = json.load(f)
city_list = construct_yelp_json.city_list
print("Now, we support to search chinese restaurant in the following cities:")
index = 1
for i in city_list:
    print(i, end = "      ")
    if index % 5 == 0:
        print(" ")
    index += 1
my_city = input("Where do you want to eat? ")
# my_city = "Lansing, MI"
if my_city not in city_list:
    print("Sorry, we don't support to search chinese restaurant in this city.")
    print("Please choose a city on the list")
else:
    index = 1
    print("There are some restaurants we found in our system in", my_city)
    print("%-5s\t%-20s\t" % ("Index", "Restaurant Name"))
    line()
    for i in data['yelp'][my_city]:
        print("%-5s\t%-20s\t" % (index, i['name']))
        index += 1
    line()
    if_rating = input("Do you want to use rating to filter restaurants? Press 'y' for yes, other for no: ")
    # if_rating = 'y'
    if if_rating == 'y':
        print("There are some recommendations for you.")
        rating_list = []
        for i in data['yelp'][my_city]:
            rating_list.append(i["rating"])
        this_list = rating_list
        de_duplication_list = list(set(this_list))
        new_list = []
        for i in de_duplication_list:
            a = 10 * i
            new_list.append(int(a))
        root = Node(new_list[0])
        for i in range(1, len(new_list)):
            root.insert(new_list[i])
        root.findMax()
        max_rating = max_rating / 10
        print("The highest ranking based on address of your choice is",max_rating)
        print("The restaurant(s) info as follow:")
        print("%-40s\t%-50s\t%-30s\t" % ("Restaurant Name", "Restaurant Address", "Rating"))
        for i in data['yelp'][my_city]:
            rating_list.append(i["rating"])

            if i["rating"] == max_rating:
                address = ""
                if i['location']['address1'] is not None:
                    address = i['location']['address1']
                    if i['location']['address2'] is not None:
                        address += i['location']['address2']
                        if i['location']['address3'] is not None:
                            address += i['location']['address3']
                            if i['location']['city'] is not None:
                                address += ", " + i['location']['city']
                                if i['location']['state'] is not None:
                                    address += ", " + i['location']['state']
                                    if i['location']['zip_code'] is not None:
                                        address += ", " + i['location']['zip_code']
                    print("%-40s\t%-50s\t%-30s\t" % (i['name'], address, i["rating"]))

    else:
        if_detail = input("Do you want to more info about those restaurants? Press 'y' for yes, other for no: ")
        if if_detail == 'y':
            print("%-40s\t%-50s\t%-30s\t" % ("Restaurant Name", "Restaurant Address", "Rating"))
            for i in data['yelp'][my_city]:
                address = ""
                if i['location']['address1'] is not None:
                    address = i['location']['address1']
                    if i['location']['address2'] is not None:
                        address += i['location']['address2']
                        if i['location']['address3'] is not None:
                            address += i['location']['address3']
                            if i['location']['city'] is not None:
                                address += ", " + i['location']['city']
                                if i['location']['state'] is not None:
                                    address += ", " + i['location']['state']
                                    if i['location']['zip_code'] is not None:
                                        address += ", " + i['location']['zip_code']
                print("%-40s\t%-50s\t%-30s\t" % (i['name'], address, i["rating"]))
    if_exchange_rate = input("Before ending the application, would you pay in another currency? Like CNY, GBP or Euro？Press 'y' for yes, other for no: ")
    if if_exchange_rate == 'y':
        print(1)
        host = "https://v6.exchangerate-api.com/v6/"
        params = "latest/USD"
        url = host + secrets.exchange_rate_api + params
        response = requests.get(url)
        dict = response.json()
        json_file = json.dumps(dict)
        text_file = open("exchange_rate_data.json", "w")
        text_file.write(json_file)
        text_file.close()

        f = open('exchange_rate_data.json')
        data = json.load(f)
        print("The currency we support are as follow:")
        currency_list = []
        for i in range(len(data['conversion_rates'])):
            key, value = list(data['conversion_rates'].items())[i]
            currency_list.append(key)
        num = 0
        for i in currency_list:
            print(i, end="   ")
            num += 1
            if num % 10 == 0:
                print("")

        currency = input("What currency would you pay? Please input like CNY: Press 'y' for yes, other for no: ")
        price = input("How much did you spend？In USD: ")
        if currency in currency_list and price.isnumeric():
            payment = int(price) * float(data['conversion_rates'][currency])
            print("Based on real time exchange rates, the payment is", payment, currency)
        else:
            print("Sorry, we don't support exchange of this currency yet.")

line()
print("Thanks for using mini-Yelp! ")
line()



