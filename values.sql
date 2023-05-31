delete from menu;
insert into menu(name, description, price)  values
('Tomato Soup', 'Tomato Soup', 50),
('Veg clear soup', 'Veggie Soup', 55),
('Vegetable Hot N Sour Soup', 'Veg sour soup',55),
('Vegetable Manchow Soup', 'manchow soup', 60),
('Paneer Tikka','Tikka',  70),
('Paneer Manchurian', 'manchurin', 70),
('Veg Nuggets', 'Nuggets', 75),
('Mushroom Salt and Pepper','mushroom', 70),
('Veg Salad', 'Simple Salad', 100),
('Veg Pasta Salad', 'pasta salad', 110);

delete from customer;
insert into customer(name, phone, address)  values
('Subbu', '9986026076', 'parijatha residency, mangalore'),
('Chaitanya', '9986099860', 'parijatha residency, mangalore');

delete from inventory;
insert into inventory(menu_id, qty)  values
(1, 500),
(2, 300),
(3, 400),
(4, 250),
(5, 550),
(6, 760),
(7, 900),
(8, 1000),
(10, 2000);
