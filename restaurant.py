#!/usr/bin/env python

import pickle
from tabulate import tabulate
from datetime import date
import mysql.connector
import datetime
import random as rd
import matplotlib.pyplot as plt
import argparse

######VENKAT-CODE-BEGIN#############
# DB Connection
def connect(user, pswd):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='restaurant_mgmt',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection
        else:
            print("No connection")

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)

# Close DB Connection
def close(connection):
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    else:
        print("MySQL connection already closed")

# List Menu Items
def list_menu(connection):
    cursor = connection.cursor()
    cursor.execute("select * from menu;")
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        print("name:" + row[1])
        print("price:%.2f"% row[3])
    cursor.close()
    return records

# Add Menu Item
def add_menu(connection, item, menu_price):
    cursor = connection.cursor()
    cursor.execute("insert into menu(name, description, price) values(%s,%s,%s);", (item, item, menu_price))
    menu_id = cursor.lastrowid
    cursor.close()
    connection.commit()
    return menu_id

# Delete from Menu
def del_menu(connection, menu_name):
    cursor = connection.cursor()
    cursor.execute("delete from menu where name = %s;", menu_name)
    connection.commit()
    cursor.close()

# Update inventory with quantity for a agiven menu_item
def update_inventory(connection, menu_name, menu_qty):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select id from menu where name = %s;", (menu_name,))
    rec=cursor.fetchone()
    print("inv.id:%s"% rec['id'])
    menu_id = rec['id']
    cursor.execute("insert into  inventory (menu_id, qty) values (%s, %s) on duplicate key update qty=%s;", (menu_id, menu_qty, menu_qty))
    connection.commit()
    cursor.close()

# Display Menu
def display_menu(connection):
    print("Display Menu")
    cursor = connection.cursor()
    cursor.execute("select * from menu;")
    records = cursor.fetchall()
    print(tabulate(records, headers=["Id", "Name", "Description", "Price"], tablefmt='rounded_outline'))
    #for (id, name, description, price) in cursor:
    #    print("%s, %s, %s, %s" % (id, name, description, price))
    cursor.close()

# Display inventory to know the current availability
def display_inventory(connection):
    print("Display Inventory")
    cursor=connection.cursor()
    cursor.execute("select name, qty from menu,inventory where menu.id=inventory.menu_id;")
    records = cursor.fetchall()
    print(tabulate(records, headers=["Name", "Quantity"], tablefmt='rounded_outline'))
    cursor.close()


# Change inventory given menu item and quantity
def change_inventory(connection, menu_item_id, incr_decr_qty):
    cursor = connection.cursor()
    cursor.execute("update inventory set qty = qty + %s  where menu_id = %s;", (incr_decr_qty, menu_item_id))
    connection.commit()
    cursor.close()

# Reserve a table
def reserve(connection, customer_identification, table_number):
    cust_id = -1;
    cursor = connection.cursor()
    cursor.execute("select id from customer where lower(name) = lower(%s) OR phone = %s", (customer_identification, customer_identification))
    cust_rec = cursor.fetchone()
    if cust_rec is None:
        print ("Welcome %s to the restaurant. Requesting few more details:", customer_identification)
        name = input("Enter customer name:")
        phone = input("Enter phone number:")
        address = input("Enter address:")
        cursor.execute("insert into customer values(%s, %s, %s)", (name, phone, address))
        cust_id = cursor.lastrowid()
        connection.commit()
    else:
        print("Welcome %s for returning visit", customer_identification)
        cust_id = cust_rec[0];
    cursor.execute("insert into reservation_order(customer_id, table_number) values(%s, %s)",(cust_id, table_number))
    connection.commit()
    cursor.close()
    print("order_id:%s at table:%s" % (cursor.lastrowid, table_number))
    return cursor.lastrowid

