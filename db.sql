DROP TABLE IF EXISTS user_fav;

CREATE TABLE user_fav
(
  id INT AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL,
  dest CHAR(3),
  price DECIMAL(5, 2),
  airline CHAR(2),
  flight_number INT,
  departs DATETIME,
  returns DATETIME,
  PRIMARY KEY (id)
);
