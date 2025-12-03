SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP SCHEMA IF EXISTS `SintoMed`;
CREATE SCHEMA IF NOT EXISTS `SintoMed` DEFAULT CHARACTER SET utf8 ;
USE `SintoMed`;

-- -----------------------------------------------------
-- Table laboratorio
-- -----------------------------------------------------
DROP TABLE IF EXISTS `laboratorio`;

CREATE TABLE `laboratorio` (
  `idlaboratorio` INT NOT NULL AUTO_INCREMENT,
  `nomeLaboratorio` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idlaboratorio`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table marca
-- -----------------------------------------------------
DROP TABLE IF EXISTS `marca`;

CREATE TABLE `marca` (
  `idmarca` INT NOT NULL AUTO_INCREMENT,
  `nomeMarca` VARCHAR(45) NOT NULL,
  `laboratorio` INT NOT NULL,
  PRIMARY KEY (`idmarca`),
  INDEX `fk_marca_laboratorio1_idx` (`laboratorio` ASC),
  CONSTRAINT `fk_marca_laboratorio1`
    FOREIGN KEY (`laboratorio`)
    REFERENCES `laboratorio` (`idlaboratorio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table medicamentos
-- -----------------------------------------------------
DROP TABLE IF EXISTS `medicamentos`;

CREATE TABLE `medicamentos` (
  `idMedicamentos` INT NOT NULL AUTO_INCREMENT,
  `nomeMedicamento` VARCHAR(200) NOT NULL,
  `dosagem` VARCHAR(45) NOT NULL,
  `link` VARCHAR(200) NOT NULL,
  `preco` FLOAT(4) NOT NULL DEFAULT '0',
  `substancia` VARCHAR(200) NOT NULL,
  `marca` INT NOT NULL,
  `quantidade` VARCHAR(45) NOT NULL default '1',
  PRIMARY KEY (`idMedicamentos`),
  INDEX `fk_medicamentos_marca_idx` (`marca` ASC),
  CONSTRAINT `fk_medicamentos_marca`
    FOREIGN KEY (`marca`)
    REFERENCES `marca` (`idmarca`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table sintoma
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sintoma`;

CREATE TABLE `sintoma` (
  `idsintoma` INT NOT NULL AUTO_INCREMENT,
  `nomeSintoma` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idsintoma`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table doenca
-- -----------------------------------------------------
DROP TABLE IF EXISTS `doenca`;

CREATE TABLE `doenca` (
  `iddoenca` INT NOT NULL AUTO_INCREMENT,
  `nomeDoenca` VARCHAR(45) NOT NULL,
  `gravidadeDoenca` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iddoenca`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table sintoma_has_medicamentos
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sintoma_has_medicamentos`;

CREATE TABLE `sintoma_has_medicamentos` (
  `sintoma` INT NOT NULL,
  `medicamentos` INT NOT NULL,
  PRIMARY KEY (`sintoma`, `medicamentos`),
  INDEX `fk_sintoma_has_medicamentos_medicamentos1_idx` (`medicamentos` ASC),
  INDEX `fk_sintoma_has_medicamentos_sintoma1_idx` (`sintoma` ASC),
  CONSTRAINT `fk_sintoma_has_medicamentos_sintoma1`
    FOREIGN KEY (`sintoma`)
    REFERENCES `sintoma` (`idsintoma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sintoma_has_medicamentos_medicamentos1`
    FOREIGN KEY (`medicamentos`)
    REFERENCES `medicamentos` (`idMedicamentos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table doenca_has_sintoma
-- -----------------------------------------------------
DROP TABLE IF EXISTS `doenca_has_sintoma`;

CREATE TABLE `doenca_has_sintoma` (
  `doenca` INT NOT NULL,
  `sintoma` INT NOT NULL,
  PRIMARY KEY (`doenca`, `sintoma`),
  INDEX `fk_doenca_has_sintoma_sintoma1_idx` (`sintoma` ASC),
  INDEX `fk_doenca_has_sintoma_doenca1_idx` (`doenca` ASC),
  CONSTRAINT `fk_doenca_has_sintoma_doenca1`
    FOREIGN KEY (`doenca`)
    REFERENCES `doenca` (`iddoenca`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_doenca_has_sintoma_sintoma1`
    FOREIGN KEY (`sintoma`)
    REFERENCES `sintoma` (`idsintoma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table usuario
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `idusuario` INT NOT NULL AUTO_INCREMENT,
  `nomeUsuario` VARCHAR(70) NOT NULL,
  `dataNascimento` DATE NOT NULL,
  `cpf` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `genero` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idusuario`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table ficha
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ficha`;

CREATE TABLE `ficha` (
  `idficha` INT NOT NULL AUTO_INCREMENT,
  `peso` VARCHAR(45) NOT NULL,
  `altura` VARCHAR(45) NOT NULL,
  `usuario` INT NOT NULL,
  PRIMARY KEY (`idficha`),
  INDEX `fk_ficha_usuario1_idx` (`usuario` ASC),
  CONSTRAINT `fk_ficha_usuario1`
    FOREIGN KEY (`usuario`)
    REFERENCES `usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table prescricao
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prescricao`;

CREATE TABLE `prescricao` (
  `medicamentos` INT NOT NULL,
  `ficha` INT NOT NULL,
  PRIMARY KEY (`medicamentos`, `ficha`),
  INDEX `fk_medicamentos_has_ficha_ficha1_idx` (`ficha` ASC),
  INDEX `fk_medicamentos_has_ficha_medicamentos1_idx` (`medicamentos` ASC),
  CONSTRAINT `fk_medicamentos_has_ficha_medicamentos1`
    FOREIGN KEY (`medicamentos`)
    REFERENCES `medicamentos` (`idMedicamentos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_medicamentos_has_ficha_ficha1`
    FOREIGN KEY (`ficha`)
    REFERENCES `ficha` (`idficha`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
