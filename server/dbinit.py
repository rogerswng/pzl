# -*- coding: utf-8 -*-

from dbaseop import Pysql

if __name__ == "__main__":
    db = Pysql()

    db.query(sql="""
        create table if not exists `user` (
            `id` int(11) not null auto_increment,
            `username` varchar(50) not null,
            `password` varchar(50) not null,
            `role` int(4) not null,
            primary key (`id`),
            unique key `user_name_unique`(`username`) using btree
        );
    """)

    db.query(sql="""
        create table if not exists `category` (
            `id` int(11) not null auto_increment,
            `parent_id` int(11) default null,
            `name` varchar(50) default null,
            `status` tinyint(1) default '1',
            `created_time` datetime default null,
            `created_user` int(11) default null,
            `updated_time` datetime default null,
            `updated_user` int(11) default null,
            primary key (`id`)
        ) engine=InnoDB default charset=utf8;
    """)

    db.query(sql="""
        create table if not exists `product` (
            `id` int(11) not null auto_increment,
            `category_id` int(11) not null,
            `name` varchar(100) not null,
            `main_image` varchar(500) default null,
            `detail` text default null,
            `price` decimal(20,2) not null,
            `stock` int(11) not null,
            `status` int(6) default '1',
            `created_time` datetime default null,
            `created_user` int(11) default null,
            `updated_time` datetime default null,
            `updated_user` int(11) default null,
            primary key (`id`)
        ) engine=InnoDB default charset=utf8;
    """)

    db.query(sql="""
        create table if not exists `order` (
            `id` int(11) not null auto_increment,
            `order_no` bigint(20) default null,
            `user_id` int(11) default null,
            `shipping_id` int(11) default null,
            `payment` decimal(20,2) default null,
            `postage` int(10) default null,
            `status` int(10) default null,
            `payment_time` datetime default null,
            `send_time` datetime default null,
            `close_time` datetime default null,
            `created_time` datetime default null,
            `updated_time` datetime default null,
            primary key (`id`),
            unique key `order_no_index`(`order_no`) using btree
        ) engine=InnoDB default charset=utf8;
    """)

    db.insert(sql="""
        insert into user (username,password,role) values
        (%s,%s,%s);
    """,params=("pangzilong","pangzilong",0))

    db.insert(sql="""
        insert into `order` (order_no,user_id,payment,status,created_time,updated_time) values
        (%s,%s,%s,%s,now(),now());
    """,params=(123456,2,19.8,10))

    db.insert(sql="""
        insert into `order` (order_no,user_id,payment,status,created_time,updated_time) values
        (%s,%s,%s,%s,now(),now());
    """,params=(234567,2,20.4,10))

    db.insert(sql="""
        insert into `order` (order_no,user_id,payment,status,created_time,updated_time) values
        (%s,%s,%s,%s,now(),now());
    """,params=(345678,2,1.8,10))
