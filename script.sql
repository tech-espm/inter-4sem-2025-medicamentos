-- MySQL Script updated by ChatGPT
-- AUTO_INCREMENT added to all ID fields

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema SintoMed
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `SintoMed`;
CREATE SCHEMA IF NOT EXISTS `SintoMed` DEFAULT CHARACTER SET utf8;
USE `SintoMed`;

-- -----------------------------------------------------
-- Table `marca`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `marca`;

CREATE TABLE `marca` (
  `idmarca` INT NOT NULL AUTO_INCREMENT,
  `nomeMarca` VARCHAR(45) NOT NULL default "sem marca",
  PRIMARY KEY (`idmarca`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `medicamentos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `medicamentos`;

CREATE TABLE `medicamentos` (
  `idMedicamentos` INT NOT NULL AUTO_INCREMENT,
  `nomeMedicamento` VARCHAR(200) NOT NULL,
  `dosagem` VARCHAR(45) NOT NULL,
  `preco` VARCHAR(45) NOT NULL DEFAULT '',
  `avaliacao` VARCHAR(45) NOT NULL default "Sem avaliação",
  `marca` INT NOT NULL ,
  PRIMARY KEY (`idMedicamentos`),
  INDEX `fk_medicamentos_marca_idx` (`marca`),
  CONSTRAINT `fk_medicamentos_marca`
    FOREIGN KEY (`marca`) REFERENCES `marca` (`idmarca`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `sintoma`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sintoma`;

CREATE TABLE `sintoma` (
  `idsintoma` INT NOT NULL AUTO_INCREMENT,
  `nomeSintoma` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idsintoma`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `doenca`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `doenca`;

CREATE TABLE `doenca` (
  `iddoenca` INT NOT NULL AUTO_INCREMENT,
  `nomeDoenca` VARCHAR(45) NOT NULL,
  `gravidadeDoenca` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iddoenca`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `sintoma_has_medicamentos`
-- (table N-N, no auto_increment)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sintoma_has_medicamentos`;

CREATE TABLE `sintoma_has_medicamentos` (
  `sintoma_idsintoma` INT NOT NULL,
  `medicamentos_idMedicamentos` INT NOT NULL,
  PRIMARY KEY (`sintoma_idsintoma`, `medicamentos_idMedicamentos`),
  INDEX `fk_sintoma_has_medicamentos_medicamentos1_idx` (`medicamentos_idMedicamentos`),
  INDEX `fk_sintoma_has_medicamentos_sintoma1_idx` (`sintoma_idsintoma`),
  CONSTRAINT `fk_sintoma_has_medicamentos_sintoma1`
    FOREIGN KEY (`sintoma_idsintoma`) REFERENCES `sintoma` (`idsintoma`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sintoma_has_medicamentos_medicamentos1`
    FOREIGN KEY (`medicamentos_idMedicamentos`) REFERENCES `medicamentos` (`idMedicamentos`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `doenca_has_sintoma`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `doenca_has_sintoma`;

CREATE TABLE `doenca_has_sintoma` (
  `doenca_iddoenca` INT NOT NULL,
  `sintoma_idsintoma` INT NOT NULL,
  PRIMARY KEY (`doenca_iddoenca`, `sintoma_idsintoma`),
  INDEX `fk_doenca_has_sintoma_sintoma1_idx` (`sintoma_idsintoma`),
  INDEX `fk_doenca_has_sintoma_doenca1_idx` (`doenca_iddoenca`),
  CONSTRAINT `fk_doenca_has_sintoma_doenca1`
    FOREIGN KEY (`doenca_iddoenca`) REFERENCES `doenca` (`iddoenca`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_doenca_has_sintoma_sintoma1`
    FOREIGN KEY (`sintoma_idsintoma`) REFERENCES `sintoma` (`idsintoma`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `usuario`
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
-- Table `ficha`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ficha`;

CREATE TABLE `ficha` (
  `idficha` INT NOT NULL AUTO_INCREMENT,
  `peso` VARCHAR(45) NOT NULL,
  `altura` VARCHAR(45) NOT NULL,
  `usuario` INT NOT NULL,
  PRIMARY KEY (`idficha`),
  INDEX `fk_ficha_usuario1_idx` (`usuario`),
  CONSTRAINT `fk_ficha_usuario1`
    FOREIGN KEY (`usuario`) REFERENCES `usuario` (`idusuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `prescricao`
-- (tabela N-N, não tem auto_increment)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prescricao`;

CREATE TABLE `prescricao` (
  `medicamentos` INT NOT NULL,
  `ficha` INT NOT NULL,
  PRIMARY KEY (`medicamentos`, `ficha`),
  INDEX `fk_medicamentos_has_ficha_ficha1_idx` (`ficha`),
  INDEX `fk_medicamentos_has_ficha_medicamentos1_idx` (`medicamentos`),
  CONSTRAINT `fk_medicamentos_has_ficha_medicamentos1`
    FOREIGN KEY (`medicamentos`) REFERENCES `medicamentos` (`idMedicamentos`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_medicamentos_has_ficha_ficha1`
    FOREIGN KEY (`ficha`) REFERENCES `ficha` (`idficha`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
