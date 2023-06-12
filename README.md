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
python restaurant.py

Username:admin
Password:admin
                          RESTAURANT MENU SYSTEM
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice:
```

## 1. Display Menu
```
Display Menu
╭──────┬───────────────────────────┬───────────────┬─────────╮
│   Id │ Name                      │ Description   │   Price │
├──────┼───────────────────────────┼───────────────┼─────────┤
│    1 │ Tomato Soup               │ Tomato Soup   │      50 │
│    2 │ Veg clear soup            │ Veggie Soup   │      55 │
│    3 │ Vegetable Hot N Sour Soup │ Veg sour soup │      55 │
│    4 │ Vegetable Manchow Soup    │ manchow soup  │      60 │
│    5 │ Paneer Tikka              │ Tikka         │      70 │
│    6 │ Paneer Manchurian         │ manchurin     │      70 │
│    7 │ Veg Nuggets               │ Nuggets       │      75 │
│    8 │ Mushroom Salt and Pepper  │ mushroom      │      70 │
│    9 │ Veg Salad                 │ Simple Salad  │     100 │
│   10 │ Veg Pasta Salad           │ pasta salad   │     110 │
│   11 │ Kesribath                 │ Kesribath     │      25 │
│   12 │ Kharabath                 │ Kharabath     │      25 │
│   13 │ Shavige                   │ Shavige       │      20 │
╰──────┴───────────────────────────┴───────────────┴─────────╯
Back to Menu? [y/n]
```
## 2.Add Items to Menu
```
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:2

Food item name:Dumroot
Cost:30
Quantity:100
inv.id:14
Any more items?[y/n]
Any more items?[y/n]y
Food item name:Mysore Pak
Cost:10
Quantity:100
inv.id:15
Any more items?[y/n]n
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:1
Display Menu
╭──────┬───────────────────────────┬───────────────┬─────────╮
│   Id │ Name                      │ Description   │   Price │
├──────┼───────────────────────────┼───────────────┼─────────┤
│    1 │ Tomato Soup               │ Tomato Soup   │      50 │
│    2 │ Veg clear soup            │ Veggie Soup   │      55 │
│    3 │ Vegetable Hot N Sour Soup │ Veg sour soup │      55 │
│    4 │ Vegetable Manchow Soup    │ manchow soup  │      60 │
│    5 │ Paneer Tikka              │ Tikka         │      70 │
│    6 │ Paneer Manchurian         │ manchurin     │      70 │
│    7 │ Veg Nuggets               │ Nuggets       │      75 │
│    8 │ Mushroom Salt and Pepper  │ mushroom      │      70 │
│    9 │ Veg Salad                 │ Simple Salad  │     100 │
│   10 │ Veg Pasta Salad           │ pasta salad   │     110 │
│   11 │ Kesribath                 │ Kesribath     │      25 │
│   12 │ Kharabath                 │ Kharabath     │      25 │
│   13 │ Shavige                   │ Shavige       │      20 │
│   14 │ Dumroot                   │ Dumroot       │      30 │
│   15 │ Mysore Pak                │ Mysore Pak    │      10 │
╰──────┴───────────────────────────┴───────────────┴─────────╯
Back to Menu? [y/n]y
```
## 3 Reserve
```agsl
Enter your Choice[1-9]:5
Current reservation orders and table occupancies:[]
No reservations made!
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:3
Enter phone number:9986026076
Enter table:8
order_id:2 at table:8
```
## 4. Add  Items to order
```agsl
Enter your Choice[1-9]:4
Enter reservation order id:2
Enter item name:Kharabath
enter item qty:7
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:4
Enter reservation order id:2
Enter item name:15  
enter item qty:6
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:4
Enter reservation order id:2
Enter item name:11
enter item qty:4
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:6
Enter reservation order id:2
Current reservations and table occupancy
╭────────────┬───────╮
│ name       │   qty │
├────────────┼───────┤
│ Kesribath  │     4 │
│ Kharabath  │     7 │
│ Mysore Pak │     6 │
╰────────────┴───────╯
Back to Menu? [y/n]
```
## 5. Show Orders
```
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:5
Current reservation orders and table occupancies
╭────────────────┬──────┬────────┬────────────┬─────────────────────╮
│   table_number │   id │ name   │      phone │ datetime            │
├────────────────┼──────┼────────┼────────────┼─────────────────────┤
│              4 │    1 │ Subbu  │ 9986026076 │ 2023-06-12 16:12:41 │
╰────────────────┴──────┴────────┴────────────┴─────────────────────╯
Back to Menu? [y/n]y
```
## 6. Show Order Items
```
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:6
Enter reservation order id:1
Current reservations and table occupancy
╭───────────────────────────┬───────╮
│ name                      │   qty │
├───────────────────────────┼───────┤
│ Tomato Soup               │    10 │
│ Vegetable Hot N Sour Soup │     7 │
│ Paneer Tikka              │     4 │
│ Kharabath                 │     4 │
╰───────────────────────────┴───────╯
Back to Menu? [y/n]y
```
## 7. Print Bill
```
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:7
Enter reservation order id:1
|----------------------------------------------------------------------------------
| HOTEL KRISHNA VILASA, Kulur Ferry Rd, Urwa, Mangaluru 575006. phone = 9591241675|
|----------------------------------------------------------------------------------
| BILL:1                                                         Date:  2023-06-12|
|----------------------------------------------------------------------------------
+---------------------------+-------+--------+
| name                      |   qty |   cost |
+===========================+=======+========+
| Tomato Soup               |    10 |    500 |
+---------------------------+-------+--------+
| Vegetable Hot N Sour Soup |     7 |    385 |
+---------------------------+-------+--------+
| Paneer Tikka              |     4 |    280 |
+---------------------------+-------+--------+
| Kharabath                 |     4 |    100 |
+---------------------------+-------+--------+
| Total(Rs)                 |    25 |   1265 |
+---------------------------+-------+--------+
|----------------------------------------------------------------------------------
```
## 8. Clear Table
```
Back to Menu? [y/n]y
1. Display Menu
2. Add Items To Menu
3. Reserve 
4. Add item to Reservation. 
5. Show Orders. 
6. Show Order Items. 
7. Print Bill 
8. Clear Table 
9. Log out
Enter your Choice[1-9]:8
Enter table:4
Clearing the table 4 & corresponding inventory
```
## 9. Log out
```agsl

```

