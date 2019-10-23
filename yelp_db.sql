-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema yelp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema yelp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `yelp` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `yelp` ;

-- -----------------------------------------------------
-- Table `yelp`.`business`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`business` (
  `business_id` CHAR(22) NOT NULL,
  `name` VARCHAR(100) NULL DEFAULT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `state` VARCHAR(10) NULL DEFAULT NULL,
  `postal_code` VARCHAR(10) NULL DEFAULT NULL,
  `latitude` FLOAT NULL DEFAULT NULL,
  `longitude` FLOAT NULL DEFAULT NULL,
  `stars` DECIMAL(2,1) NULL DEFAULT NULL,
  `review_count` INT(11) NULL DEFAULT NULL,
  `is_open` TINYINT(1) NULL DEFAULT NULL,
  `attributes` JSON NULL DEFAULT NULL,
  `categories` LONGTEXT NULL DEFAULT NULL,
  `hours` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`business_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `yelp`.`checkin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`checkin` (
  `business_id` CHAR(22) NOT NULL,
  `checkin_count` INT(11) NULL DEFAULT NULL,
  INDEX `checkin_fk_business_id` (`business_id` ASC),
  CONSTRAINT `checkin_fk_business_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `yelp`.`business` (`business_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `yelp`.`photo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`photo` (
  `caption` VARCHAR(255) NULL DEFAULT NULL,
  `photo_id` CHAR(22) NOT NULL,
  `business_id` CHAR(22) NULL DEFAULT NULL,
  `label` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`photo_id`),
  INDEX `photo_fk_business_id_idx` (`business_id` ASC),
  CONSTRAINT `photo_fk_business_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `yelp`.`business` (`business_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `yelp`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`user` (
  `user_id` CHAR(22) NOT NULL,
  `name` VARCHAR(100) NULL DEFAULT NULL,
  `review_count` INT(11) NULL DEFAULT NULL,
  `yelping_since` DATETIME NULL DEFAULT NULL,
  `useful` INT(11) NULL DEFAULT NULL,
  `funny` INT(11) NULL DEFAULT NULL,
  `cool` INT(11) NULL DEFAULT NULL,
  `elite` VARCHAR(255) NULL DEFAULT NULL,
  `fans` INT(11) NULL DEFAULT NULL,
  `average_stars` DECIMAL(3,2) NULL DEFAULT NULL,
  `compliment_hot` INT(11) NULL DEFAULT NULL,
  `compliment_more` INT(11) NULL DEFAULT NULL,
  `compliment_profile` INT(11) NULL DEFAULT NULL,
  `compliment_cute` INT(11) NULL DEFAULT NULL,
  `compliment_list` INT(11) NULL DEFAULT NULL,
  `compliment_note` INT(11) NULL DEFAULT NULL,
  `compliment_plain` INT(11) NULL DEFAULT NULL,
  `compliment_cool` INT(11) NULL DEFAULT NULL,
  `compliment_funny` INT(11) NULL DEFAULT NULL,
  `compliment_writer` INT(11) NULL DEFAULT NULL,
  `compliment_photos` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `yelp`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`review` (
  `review_id` CHAR(22) NOT NULL,
  `user_id` CHAR(22) NOT NULL,
  `business_id` CHAR(22) NOT NULL,
  `stars` INT(11) NULL DEFAULT NULL,
  `useful` INT(11) NULL DEFAULT NULL,
  `funny` INT(11) NULL DEFAULT NULL,
  `cool` INT(11) NULL DEFAULT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  INDEX `fk_review_b_id_idx` (`business_id` ASC),
  INDEX `fk_review_u_id_idx` (`user_id` ASC),
  CONSTRAINT `review_fk_business_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `yelp`.`business` (`business_id`),
  CONSTRAINT `review_fk_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `yelp`.`user` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `yelp`.`tip`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `yelp`.`tip` (
  `user_id` CHAR(22) NULL DEFAULT NULL,
  `business_id` CHAR(22) NULL DEFAULT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `compliment_count` INT(11) NULL DEFAULT NULL,
  INDEX `fk_tip_business_id_idx` (`business_id` ASC),
  INDEX `fk_tip_user_id_idx` (`user_id` ASC),
  CONSTRAINT `tip_fk_business_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `yelp`.`business` (`business_id`),
  CONSTRAINT `tip_fk_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `yelp`.`user` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;