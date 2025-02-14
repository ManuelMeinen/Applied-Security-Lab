CREATE DATABASE imovies;

USE imovies;

CREATE TABLE users (
  uid varchar(64) NOT NULL DEFAULT '',
  lastname varchar(64) NOT NULL DEFAULT '',
  firstname varchar(64) NOT NULL DEFAULT '',
  email varchar(64) NOT NULL DEFAULT '',
  pwd varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (uid)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO users VALUES ('ps','Schaller','Patrick','ps@imovies.ch','6e58f76f5be5ef06a56d4eeb2c4dc58be3dbe8c7'),('lb','Bruegger','Lukas','lb@imovies.ch','8d0547d4b27b689c3a3299635d859f7d50a2b805'),('ms','Schlaepfer','Michael','ms@imovies.ch','4d7de8512bd584c3137bb80f453e61306b148875'),('a3','Anderson','Andres Andrea','anderson@imovies.ch','6b97f534c330b5cc78d4cc23e01e48be3377105b');
INSERT INTO users VALUES('admin', 'Admin', 'Admin', 'admin@imovies.com', '86207ea6969c0b9035b9f87e029a5336cb9926d2');

CREATE TABLE admin (
  uid varchar(64) NOT NULL DEFAULT '',
  is_admin BOOLEAN NOT NULL DEFAULT 0,
  PRIMARY KEY (uid)
);

INSERT INTO admin VALUES ('ps', 0), ('lb', 0), ('ms', 0), ('a3', 0), ('admin', 1);

CREATE TABLE certificates (
  uid varchar(64) NOT NULL DEFAULT '',
  certificate varchar(2048) NOT NULL DEFAULT '',
  revoked BOOLEAN NOT NULL DEFAULT 0,
  PRIMARY KEY (certificate)
);

CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY 'JT:*g,m,p8{-"95';
GRANT DELETE, INSERT, SELECT, UPDATE ON imovies.users TO 'ubuntu'@'localhost';
GRANT DELETE, INSERT, SELECT, UPDATE ON imovies.certificates TO 'ubuntu'@'localhost';
GRANT DELETE, INSERT, SELECT, UPDATE ON imovies.admin TO 'ubuntu'@'localhost';