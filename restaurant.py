import pickle
from tabulate import tabulate
from datetime import date
import mysql.connector
import datetime
import random as rd
import matplotlib.pyplot as plt

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
    cursor = connection.cursor()
    cursor.execute("select id from customer where lower(name) = lower(%s) OR phone = %s", (customer_identification, customer_identification))
    cust_rec = cursor.fetchone()
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
    header = records[0].keys()
    rows =  [x.values() for x in records]
    print("Current reservation orders and table occupancies")
    print(tabulate(rows, header, tablefmt='rounded_outline'))
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



# Print Bill
def print_bill(connection, order_id):
    cursor = connection.cursor(buffered=True , dictionary=True)
    cursor.execute("select name, qty, (price*qty) as cost  from menu, order_item where menu.id=order_item.menu_id;")
    records = cursor.fetchall()
    cursor.close()
    total_cost = 0.0
    total_qty = 0
    print("|----------------------------------------------------------------------------------")
    print("| HOTEL KRISHNA VILASA, Kulur Ferry Rd, Urwa, Mangaluru 575006. phone = 9591241675|")
    print("|----------------------------------------------------------------------------------")
    print("| BILL:%s                                                         Date:  %s|" % (order_id, date.today()))
    print("|----------------------------------------------------------------------------------")
    #print("|%-64s|%3s|%12s|" % (' Item', 'Qty', 'Cost(Rs)'))
    #print("|----------------------------------------------------------------------------------")
    for row in records:
        #print("|%-64s|%3d|%12.2f|" % (" "+row['name'], row['qty'], row['cost']))
        total_cost +=  float(row['cost'])
        total_qty  +=  row['qty']
    #print("|----------------------------------------------------------------------------------")
    #print("|%-64s|%3s|%12.2f|" % (" Total(Rs)",total_qty,  total_cost))
    #records.append([{'name':'Total(Rs)'}, {'qty', total_qty}, {'cost':total_cost}])
    header = records[0].keys()
    rows =  [x.values() for x in records]
    rows.append(['Total(Rs)', total_qty, total_cost])
    print(tabulate(rows, header, tablefmt='grid'))
    print("|----------------------------------------------------------------------------------")
######VENKAT-CODE-END###############

name='Devdat'
registry={}
pass_word='error_password'