# Show all reservation orders
def show_orders(connection):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select table_number, reservation_order.id, customer.name, customer.phone, datetime from customer, reservation_order where customer.id=reservation_order.customer_id;")
    records = cursor.fetchall()
    print("Current reservation orders and table occupancies:%s" % records)
    if len(records)>0:
        header = records[0].keys()
        rows =  [x.values() for x in records]
        print(tabulate(rows, header, tablefmt='rounded_outline'))
    else:
        print("No reservations made!")
    cursor.close()


# Clear Reservation
def clear_table(connection, table):
    cursor = connection.cursor()
    cursor.execute("delete from reservation_order where table_number=%s;", (table,))
    connection.commit()
    cursor.close()
    print("Clearing the table %d & corresponding inventory" % table)

# Add menu items along with their quantities
def add_order_item(connection, order_id, menu_name, item_qty):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select menu_id, qty from inventory where menu_id = (select id from menu where lower(name) = lower(%s) OR id = %s);", (menu_name, menu_name))
    record = cursor.fetchone()
    cursor.close()

    if record is None:
        print("No inventory found for %s and hence could not be added to order" % menu_name)
        return

    menu_item_id = record['menu_id']
    existing_qty = record['qty']

    cursor = connection.cursor(buffered=True , dictionary=True)
    if existing_qty > item_qty:
        cursor.execute("insert into order_item values(%s,%s,%s) on duplicate key update qty=%s;", (order_id, menu_item_id, item_qty, item_qty))
        change_inventory(connection, menu_item_id, -item_qty)
    else:
        print("Sorry %s is not avialable" % menu_name)
    connection.commit()
    cursor.close()


# List order items
def list_order_items(connection, order_id):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select name, qty from menu, order_item where order_item.order_id=%s and menu.id=order_item.menu_id;", (order_id,))
    records = cursor.fetchall()
    cursor.close()
    print("Current reservations and table occupancy")
    header = records[0].keys()
    rows =  [x.values() for x in records]
    print(tabulate(rows, header, tablefmt='rounded_outline'))

# Count orders
def count_orders(connection, day_start, day_end):
    if day_end == '' or day_end is None:
        day_end = day_start
    print ("Orders for the day:[%s - %s]" % (day_start, day_end))
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select count(*) as no_of_orders, sum(cost) as revenue, (sum(cost)/count(*)) as avg_revenue from reservation_order where date(datetime) between %s and %s;",
                   (day_start, day_end))
    records = cursor.fetchall()
    cursor.close()
    return records

    # Print Bill
def print_bill(connection, order_id):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select name, qty, (price*qty) as cost  from menu, order_item where menu.id=order_item.menu_id and order_item.order_id=%s;",(order_id,))
    records = cursor.fetchall()

    total_cost = 0.0
    total_qty = 0
    print("+============================================+")
    print("|    HOTEL KRISHNA VILASA, Kulur Ferry Rd,   |")
    print("| Urwa, Mangaluru 575006. phone = 9591241675 |")
    print("+--------------------------------------------+")
    print("| BILL NO:%s                 Date:  %s|" % (order_id, date.today()))
    #print("+--------------------------------------------+")
    for row in records:
        total_cost +=  float(row['cost'])
        total_qty  +=  row['qty']
    rows =  [x.values() for x in records]
    rows.append(['Total(Rs)', total_qty, total_cost])
    #       +============================================+
    header=["          Name         ","Qty","Cost"]
    print(tabulate(rows, header, tablefmt='grid'))
    cursor.execute("update reservation_order set cost=%s where id=%s", (total_cost, order_id))
    connection.commit()
    cursor.close()
    #print("|------------------------------------------------|")
