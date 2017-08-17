-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'users'
--
-- ---

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `name` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `username` VARCHAR(30) NULL DEFAULT NULL,
  `password` VARCHAR(100) NULL DEFAULT NULL,
  `register_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
);

-- ---
-- Table 'accounts'
--
-- ---

DROP TABLE IF EXISTS `accounts`;

CREATE TABLE `accounts` (
  `account_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `mrkt_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `account` VARCHAR(50) NULL DEFAULT NULL,
  `address` VARCHAR(75) NULL DEFAULT NULL,
  `contact` VARCHAR(50) NULL DEFAULT NULL,
  `phone` VARCHAR(15) NULL DEFAULT NULL,
  `comments` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`account_id`)
);

-- ---
-- Table 'articles'
--
-- ---

DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
  `artic_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `user_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `title` VARCHAR(255) NULL DEFAULT NULL,
  `author` VARCHAR(100) NULL DEFAULT NULL,
  `body` MEDIUMTEXT NULL DEFAULT NULL,
  `create_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`artic_id`)
);

-- ---
-- Table 'employees'
--
-- ---

DROP TABLE IF EXISTS `employees`;

CREATE TABLE `employees` (
  `emp_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `user_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `hour_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Primary key',
  `fname` VARCHAR(50) NULL DEFAULT NULL,
  `lname` VARCHAR(50) NULL DEFAULT NULL,
  `address` VARCHAR(100) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `state` VARCHAR(25) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `phonenumber` VARCHAR(10) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `dresssize` VARCHAR(10) NULL DEFAULT NULL,
  `comments` MEDIUMTEXT NULL DEFAULT NULL,
  `create_date` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
);

-- ---
-- Table 'events'
--
-- ---

DROP TABLE IF EXISTS `events`;

CREATE TABLE `events` (
  `event_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `account_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `prgm_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `program` VARCHAR(25) NULL DEFAULT NULL,
  `event_date` DATE NULL DEFAULT NULL,
  `s_time` TIME NULL DEFAULT NULL,
  `e_time` TIME NULL DEFAULT NULL,
  `account` VARCHAR(100) NULL DEFAULT NULL,
  `sampler1` VARCHAR(50) NULL DEFAULT NULL,
  `sampler2` VARCHAR(50) NULL DEFAULT NULL,
  `teamlead` VARCHAR(50) NULL DEFAULT NULL,
  `comments` MEDIUMTEXT NULL DEFAULT NULL,
  `create_date` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`event_id`)
);

-- ---
-- Table 'managers'
--
-- ---

DROP TABLE IF EXISTS `managers`;

CREATE TABLE `managers` (
  `man_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `user_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `fname` VARCHAR(50) NULL DEFAULT NULL,
  `lname` VARCHAR(50) NULL DEFAULT NULL,
  `address` VARCHAR(100) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `state` VARCHAR(25) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `phonenumber` VARCHAR(12) NULL DEFAULT NULL,
  `email` VARCHAR(10) NULL DEFAULT NULL,
  `create_date` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`man_id`)
);

-- ---
-- Table 'markets'
--
-- ---

DROP TABLE IF EXISTS `markets`;

CREATE TABLE `markets` (
  `mrkt_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `mrkttitle` VARCHAR(50) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `state` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`mrkt_id`)
);

-- ---
-- Table 'programs'
--
-- ---

DROP TABLE IF EXISTS `programs`;

CREATE TABLE `programs` (
  `prgm_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `name` VARCHAR(50) NULL DEFAULT NULL,
  `brand` VARCHAR(50) NULL DEFAULT NULL,
  `spend` DOUBLE(10) NULL DEFAULT NULL,
  PRIMARY KEY (`prgm_id`)
);

-- ---
-- Table 'payroll'
--
-- ---

DROP TABLE IF EXISTS `payroll`;

CREATE TABLE `payroll` (
  `pay_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `emp_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `payrolldate` VARCHAR(11) NULL DEFAULT NULL,
  `startdate` VARCHAR(10) NULL DEFAULT NULL,
  `enddate` VARCHAR(11) NULL DEFAULT NULL,
  `hours` DECIMAL(5) NULL DEFAULT NULL,
  `gross` DECIMAL(8) NULL DEFAULT NULL,
  `deductions` DECIMAL(8) NULL DEFAULT NULL,
  `additions` DECIMAL(8) NULL DEFAULT NULL,
  `netpay` DECIMAL(8) NULL DEFAULT NULL,
  PRIMARY KEY (`pay_id`)
);

