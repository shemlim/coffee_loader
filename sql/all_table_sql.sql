-- Barista Table
CREATE TABLE IF NOT EXISTS public.order_barista
(
    barista_id serial,
    barista_name character varying(100)  NOT NULL,
    barista_password character varying(50)  NOT NULL,
    barista_job character varying(50) NOT NULL,
    barista_hold_table integer,
    barista_status integer,
    barista_date_edit timestamp,
    barista_order_id integer,
    CONSTRAINT order_barista_pkey PRIMARY KEY (barista_id)
)

insert into order_barista(barista_name,barista_password,barista_job) values('Seth','seth123','Barista') 
insert into order_barista(barista_name,barista_password,barista_job) values('Chloe','chloe123','Waiter')


-- Transaction order table
CREATE TABLE IF NOT EXISTS public.order_transac
(
    order_id serial NOT NULL ,
    order_table character varying(150)  NOT NULL,
    order_details text  NOT NULL,
    order_priority integer,
    order_total integer,
    order_barista character varying(50) ,
    order_status integer,
    order_date timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pkey PRIMARY KEY (order_id)
)

-- Menu order table
CREATE TABLE IF NOT EXISTS public.order_menu
(
    menu_id serial NOT NULL ,
    menu_name character varying(150)  NOT NULL,
    menu_status integer,
    menu_date timestamp DEFAULT CURRENT_TIMESTAMP,
    order_description text ,
    order_menu_category character varying(50) ,
    CONSTRAINT order_menu_pkey PRIMARY KEY (menu_id)
)


-- Insert manual menu
insert into order_menu(menu_name,menu_status,order_menu_category) values('Latte',1,'Drink');
insert into order_menu(menu_name,menu_status,order_menu_category) values('Mocca',1,'Drink');
insert into order_menu(menu_name,menu_status,order_menu_category) values('Green Tea Latte',1,'Drink');
insert into order_menu(menu_name,menu_status,order_menu_category) values('Americano',1,'Drink');
insert into order_menu(menu_name,menu_status,order_menu_category) values('Cappucino',1,'Drink');
insert into order_menu(menu_name,menu_status,order_menu_category) values('Espresso',1),'Drink';