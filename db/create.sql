-- Feel free to modify this file to match your development goal.
CREATE TABLE Users
(id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL, -- copied this 'generated by default structure from the skeleton code, unsure of exact functionality
email VARCHAR(256) NOT NULL UNIQUE,
password VARCHAR(256) NOT NULL,
firstname VARCHAR(256) NOT NULL,
lastname VARCHAR(256) NOT NULL
--balance FLOAT NOT NULL  CHECK (balance >= 0) -- can balance be null?
);

CREATE TABLE Seller(
id INT NOT NULL PRIMARY KEY REFERENCES Users(id)
);

CREATE TABLE Coupons
(code VARCHAR(32) NOT NULL PRIMARY KEY,
percent_off FLOAT NOT NULL
);

CREATE TABLE Products(
--id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
id INT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
name VARCHAR(256) NOT NULL, 
seller_id INT NOT NULL REFERENCES Seller(id),
description VARCHAR(512),
category VARCHAR(256),
inventory  INT NOT NULL,
available BOOLEAN NOT NULL, 
price FLOAT NOT NULL,
coupon_code VARCHAR(32) NOT NULL REFERENCES Coupons(code),
PRIMARY KEY (id, seller_id)
);

CREATE TABLE Purchases
(id INT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
product_id INT NOT NULL,
seller_ID_2 INT NOT NULL,
buyer_id INT NOT NULL REFERENCES Users(id),
time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
quantity INT NOT NULL,
fulfilled_status BOOLEAN NOT NULL,
PRIMARY KEY (id, product_id, seller_ID_2),
FOREIGN KEY(product_id, seller_ID_2) REFERENCES Products(id, seller_id)
);

CREATE TABLE Cart_Items
(user_id INT NOT NULL REFERENCES Users(id), --why is this a foeign key
product_id INT NOT NULL,
seller_id INT NOT NULL,
quantity INT NOT NULL,
coupon_code VARCHAR(32), --check why not the same as products coupon_code
PRIMARY KEY(user_id, product_id, seller_id),
FOREIGN KEY(product_id, seller_id) REFERENCES Products(id, seller_id),
CHECK (quantity > 0) -- we want to check if the Cart_Items(quantity) <= Products(inventory), but this check should occur at the time of the purchase
);