while pass_word=='error_password':
    user_name=input("Username:" )
    pass_word=input("Password:")

    admin = connect(user_name,pass_word);

    if pass_word=='admin' and user_name=='admin':   #change password here
        q ='y'
        print('Hello',name)
        print("\t\t\t\t\tRESTAURANT MENU SYSTEM")
        while q == 'y':
            print("1. Display Menu\n2. Add Items To Menu\n3. Reserve \n4. Add item to Reservation. \n5. Show Orders. \n6. Show Order Items. \n7. Print Bill \n8. Clear Table \n9. Log out")
            f=int(input("Enter your Choice:"))
            order_id = 0;
            if f == 2:


                # get the name, address, and phone number of the restaurant
                hotel_name = "HOTEL KRISHNA VILASA"   #Please Enter your restaurant name b/w "_".
                address = "Kulur Ferry Rd, Urwa, Mangaluru, Karnataka 575006"#address
                phone = "9591241675"#phone numbersh
                print("")
                # create a list of items and their corresponding prices
                main=[]
                #menufile = open("edit.dat", 'ab')#menu file m
                ans = 'y'
                while ans == 'y':
                    try:
                        #rno= int(input("order number:"))
                        name = input("Food item name:")
                        marks = int(input("Cost:"))
                        menu_qty = int(input("Quantity:"))
                        #Add read data
                        #lst = [rno, name, marks]
                        #pickle.dump(lst, menufile)
                        rno = add_menu(admin, name, marks)
                        update_inventory(admin, name, menu_qty)
                        ans = input("Any more items?[y/n]")
                    except:
                        print('There was an error!')
                        #rno= int(input("order number:"))
                        #name = input("Food item name:")
                        #marks = int(input("Cost:"))
                        #Add read data
                        #lst = [rno, name, marks]
                        #pickle.dump(lst, menufile)
                        ans = input("Do you want to quit adding this item? [y/n]:")
                #menufile.close()

                q = input("Back to Menu? [y/n]")

            elif f == 1:
                #Unpickling
                display_menu(admin)
                q = input("Back to Menu? [y/n]")
                #emp={}
                #empfile = open("edit.dat", 'rb')
                #try:
                    #lstmain1=[]
                    #while True:
                        #emp = pickle.load(empfile)
                        #lstmain1.append(emp)
                        #xyz = tabulate(lstmain1, headers=["Order no","Food item", "Cost"],tablefmt='rounded_outline')

                #except EOFError:
                    #empfile.close()
                    #print(xyz)
                    #q = input("Back to Menu? [y/n]")
            elif f==3 :
                customer_identification= input("Enter phone number:")
                table_number = int(input("Enter table:"))
                order_id = reserve(admin, customer_identification, table_number)
                q = input("Back to Menu? [y/n]")
            elif f==4 :
                order_id = input("Enter reservation order id:")
                menu_name = input("Enter item name:")
                qty = int(input("enter item qty:"))
                add_order_item(admin, order_id, menu_name, qty)
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

    elif pass_word=='cashier' and user_name=='cashier':#change password for waiter here
        print('Greetings!')
        hotel_name = "HOTEL KRISHNA VILASA"   #Please Enter your restaurant name b/w "_".
        address = "Kulur Ferry Rd, Urwa, Mangaluru, Karnataka 575006"#address
        phone = "9591241675"#phone number

        print("")

        #Unpickling
        #emp={}
        #empfile = open("edit.dat", 'rb')
        #try:
        #    lstmain1=[]
        #    while True:
        #       emp = pickle.load(empfile)
        #       lstmain1.append(emp)
        #except EOFError:
        #    empfile.close()


        #print(tabulate(lstmain1, headers=["Order no","Food item", "Cost"],tablefmt='rounded_outline'))
        #print("\tMenu")
        #print("-----------------")


        # create a loop to process multiple bills
        loop_bill = 'yes'
        count=0#number of customers
        amt=0#for total revenue
        client=1#order number
        gry=[]#graph data(y-axis)
        grx=[]#graph data(x-axis)
        while loop_bill == 'yes':
            # initialize a list to store the items and their corresponding quantities and prices for the current bill
            bill_items = []
            kot_bill=[]
            total_cost = 0

            # create a loop to add items to the bill
            next_item = 'y'
            #To see the order number of the customer
            print("» Order number",client)
            gry.append(str(client))

            while next_item == 'y':
                # get the order number and item details
                print()
                while True:
                    try:
                        item_number = int(input("Enter the item no: "))
                        item = lstmain1[item_number - 1][1]
                        cost = lstmain1[item_number - 1][2]
                        break
                    except:
                        print("Value error, item doesn't exist, please retry!")

                # ask the user for the quantity of the item
                quantity = int(input("Enter the quantity: "))

                # add the item, quantity, and cost to the bill
                bill_items.append([item, quantity, cost])

                #adding item and qty. to KOT bill
                kot_bill.append([item,quantity])

                # add the cost of the item to the total cost
                total_cost += cost * quantity

                # ask the user if they want to add more items
                next_item = input("More Items? [y/n] ")

            # print the bill
            print(40*'*')
            print("\n" + hotel_name)
            print(address)
            print("Phone: " + phone)
            print(date.today())
            print("Bill No.: " + str(rd.randint(1000, 9999)))
            print(tabulate(bill_items, headers=["Item", "Quantity", "Cost"], tablefmt='rounded_outline'))
            print("Total Cost: ₹" + str(total_cost))
            count+=1
            client+=1
            grx.append(total_cost)
            amt+=total_cost
            print(60*'*')
            # ask the user if they want to process another bill

            #Kitchen purpose bill KOT
            print(60*'*')
            print("\n" + hotel_name)
            print(address)
            print(date.today())
            print(tabulate(kot_bill, headers=["Item", "Quantity"],tablefmt='rounded_outline'))
            # ask the user if they want to process another bill
            loop_bill = input("\nNext Order? [yes/no] ")
            print()

        print("\n\n")
        print("The number of orders taken today is",count)
        print("The total revenue today is ₹",amt)
        print("The average revenue per order is",amt/count)

        plt.bar(gry, grx)

        # Add a title and label the axes
        plt.title('Revenue today')
        plt.ylabel('Collected amount')
        plt.xlabel('Order number')

        # Show the plot
        plt.show()

        rev=open("revenue.dat","ab")
        #Findind the day of the week
        # Get the current date and time
        now = datetime.datetime.now()

        # Use strftime() to format the date and time as a string
        # with the weekday name (e.g. "Monday", "Tuesday", etc.)
        weekday= now.strftime("%A")
        date_=date.today()

        # sample data to save

        # open the existing binary file in write mode
        file = open("revenue.dat", "ab")
        # create a dictionary to store the data
        info= [weekday,date_,amt,count]
        # use the pickle module to dump the data to the binary file
        pickle.dump(info, file)


    else:
        print("Wrong Username or Password\nPlease Retry!")
        pass_word='error_password'


