-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema RRdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema RRdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `RRdb` DEFAULT CHARACTER SET utf8 ;
USE `RRdb` ;

-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `User` (
  `id` INT NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `displayName` VARCHAR(45) NOT NULL,
  `avatar` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Session` (
  `session_id` VARCHAR(100) NULL,
  `login_ip` VARCHAR(15) NULL,
  `http_user_agent` VARCHAR(256) NULL,
  `User_id` INT NOT NULL,
  PRIMARY KEY (`User_id`),
  FOREIGN KEY (`User_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)

ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Product` (
  `id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `description` MEDIUMTEXT NULL,
  `User_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`User_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Review` (
  `Product_id` INT NOT NULL,
  `User_id` INT NOT NULL,
  `dateTime` DATETIME NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  FOREIGN KEY (`Product_id`)
    REFERENCES `Product` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`User_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  PRIMARY KEY (`dateTime`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Like`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Like` (
  `Review_Product_id` INT NOT NULL,
  `Review_User_id` INT NOT NULL,
  `Review_dateTime` DATETIME NOT NULL,
  `User_id` INT NOT NULL,
  FOREIGN KEY (`Review_Product_id`)
    REFERENCES `Review` (`Product_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`Review_User_id`)
    REFERENCES `Review` (`User_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`Review_dateTime`)
    REFERENCES `Review` (`dateTime`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`User_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Dislike`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Dislike` (
  `Review_Product_id` INT NOT NULL,
  `Review_User_id` INT NOT NULL,
  `Review_dateTime` DATETIME NOT NULL,
  `User_id` INT NOT NULL,
  FOREIGN KEY (`Review_Product_id`)
    REFERENCES `Review` (`Product_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`Review_User_id`)
    REFERENCES `Review` (`User_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`Review_dateTime`)
    REFERENCES `Review` (`dateTime`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  FOREIGN KEY (`User_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Flags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Flags` (
  `challenge` VARCHAR(100) NOT NULL,
  `state` BIT,
  PRIMARY KEY (`challenge`))

ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `User`
-- -----------------------------------------------------
START TRANSACTION;
USE `RRdb`;
INSERT INTO `User` (`id`, `email`, `displayName`, `avatar`) VALUES (1001, 'bruh@idk.com', 'BruhMan', NULL);
INSERT INTO `User` (`id`, `email`, `displayName`, `avatar`) VALUES (1002, 'nah@idk.com', 'Nah IDK', NULL);
INSERT INTO `User` (`id`, `email`, `displayName`, `avatar`) VALUES (1003, 'zaza@yaahoo.com', 'ZAAAZAAA', NULL);
INSERT INTO `User` (`id`, `email`, `displayName`, `avatar`) VALUES (1004, 'me@hva.nl', 'Serge Andriessen', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `Session`
-- -----------------------------------------------------
START TRANSACTION;
USE `RRdb`;
INSERT INTO `Session` (`User_id`, `session_id`) VALUES (1001, NULL);
INSERT INTO `Session` (`User_id`, `session_id`) VALUES (1002, NULL);
INSERT INTO `Session` (`User_id`, `session_id`) VALUES (1003, NULL);
INSERT INTO `Session` (`User_id`, `session_id`) VALUES (1004, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `Product`
-- -----------------------------------------------------
START TRANSACTION;
USE `RRdb`;
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1001, 'Cookie Dough', 4.75, 'Delicious cookie dough, made by a real leprechaun in the hart of Ireland.', 1001);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1002, '19 dollar Fortnite card', 20.00, NULL, 1001);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1003, '100% pure ZAAZAA', 9999.99, NULL, 1003);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1004, 'HvA login credentials 1 piece', 2.69, NULL, 1002);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1005, '10x HvA login credentials', 75.49, NULL, 1002);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1006, '50x HvA login credentials', 75.49, NULL, 1002);
INSERT INTO `Product` (`id`, `name`, `price`, `description`, `User_id`) VALUES (1007, '300x HvA login credentials', 699.99, NULL, 1002);

COMMIT;


-- -----------------------------------------------------
-- Data for table `Review`
-- -----------------------------------------------------
START TRANSACTION;
USE `RRdb`;
INSERT INTO `Review` (`Product_id`, `User_id`, `dateTime`, `text`) VALUES (1001, 1001, '2021-01-11 13:23:43', 'such wow');
INSERT INTO `Review` (`Product_id`, `User_id`, `dateTime`, `text`) VALUES (1001, 1003, '2021-01-12 17:46:11', 'yes');

COMMIT;


-- -----------------------------------------------------
-- Data for table `Flags`
-- -----------------------------------------------------
START TRANSACTION;
USE `RRdb`;
INSERT INTO `Flags` (`challenge`, `state`) VALUES ('Challenge 1', 0);
INSERT INTO `Flags` (`challenge`, `state`) VALUES ('Challenge 2', 0);
INSERT INTO `Flags` (`challenge`, `state`) VALUES ('Challenge 3', 0);

COMMIT;
