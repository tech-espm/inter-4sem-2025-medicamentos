-- =========================================
-- BANCO DE DADOS: SINTOMED
-- MODELO COM AUTO_INCREMENT CORRETO
-- =========================================

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE;
SET SQL_MODE='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------
-- SCHEMA
-- -----------------------------------------
DROP SCHEMA IF EXISTS sintomed;
CREATE SCHEMA sintomed;
USE sintomed;

-- -----------------------------------------
-- USUARIO
-- -----------------------------------------
CREATE TABLE usuario (
  idusuario INT AUTO_INCREMENT PRIMARY KEY,
  nomeUsuario VARCHAR(200) NOT NULL,
  genero VARCHAR(45) NOT NULL,
  dataNascimento DATE NOT NULL,
  email VARCHAR(150) NOT NULL,
  senha VARCHAR(45) NOT NULL
) ENGINE=InnoDB;

-- -----------------------------------------
-- FICHA
-- -----------------------------------------
CREATE TABLE ficha (
  idficha INT AUTO_INCREMENT PRIMARY KEY,
  peso VARCHAR(45) NOT NULL,
  altura VARCHAR(45) NOT NULL,
  data DATE NOT NULL,
  idusuario INT NOT NULL,
  INDEX fk_ficha_usuario_idx (idusuario),
  CONSTRAINT fk_ficha_usuario
    FOREIGN KEY (idusuario)
    REFERENCES usuario (idusuario)
) ENGINE=InnoDB;

-- -----------------------------------------
-- MODELO DE RECOMENDACAO
-- -----------------------------------------
CREATE TABLE modeloRecomendacao (
  idmodeloRecomendacao INT AUTO_INCREMENT PRIMARY KEY,
  nomeModelo VARCHAR(45),
  metricas VARCHAR(45) NOT NULL
) ENGINE=InnoDB;

-- -----------------------------------------
-- LABORATORIO
-- -----------------------------------------
CREATE TABLE laboratorio (
  idlaboratorio INT AUTO_INCREMENT PRIMARY KEY,
  nomeLaboratorio VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- -----------------------------------------
-- MARCA
-- -----------------------------------------
CREATE TABLE marca (
  idmarca INT AUTO_INCREMENT PRIMARY KEY,
  nomeMarca VARCHAR(150) NOT NULL,
  idlaboratorio INT NOT NULL,
  INDEX fk_marca_laboratorio_idx (idlaboratorio),
  CONSTRAINT fk_marca_laboratorio
    FOREIGN KEY (idlaboratorio)
    REFERENCES laboratorio (idlaboratorio)
) ENGINE=InnoDB;

-- -----------------------------------------
-- MEDICAMENTO
-- -----------------------------------------
CREATE TABLE medicamento (
  idmedicamento INT AUTO_INCREMENT PRIMARY KEY,
  nomeMedicamento VARCHAR(200) NOT NULL,
  preco FLOAT NOT NULL,
  link VARCHAR(200) NOT NULL,
  avaliacao VARCHAR(45),
  quantidade VARCHAR(45),
  dosagem VARCHAR(45),
  idmarca INT NOT NULL,
  INDEX fk_medicamento_marca_idx (idmarca),
  CONSTRAINT fk_medicamento_marca
    FOREIGN KEY (idmarca)
    REFERENCES marca (idmarca)
) ENGINE=InnoDB;

-- -----------------------------------------
-- SUBSTANCIA
-- -----------------------------------------
CREATE TABLE substancia (
  idsubstancia INT AUTO_INCREMENT PRIMARY KEY,
  nomeSubstancia VARCHAR(200) NOT NULL,
  sugrupo VARCHAR(200)
) ENGINE=InnoDB;

-- -----------------------------------------
-- SINTOMA
-- -----------------------------------------
CREATE TABLE sintoma (
  idsintoma INT AUTO_INCREMENT PRIMARY KEY,
  nomeSintoma VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- -----------------------------------------
-- SUBSTANCIA x MEDICAMENTO (N:N)
-- -----------------------------------------
CREATE TABLE substancia_has_medicamento (
  idsubstancia INT NOT NULL,
  idmedicamento INT NOT NULL,
  PRIMARY KEY (idsubstancia, idmedicamento),
  FOREIGN KEY (idsubstancia) REFERENCES substancia (idsubstancia),
  FOREIGN KEY (idmedicamento) REFERENCES medicamento (idmedicamento)
) ENGINE=InnoDB;

-- -----------------------------------------
-- SINTOMA x SUBSTANCIA (N:N)
-- -----------------------------------------
CREATE TABLE sintoma_has_substancia (
  idsintoma INT NOT NULL,
  idsubstancia INT NOT NULL,
  PRIMARY KEY (idsintoma, idsubstancia),
  FOREIGN KEY (idsintoma) REFERENCES sintoma (idsintoma),
  FOREIGN KEY (idsubstancia) REFERENCES substancia (idsubstancia)
) ENGINE=InnoDB;

-- -----------------------------------------
-- FICHA x SINTOMA (N:N)
-- -----------------------------------------
CREATE TABLE ficha_has_sintoma (
  idficha INT NOT NULL,
  idsintoma INT NOT NULL,
  PRIMARY KEY (idficha, idsintoma),
  FOREIGN KEY (idficha) REFERENCES ficha (idficha),
  FOREIGN KEY (idsintoma) REFERENCES sintoma (idsintoma)
) ENGINE=InnoDB;

-- -----------------------------------------
-- RECOMENDACAO
-- -----------------------------------------
CREATE TABLE recomendacao (
  idrecomendacao INT AUTO_INCREMENT PRIMARY KEY,
  idficha INT NOT NULL,
  idsintoma INT NOT NULL,
  idmedicamento INT NOT NULL,
  idmodeloRecomendacao INT NOT NULL,
  FOREIGN KEY (idficha) REFERENCES ficha (idficha),
  FOREIGN KEY (idsintoma) REFERENCES sintoma (idsintoma),
  FOREIGN KEY (idmedicamento) REFERENCES medicamento (idmedicamento),
  FOREIGN KEY (idmodeloRecomendacao) REFERENCES modeloRecomendacao (idmodeloRecomendacao)
) ENGINE=InnoDB;

-- -----------------------------------------
-- FINALIZACAO
-- -----------------------------------------
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
