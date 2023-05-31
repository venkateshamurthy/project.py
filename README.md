# project.py
This is a restaurant billing system

## DB Setup
After logging in to MySql first do
```
source ./data.sql;
source ./values.sql;
```
## Ensure below python libraries installed
```
pip install argparse
pip install matplotlib
pip install argparse
pip install mysql
Add any other as required
```
## Main Program help
```
./resto -h
usage: resto [-h] {add-menu,show-menu,show-inv,show-bill,reserve,add-item,clear-table,show-orders} ...

Restaurant Booking System

positional arguments:
{add-menu,show-menu,show-inv,show-bill,reserve,add-item,clear-table,show-orders}
add-menu            Add menu items to restaurant with name and price
show-menu           Show menu of the restaurant
show-inv            Show the inventory quantities
show-bill           Prepare Bill
reserve             Reserve the table
add-item            Add menu items to the reservation order
clear-table         Clear Table Reservation
show-orders         Show All Reservation Orders

options:
-h, --help            show this help message and exit
```
## Show Menu --help
```
 ./resto show-menu -h
usage: resto show-menu [-h]

positional arguments:
  show-menu

options:
  -h, --help  show this help message and exit
  ```

## Add to menu --help
```
./resto add-menu -h
usage: resto add-menu [-h] -m MENU -p PRICE -q QTY

options:
  -h, --help            show this help message and exit
  -m MENU, --menu MENU  Menu or the dish name itself such as say "keribath"
  -p PRICE, --price PRICE
                        Price per unit
  -q QTY, --qty QTY     Quantity to replenish
```
## Show Menu
```
./resto show-menu

args:Namespace(command='show-menu', **{'show-menu': True})
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)
Display Menu

1, Tomato Soup, Tomato Soup, 50.00
2, Veg clear soup, Veggie Soup, 55.00
3, Vegetable Hot N Sour Soup, Veg sour soup, 55.00
4, Vegetable Manchow Soup, manchow soup, 60.00
5, Paneer Tikka, Tikka, 70.00
6, Paneer Manchurian, manchurin, 70.00
7, Veg Nuggets, Nuggets, 75.00
8, Mushroom Salt and Pepper, mushroom, 70.00
9, Veg Salad, Simple Salad, 100.00
10, Veg Pasta Salad, pasta salad, 110.00
11, Kesribath, Kesribath, 25.00
MySQL connection is closed
```


## Show inventory
```
./resto show-inv

args:Namespace(command='show-inv', **{'show-inv': True})
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)

Display Inventory
Kesribath, 95
Mushroom Salt and Pepper, 1000
Paneer Manchurian, 760
Paneer Tikka, 546
Tomato Soup, 487
Veg clear soup, 300
Veg Nuggets, 900
Veg Pasta Salad, 2000
Veg Salad, 1486
Vegetable Hot N Sour Soup, 400
Vegetable Manchow Soup, 250
MySQL connection is closed
```

## Add to menu
```
./resto add-menu -mKharabath -p20.0 -q100
args:Namespace(command='add-menu', menu='Kharabath', price=20.0, qty=100)
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)
Kharabath, 20.0, 100
inv.id:12
Menu Items:
Display Menu

1, Tomato Soup, Tomato Soup, 50.00
2, Veg clear soup, Veggie Soup, 55.00
3, Vegetable Hot N Sour Soup, Veg sour soup, 55.00
4, Vegetable Manchow Soup, manchow soup, 60.00
5, Paneer Tikka, Tikka, 70.00
6, Paneer Manchurian, manchurin, 70.00
7, Veg Nuggets, Nuggets, 75.00
8, Mushroom Salt and Pepper, mushroom, 70.00
9, Veg Salad, Simple Salad, 100.00
10, Veg Pasta Salad, pasta salad, 110.00
11, Kesribath, Kesribath, 25.00
12, Kharabath, Kharabath, 20.00

Inventory:
Display Inventory
Kesribath, 95
Kharabath, 100
Mushroom Salt and Pepper, 1000
Paneer Manchurian, 760
Paneer Tikka, 546
Tomato Soup, 487
Veg clear soup, 300
Veg Nuggets, 900
Veg Pasta Salad, 2000
Veg Salad, 1486
Vegetable Hot N Sour Soup, 400
Vegetable Manchow Soup, 250
MySQL connection is closed
```

## Reserve a table (--help)
```
./resto reserve -h
usage: resto reserve [-h] -i IDENTIFICATION -t TABLE

options:

-h, --help            show this help message and exit

-i IDENTIFICATION, --identification IDENTIFICATION

                        Customer name or phone number

-t TABLE, --table TABLE

                        Table number to reserve for the customer
```
## Reserve a table
```
./resto reserve -i9986026076 -t6

args:Namespace(command='reserve', identification='9986026076', table=6)
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)
order_id:3 at table:6
order id:3
MySQL connection is closed
```


## Adding a menu item to an reservation order
```
./resto add-item -o3 -m"paneer manchurian" -q5
args:Namespace(command='add-item', order=3, menu='paneer manchurian', qty=5)
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)
Current reservations and table occupancy

Tomato Soup, 3
Paneer Tikka, 5
Paneer Manchurian, 5
Veg Nuggets, 5
Veg Salad, 5
Kesribath, 7
Kharabath, 12
MySQL connection is closed
```


## Show Bill (--help)
```
./resto show-bill -h

usage: resto show-bill [-h] -o ORDER



options:

-h, --help            show this help message and exit

-o ORDER, --order ORDER

                        Enter the order id
```
## Show Bill
```
./resto show-bill --order 3

args:Namespace(command='show-bill', order=3)
Connected to MySQL Server version  8.0.33
You're connected to database:  ('restaurant_mgmt',)
|----------------------------------------------------------------------------------
| HOTEL KRISHNA VILASA, Kulur Ferry Rd, Urwa, Mangaluru 575006. phone = 9591241675|
|----------------------------------------------------------------------------------
| BILL:3                                                         Date:  2023-05-31|
|----------------------------------------------------------------------------------
| Item                                                           |Qty|    Cost(Rs)|
|----------------------------------------------------------------------------------
| Tomato Soup                                                    |  5|      250.00|
| Veg Salad                                                      |  5|      500.00|
| Kesribath                                                      |  5|      125.00|
| Tomato Soup                                                    |  3|      150.00|
| Paneer Tikka                                                   |  5|      350.00|
| Paneer Manchurian                                              |  5|      350.00|
| Veg Nuggets                                                    |  5|      375.00|
| Veg Salad                                                      |  5|      500.00|
| Kesribath                                                      |  7|      175.00|
| Kharabath                                                      | 12|      240.00|
|----------------------------------------------------------------------------------
| Total(Rs)                                                      | 57|     3015.00|
|----------------------------------------------------------------------------------
MySQL connection is closed
```