-- ---
-- Table 'hourly'
--
-- ---

DROP TABLE IF EXISTS `hourly`;

CREATE TABLE `hourly` (
  `hour_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `rate` DECIMAL(8) NULL DEFAULT NULL,
  PRIMARY KEY (`hour_id`)
);

-- ---
-- Table 'timesheet'
--
-- ---

DROP TABLE IF EXISTS `timesheet`;

CREATE TABLE `timesheet` (
  `time_id` INTEGER(11) NULL AUTO_INCREMENT DEFAULT NULL COMMENT 'Primary key',
  `emp_id` INTEGER(11) NULL DEFAULT NULL COMMENT 'Foreign key',
  `hours` DECIMAL(5) NULL DEFAULT NULL,
  `entered` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`time_id`)
);

-- ---
-- Foreign Keys
-- ---

ALTER TABLE `accounts` ADD FOREIGN KEY (mrkt_id) REFERENCES `markets` (`mrkt_id`);
ALTER TABLE `articles` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `employees` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `employees` ADD FOREIGN KEY (hour_id) REFERENCES `hourly` (`hour_id`);
ALTER TABLE `events` ADD FOREIGN KEY (account_id) REFERENCES `accounts` (`account_id`);
ALTER TABLE `events` ADD FOREIGN KEY (prgm_id) REFERENCES `programs` (`prgm_id`);
ALTER TABLE `managers` ADD FOREIGN KEY (user_id) REFERENCES `users` (`user_id`);
ALTER TABLE `payroll` ADD FOREIGN KEY (emp_id) REFERENCES `employees` (`emp_id`);
ALTER TABLE `timesheet` ADD FOREIGN KEY (emp_id) REFERENCES `employees` (`emp_id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `users` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `accounts` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `articles` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `employees` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `events` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `managers` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `markets` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `programs` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `payroll` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `hourly` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `timesheet` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `users` (`user_id`,`name`,`email`,`username`,`password`,`register_date`) VALUES
-- ('','','','','','');
-- INSERT INTO `accounts` (`account_id`,`mrkt_id`,`account`,`address`,`contact`,`phone`,`comments`) VALUES
-- ('','','','','','','');
-- INSERT INTO `articles` (`artic_id`,`user_id`,`title`,`author`,`body`,`create_date`) VALUES
-- ('','','','','','');
-- INSERT INTO `employees` (`emp_id`,`user_id`,`hour_id`,`fname`,`lname`,`address`,`city`,`state`,`zipcode`,`phonenumber`,`email`,`dresssize`,`comments`,`create_date`) VALUES
-- ('','','','','','','','','','','','','','');
-- INSERT INTO `events` (`event_id`,`account_id`,`prgm_id`,`program`,`event_date`,`s_time`,`e_time`,`account`,`sampler1`,`sampler2`,`teamlead`,`comments`,`create_date`) VALUES
-- ('','','','','','','','','','','','','');
-- INSERT INTO `managers` (`man_id`,`user_id`,`fname`,`lname`,`address`,`city`,`state`,`zipcode`,`phonenumber`,`email`,`create_date`) VALUES
-- ('','','','','','','','','','','');
-- INSERT INTO `markets` (`mrkt_id`,`mrkttitle`,`city`,`state`) VALUES
-- ('','','','');
-- INSERT INTO `programs` (`prgm_id`,`name`,`brand`,`spend`) VALUES
-- ('','','','');
-- INSERT INTO `payroll` (`pay_id`,`emp_id`,`payrolldate`,`startdate`,`enddate`,`hours`,`gross`,`deductions`,`additions`,`netpay`) VALUES
-- ('','','','','','','','','','');
-- INSERT INTO `hourly` (`hour_id`,`rate`) VALUES
-- ('','');
-- INSERT INTO `timesheet` (`time_id`,`emp_id`,`hours`,`entered`) VALUES
-- ('','','','');
