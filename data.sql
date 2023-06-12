drop database if exists restaurant_mgmt;
create database restaurant_mgmt;
use restaurant_mgmt;

drop table if exists menu;
create table menu (
   id          int primary key auto_increment,
   name        varchar(32) not null,
   description varchar(100) not null,
   price       decimal(6,2) not null);

drop table if exists inventory;
create table inventory (
   menu_id    int primary key auto_increment,
   qty        int not null,
   constraint fK_menu_id foreign key (menu_id) references menu(id) on delete cascade);


drop table if exists customer;
create table customer (
   id         int primary key  auto_increment,
   name       varchar(32) not null,
   phone      varchar(20) not null,
   address    varchar(250));

drop table if exists reservation_order;
create table reservation_order (
   id              int primary key  auto_increment,
   customer_id     int not null,
   table_number    int not null,
   cost            decimal(6,2) not null default 0.0,
   datetime        timestamp not null default current_timestamp,
   constraint uk_cust_table  unique(customer_id, table_number),
   constraint fk_customer_id foreign key(customer_id) references customer(id) on delete cascade);

drop table if exists order_item;
create table order_item(
   order_id  int not null,
   menu_id   int not null,
   qty       int not null,
   primary key(order_id, menu_id));

drop table if exists bill;
create table bill(
   id              int primary key auto_increment,
   billing_time    datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   customer_id     int not null,
   items           JSON not null);


create user if not exists 'admin'@'*' identified by 'admin';
create user if not exists 'cashier'@'*' identified by 'cashier';

grant create, drop, insert, delete, select, update on restaurant_mgmt.inventory to 'admin'@'*';
grant select, update on restaurant_mgmt.inventory to 'cashier'@'*';
grant create, drop, insert, delete, select, update on restaurant_mgmt.bill to 'cashier'@'*';
grant all privileges on restaurant_mgmt.menu  to 'cashier'@'*';
grant all privileges on restaurant_mgmt.menu  to 'admin'@'*';
grant all privileges on restaurant_mgmt.order_item  to 'admin'@'*';
grant all privileges on restaurant_mgmt.order_item  to 'cashier'@'*';
grant all privileges on restaurant_mgmt.customer  to 'cashier'@'*';
grant all privileges on restaurant_mgmt.customer  to 'admin'@'*';
grant all privileges on restaurant_mgmt.customer  to 'admin'@'*';
grant all privileges on restaurant_mgmt.reservation_order  to 'cashier'@'*';
