CREATE DATABASE `spider`;

CREATE TABLE `doubanread`(
    id INT NOT NULL AUTO_INCREMENT,
    maintitle VARCHAR(64) NOT NUll,
    subtitle VARCHAR(64) DEFAULT "",
    author VARCHAR(64) DEFAULT "",
    type VARCHAR(128) DEFAULT "",
    score CHAR(4) DEFAULT "",
    detail_url VARCHAR(128) DEFAULT "",
    `describe` VARCHAR(256) DEFAULT "",
    PRIMARY KEY (id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;