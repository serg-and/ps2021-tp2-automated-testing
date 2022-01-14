-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema PAPAdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema PAPAdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `PAPAdb` DEFAULT CHARACTER SET utf8 ;
USE `PAPAdb` ;

-- -----------------------------------------------------
-- Table `PAPAdb`.`kaas haash`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PAPAdb`.`User` (
  `id` INT NOT NULL,
  `wwhash` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `PAPAdb`.`kaas haash`
-- -----------------------------------------------------
START TRANSACTION;
USE `PAPAdb`;
INSERT INTO `PAPAdb`.`User` (`id`, `wwhash`) VALUES (1001, '$2b$12$CZAwBFHsab5SBpK7acyPh.3OKQZwUDsTtakwres2wkKmV/5sP/BWi');
INSERT INTO `PAPAdb`.`User` (`id`, `wwhash`) VALUES (1002, '$2b$12$KiqrxQMOiLUwUr8yhwo4huzA/x05yrtqEoq2Z0knzds35MmkcsXWW');
INSERT INTO `PAPAdb`.`User` (`id`, `wwhash`) VALUES (1003, '$2b$12$PYQGkCgwL0C1A6T5X3JNweOPSlNhUvSS5Q5.b/CEddppJG0KxuS/S');
INSERT INTO `PAPAdb`.`User` (`id`, `wwhash`) VALUES (1004, '$2b$12$jta51ywSEyu7h.kNqEcVcueSIpqocI45smKbebfbbTNs0Z3FsaKrK');

COMMIT;