######VENKAT-CODE-END###############
# MAIN PROGRAM
def main():
    parser = argparse.ArgumentParser(description='Restaurant Booking System')
    parser.add_argument('-u', '--user',      required=True, help="Enter user name to manage the restaurant booking and billing")
    parser.add_argument('-p', '--password', required=True, help="Enter password to manage the restaurant booking and billing")
    args = parser.parse_args()
    print("args:%s" % args)
    name='Subramhanya'
    pass_word=args.password
    user_name=args.user

    admin = connect(user_name,pass_word);

    if pass_word=='admin' and user_name=='admin':   #change password here
        q ='y'
        print('Hello', name)
        print("\t\t\t\t\tRESTAURANT MENU SYSTEM")
        while q == 'y':
            print("1. Display Menu\n2. Add Items To Menu\n3. Reserve \n4. Add item to Reservation. \n5. Show Orders. \n6. Show Order Items. \n8. Clear Table \n9. Log out")
            f=int(input("Enter your Choice[1-9]:"))
            if f == 2:
                # get the name, address, and phone number of the restaurant
                ans = 'y'
                while ans == 'y':
                    try:
                        name = input("Food item name:")
                        marks = int(input("Cost:"))
                        menu_qty = int(input("Quantity:"))
                        rno = add_menu(admin, name, marks)
                        update_inventory(admin, name, menu_qty)
                        ans = input("Any more items?[y/n]")
                    except:
                        print('There was an error!')
                        ans = input("Do you want to quit adding this item? [y/n]:")

                q = input("Back to Menu? [y/n]")

            elif f == 1:
                display_menu(admin)
                q = input("Back to Menu? [y/n]")
            elif f==3 :
                customer_identification= input("Enter phone number:")
                table_number = int(input("Enter table:"))
                order_id = reserve(admin, customer_identification, table_number)
                q = input("Back to Menu? [y/n]")
            elif f==4 :
                more_items = 'y';
                order_id = input("Enter reservation order id:")
                while more_items=='y':
                    menu_name = input("Enter item name:")
                    qty = int(input("Enter item qty:"))
                    add_order_item(admin, order_id, menu_name, qty)
                    more_items = input("Add another item[y/n]:")
                q = input("Back to Menu? [y/n]")
            elif f==5:
                show_orders(admin)
                q = input("Back to Menu? [y/n]")
            elif f==6:
                order_id = input("Enter reservation order id:")
                list_order_items(admin, order_id)
                q = input("Back to Menu? [y/n]")
            elif f==7:
                order_id = input("Enter reservation order id:")
                print_bill(admin, order_id)
                q = input("Back to Menu? [y/n]")
            elif f==8:
                table = int(input("Enter table:"))
                clear_table(admin, table)
                q = input("Back to Menu? [y/n]")
            elif f==9:
                print('Succesfully logged off')
                close(admin)
                q='n'
        close(admin)

    if pass_word=='cashier' and user_name=='cashier':#change password for waiter here
        connection = connect(user_name, pass_word)
        q ='y'
        print('Hello', name)
        print("\t\t\t\t\tRESTAURANT MENU SYSTEM")
        while q == 'y':
            print("11. Print Bill\n12. Revenue and Footfall\n13. Plot revenue. \n9. Log out")
            f=int(input("Enter your Choice[1-9]:"))
            if f==11:
                order_id = input("Enter reservation order id:")
                print_bill(connection, order_id)
                q = input("Back to Menu? [y/n]")
            elif f==12:
                day = input("Enter the day to count orders:")
                if day == '' or day is None:
                    day=date.today()
                records = count_orders(connection, day, day)
                header = records[0].keys()
                rows =  [x.values() for x in records]
                print(tabulate(rows, header, tablefmt='grid'))
                q = input("Back to Menu? [y/n]")
            elif f==13:
                day_start = input("Enter Start date:")
                day_end = input("Enter End date:")
                records = count_orders(connection, day_start, day_end)
                header = records[0].keys()
                rows =  [x.values() for x in records]
                print(tabulate(rows, header, tablefmt='grid'))
                q = input("Back to Menu? [y/n]")
            elif f==9:
                close(connection)
                q='n'
        close(connection)

        ### plt.bar(gry, grx)

        # Add a title and label the axes
        ### plt.title('Revenue today')
        ### plt.ylabel('Collected amount')
        ### plt.xlabel('Order number')

        # Show the plot
        ### plt.show()
if __name__=="__main__":
    main()