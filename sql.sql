INSERT INTO role (name)
VALUES ('admin');

INSERT INTO user (email, firstname, lastname, password_hash, role_id, create_date)
VALUES ('kevin_foong@yahoo.com', 'Kevin', 'Foong', 'abc', 1, now());

u = User(email="kevin_foong@yahoo.com", firstname="Kevin", lastname="Foong", password_hash="abc", role_id=1, last_seen=now, create_date=now)

from app.admin_auth.models import User
from app import db
from datetime import datetime
now = datetime.now()
u = User.query.filter_by(email="kevin_foong@yahoo.com").first()
u.set_password('abc')
db.session.add(u)
db.session.commit()

INSERT INTO image_type(name)
values('blog'),('page');

insert into page_status (name, create_date)
values ('draft', now()),('published', now()),('archived', now());

insert into site_setting (posts_per_page, google_map_key, recaptcha_key, sendgrid_key, mail_from, mail_admins, user_id, update_date, create_date)
values (5, 'key', 'key', 'key', 'no-reply@flaskcms.com', 'kevin_foong@yahoo.com kfoong7@gmail.com', 1, now(), now());

==

Message

INSERT INTO message(name,email,message,user_read,create_date)
VALUES("John Smith", "john.smith@abc.com", "Hello how are you?", false, now());

INSERT INTO message(name,email,message,user_read,create_date)
VALUES("Amy Burr", "amy.burr@abc.com", "What a great website. Well done!", false, now());

INSERT INTO message(name,email,message,user_read,create_date)
VALUES("Troy Trojan", "troy@aabb.com", "Please help", false, now());

==

Page

insert into page (name, user_id, last_publish_date, create_date, display)
values ('home', 2, now(), now());

insert into page (name, user_id, last_publish_date, create_date, display)
values ('contact', 2, now(), now());

insert into page (name, user_id, last_publish_date, create_date, display)
values ('home_hero', 1, now(), now(), 'Home - Hero');

insert into page_status (name, create_date)
values ('draft', now());

insert into page_status (name, create_date)
values ('published', now());

insert into page_status (name, create_date)
values ('archived', now());

INSERT into page_contact (status_id, content, page_id, user_id, update_date, create_date)
VALUES (1, "Drop me a line! Either fill in the form below or send me an email. I will get back to you shortly.", 8, 2, now(), now());

INSERT into page_contact (status_id, content, page_id, user_id, update_date, create_date)
VALUES (2, "Drop me a line! Either fill in the form below or send me an <a href='abc'>email</a>. I will get back to you shortly. Thanks!", 8, 2, now(), now());


POST

INSERT into post (slug, active, create_date, post, title, update_date, user_id)
VALUES ('test-slug', 1, now(), 'This is a test post', 'Some title', now(), 2);

INSERT into post (slug, active, create_date, post, title, update_date, user_id)
VALUES ('another-slug', 1, now(), 'Another test post', 'Yep 123', now(), 2);


INSERT INTO image_type(name)
values('blog');
INSERT INTO image_type(name)
values('page');

INSERT INTO comment(comment, name,email,post_id,create_date)
values('Nice post by the way','Joe','joe@abc.com',1,now());
INSERT INTO comment(comment, name,email,post_id,create_date)
values('I have a question','Mary','mary@jjj.com',1,now());


INSERT INTO page_home_main(important,text,image_id1,status_id,page_id,user_id,update_date,create_date,heading)
values('bla bla this is important', 'hello 123', 12,2,7,2,now(),now(),'Some heading')

INSERT INTO page_home_hero(text,image_id1,image_id2,status_id,page_id,user_id,update_date,create_date,heading)
values('bla bla this is important', 12,12,2,9,2,now(),now(),'Some heading')

INSERT INTO page_home_splash(title1,image_id1,title2,title3,status_id,page_id,user_id,update_date,create_date)
values('bla bla', 36, 'zub', 'dub',2,10,2,now(),now())

insert into page (name, user_id, last_publish_date, create_date, display)
values ('home_splash', 1, now(), now(), 'Home - Splash');

insert into site_setting (create_date)
values (now());

INSERT INTO category(name,display,create_date)
VALUES('men-tops','Men - Tops',now());

INSERT INTO category(name,display,create_date)
VALUES('women-tops','Women - Tops',now());

INSERT INTO category(name,display,create_date)
VALUES('men-bottoms','Men - Bottoms',now());

INSERT INTO category(name,display,create_date)
VALUES('women-bottoms','Women - Bottoms',now());

INSERT INTO category_general(title,description,category_id,user_id,update_date,create_date)
VALUES('RDX shorts','Cool and sleek MMA shorts',3,2,now(),now());

INSERT INTO category_general(title,description,category_id,user_id,update_date,create_date)
VALUES('Adidas running shorts','Cheetah print looks even better when viewed in a blur. So wear these adidas two-in-one running shorts as you race across the finish line. They stay in place on the move thanks to a high-rise back and drawcord. Slip your phone into the pocket on the supportive inner tights. This product is made with Primeblue, a high-performance recycled material made in part with Parley Ocean Plastic.',3,2,now(),now());

INSERT INTO category_general(title,description,category_id,user_id,update_date,create_date)
VALUES('Under Armour Long sleeve','Prepare for battle with the Under Armour HeatGear Armour Compression Top. With HeatGear technology combining with Under Armours signature Moisture Transport System whisking away sweat to keep you feeling dry, cool and comfortable, this is the ultimate warm weather workout top. Reach your potential with Under Armour',1,2,now(),now());

INSERT INTO image_type(name)
VALUES('store');

INSERT INTO size(name,create_date,update_date,user_id)
VALUES
('S',now(),now(),2),
('M',now(),now(),2),
('L',now(),now(),2),
('XL',now(),now(),2);

INSERT INTO color(name,create_date,update_date,user_id)
VALUES
('Red',now(),now(),2),
('Blue',now(),now(),2),
('Green',now(),now(),2);