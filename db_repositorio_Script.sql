-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_repositorio
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_repositorio` DEFAULT CHARACTER SET utf8 ;
USE `db_repositorio` ;

-- -----------------------------------------------------
-- Table Usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `imagem_usuario` VARCHAR(100),
  `Tipo` ENUM('Aluno', 'Professor', 'Coordenador') NOT NULL,
  `Nome` VARCHAR(20) NOT NULL,
  `Sobrenome` VARCHAR(20) NOT NULL,
  `Email` VARCHAR(100) NOT NULL,
  `Senha` VARCHAR(30) NOT NULL,
  `Descricao` VARCHAR(300),
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB;

INSERT INTO Usuario (Tipo, Nome, Sobrenome, Email, Senha) VALUES 
('Aluno', 'Augusto', 'Sousa', 'Augusto@gmail.com', '1234'),
('Professor', 'Felipe', 'Monteiro', 'Felip01@gmail.com', '1234'),
('Coordenador', 'Jonatanh', 'Costa', 'JonyMal@gmail.com', '1234'),
('Aluno', 'Kleber', 'Marques', 'Klebin@gmail.com', '1234'),
('Professor', 'Maria', 'Fernandes', 'maria.fernandes@gmail.com', 'abcd'),
('Aluno', 'João', 'Pereira', 'joao.pereira@gmail.com', 'abcd'),
('Coordenador', 'Paula', 'Mendes', 'paula.mendes@gmail.com', 'abcd'),
('Aluno', 'Ricardo', 'Oliveira', 'ricardo.oliveira@gmail.com', 'abcd'),
('Aluno', 'Mariana', 'Silva', 'mariana.silva@gmail.com', 'senha123'),
('Professor', 'Carlos', 'Almeida', 'carlos.almeida@gmail.com', 'senha123'),
('Aluno', 'Ana', 'Pereira', 'ana.pereira@gmail.com', 'senha123'),
('Coordenador', 'Ricardo', 'Santos', 'ricardo.santos@gmail.com', 'senha123'),
('Aluno', 'Lucas', 'Fernandes', 'lucas.fernandes@gmail.com', 'senha123'),
('Professor', 'Fernanda', 'Costa', 'fernanda.costa@gmail.com', 'senha123'),
('Aluno', 'Bruna', 'Rodrigues', 'bruna.rodrigues@gmail.com', 'senha123'),
('Coordenador', 'Marcos', 'Oliveira', 'marcos.oliveira@gmail.com', 'senha123'),
('Aluno', 'Pedro', 'Moura', 'pedro.moura@gmail.com', 'senha123'),
('Aluno', 'Joana', 'Lima', 'joana.lima@gmail.com', 'senha123'),
('Professor', 'Roberto', 'Dias', 'roberto.dias@gmail.com', 'senha123');

-- -----------------------------------------------------
-- Table Curso
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Curso` (
  `idCurso` INT NOT NULL AUTO_INCREMENT,
  `imagem_curso` VARCHAR(100),
  `Nome_curso` VARCHAR(45) NOT NULL,
  `Descricao_curso` VARCHAR(100),
  `Data_inicio` DATE,
  `Data_final` DATE NOT NULL,
  `ID_Usuario` INT NOT NULL,
  PRIMARY KEY (`idCurso`),
  INDEX (`ID_Usuario`),
  CONSTRAINT `fk_Curso_Usuario` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Curso (Nome_curso, Descricao_curso, Data_inicio, Data_final, ID_Usuario) VALUES 
('Desenvolvimento de sistemas', 'Descrição', '2025-02-01', '2026-04-05', 3),
('Administrador de Banco de dados', 'Descrição', '2025-02-20', '2026-04-29', 3),
('Administrador de Redes', 'Descrição', '2025-02-25', '2026-05-10', 3),
('IT Essentials', 'Descrição', '2025-03-10', '2026-07-20', 3),
('Programação Web', 'Curso focado em desenvolvimento web', '2025-05-15', '2026-08-10', 5),
('Segurança da Informação', 'Curso de cibersegurança', '2024-09-01', '2025-12-20', 7),
('Design Gráfico', 'Curso de criação e edição de imagens', '2025-06-01', '2026-09-15', 5),
('Engenharia de Software', 'Curso sobre desenvolvimento ágil', '2025-07-01', '2026-12-15', 10),
('Banco de Dados Avançado', 'Curso avançado em SQL e NoSQL', '2025-08-10', '2026-11-30', 2),
('Redes e Segurança', 'Curso avançado em redes e cibersegurança', '2025-09-05', '2026-10-20', 14);

-- -----------------------------------------------------
-- Table Turma
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turma` (
  `idTurma` INT NOT NULL AUTO_INCREMENT,
  `Codigo_Turma` VARCHAR(11) NOT NULL,
  `Turno` ENUM('Manha', 'Tarde', 'Noite'),
  `ID_Curso` INT NOT NULL,
  PRIMARY KEY (`idTurma`),
  INDEX (`ID_Curso`),
  CONSTRAINT `fk_Turma_Curso` FOREIGN KEY (`ID_Curso`) REFERENCES `Curso` (`idCurso`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Turma (Codigo_Turma, Turno, ID_Curso) VALUES
('2025.10.111', 'Manha', 1),
('2025.02.001', 'Tarde', 2),
('2025.10.201', 'Noite', 3),
('2025.12.115', 'Manha', 4),
('2025.05.210', 'Tarde', 5),
('2024.09.001', 'Noite', 6),
('2025.06.300', 'Manha', 7),
('2025.07.101', 'Noite', 8),
('2025.08.502', 'Tarde', 9),
('2025.09.305', 'Manha', 10),
('2025.11.150', 'Noite', 5),
('2025.12.210', 'Tarde', 3);

-- -----------------------------------------------------
-- Table Eventos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Eventos` (
  `idEventos` INT NOT NULL AUTO_INCREMENT,
  `Nome_do_evento` VARCHAR(30) NOT NULL,
  `Hora_do_evento` TIME NOT NULL,
  `Data_do_evento` DATE NOT NULL,
  `Descricao` VARCHAR(100) NOT NULL,
  `Endereco` VARCHAR(30) NOT NULL,
  `status` VARCHAR(50),
  `ID_Usuario` INT NOT NULL,
  PRIMARY KEY (`idEventos`),
  INDEX (`ID_Usuario`),
  CONSTRAINT `fk_Eventos_Usuario` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Eventos (Nome_do_evento, Hora_do_evento, Data_do_evento, Descricao, Endereco, ID_Usuario) VALUES 
('AgriTec', '12:20:00', '2025-01-01', 'Descrição', 'Senac Doca', 2),
('Exposição de Artes', '13:52:10', '2025-01-10', 'Descrição', 'Senac Doca', 2),
('Semana de Tecnologia', '09:00:00', '2025-05-25', 'Evento com palestras e workshops', 'Senac Centro', 5),
('Noite da Segurança', '19:30:00', '2025-10-15', 'Palestras sobre segurança digital', 'Auditório Central', 7),
('Feira de Design', '14:00:00', '2025-07-20', 'Exposição de trabalhos de design', 'Senac Doca', 5),
('Hackathon 2025', '08:00:00', '2025-08-12', 'Competição de programação 24h', 'Laboratório de TI', 10),
('Workshop de UX/UI', '10:00:00', '2025-09-10', 'Workshop sobre design de experiência do usuário', 'Sala 202', 14),
('Palestra de Cloud Computing', '15:30:00', '2025-06-20', 'Introdução à computação em nuvem', 'Auditório B', 2),
('Fórum de Segurança Cibernética', '18:00:00', '2025-11-05', 'Discussões sobre ameaças e defesas', 'Auditório Central', 7),
('Mostra de Projetos', '16:00:00', '2025-12-10', 'Apresentação dos projetos dos alunos', 'Hall Principal', 5);

-- -----------------------------------------------------
-- Table Projeto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projeto` (
  `idProjeto` INT NOT NULL AUTO_INCREMENT,
  `Nome_projeto` VARCHAR(30) NOT NULL,
  `Data_de_criacao` DATE NOT NULL,
  `Data_de_modificacao` DATE NOT NULL,
  `Caminho_do_arquivo` VARCHAR(50) NOT NULL,
  `ID_Turma` INT NOT NULL,
  `ID_Curso` INT NOT NULL,
  PRIMARY KEY (`idProjeto`),
  INDEX (`ID_Turma`, `ID_Curso`),
  CONSTRAINT `fk_Projeto_Turma` FOREIGN KEY (`ID_Turma`) REFERENCES `Turma` (`idTurma`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Projeto_Curso` FOREIGN KEY (`ID_Curso`) REFERENCES `Curso` (`idCurso`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Projeto (Nome_projeto, Data_de_criacao, Data_de_modificacao, Caminho_do_arquivo, ID_Turma, ID_Curso) VALUES 
('Sistema de Ligações', '2020-03-19', '2022-01-04', 'Caminho', 1, 1),
('PetShop', '2020-05-20', '2023-03-10', 'Caminho', 1, 1),
('Hot Dog', '2020-01-01', '2024-01-10', 'Caminho', 1, 1),
('Odonto', '2020-07-10', '2025-04-30', 'Caminho', 2, 2),
('Hotelaria', '2021-09-14', '2025-01-01', 'Caminho', 2, 2),
('Canal de Rede', '2024-01-10', '2025-03-23', 'Caminho', 3, 3),
('Distribuidora', '2020-04-23', '2021-04-02', 'Caminho', 3, 3),
('Telefone', '2022-08-09', '2022-06-13', 'Caminho', 4, 4),
('E-commerce', '2025-05-20', '2025-06-15', 'Caminho', 5, 5),
('Firewall Config', '2024-10-05', '2025-01-10', 'Caminho', 6, 6),
('Logo Designer', '2025-06-10', '2025-07-05', 'Caminho', 7, 7);

-- -----------------------------------------------------
-- Table Forum
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Forum` (
  `idForum` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(50) NOT NULL,
  `Data_criacao` DATE NOT NULL,
  `ID_Usuario` INT NOT NULL,
  PRIMARY KEY (`idForum`),
  INDEX (`ID_Usuario`),
  CONSTRAINT `fk_Forum_Usuario` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Forum (Nome, Data_criacao, ID_Usuario) VALUES
('Administrador de Banco de Dados', '2021-02-01', 2),
('Desenvolvimento de Sistemas', '2023-03-10', 2),
('Administrador de Redes', '2023-05-20', 2),
('Programação Web Avançada', '2025-05-20', 5),
('Segurança da Informação e Redes', '2025-10-16', 7),
('Design Criativo', '2025-07-21', 5);

-- -----------------------------------------------------
-- Table Mensagem
-- -----------------------------------------------------
CREATE TABLE `mensagem` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `ID_Forum` INT NOT NULL,
    `ID_Usuario` INT NOT NULL,
    `Conteudo` TEXT NOT NULL,
    `Data_criacao` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_mensagem_forum`
        FOREIGN KEY (`ID_Forum`) REFERENCES `forum`(`idForum`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_mensagem_usuario`
        FOREIGN KEY (`ID_Usuario`) REFERENCES `usuario`(`ID_Usuario`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table Usuario_da_Turma
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario_da_Turma` (
  `ID_Usuario` INT NOT NULL,
  `ID_Turma` INT NOT NULL,
  PRIMARY KEY (`ID_Usuario`, `ID_Turma`),
  INDEX (`ID_Usuario`),
  INDEX (`ID_Turma`),
  CONSTRAINT `fk_Usuario_da_Turma_Usuario` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_da_Turma_Turma` FOREIGN KEY (`ID_Turma`) REFERENCES `Turma` (`idTurma`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

INSERT INTO Usuario_da_Turma (ID_Usuario, ID_Turma) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 5),
(7, 6),
(8, 7);

-- -----------------------------------------------------
-- Consultas
-- -----------------------------------------------------

-- 1) Listar os cursos iniciados após 2024
SELECT Nome_curso, Data_inicio
FROM Curso
WHERE Data_inicio > '2024-12-31';

-- 2) Ver todos os projetos cadastrados em janeiro de 2024
SELECT Nome_projeto, Data_de_criacao
FROM Projeto
WHERE YEAR(Data_de_criacao) = 2024
  AND MONTH(Data_de_criacao) = 1;

-- 3) Listar os fóruns criados em 2024, em ordem alfabética
SELECT Nome, Data_criacao
FROM Forum
WHERE YEAR(Data_criacao) = 2021
ORDER BY Nome ASC;

-- 4) Mostrar cada projeto com: nome do projeto, turma que pertence, turno da turma, nome do curso
SELECT p.Nome_projeto,
       t.Codigo_Turma,
       t.Turno,
       c.Nome_curso
FROM Projeto p
JOIN Turma t ON p.ID_Turma = t.idTurma
JOIN Curso c ON p.ID_Curso = c.idCurso;

-- 5) Mostrar todos os eventos com: nome do evento, data e hora, endereço, nome do organizador
SELECT e.Nome_do_evento,
       e.Data_do_evento,
       e.Hora_do_evento,
       e.Endereco,
       CONCAT(u.Nome, ' ', u.Sobrenome_usuario) AS Nome_organizador
FROM Eventos e
JOIN Usuario u ON e.ID_Usuario = u.idUsuario;

-- 6) Mostrar cada projeto com: nome do projeto, turma que pertence, turno da turma
SELECT p.Nome_projeto,
       t.Codigo_Turma,
       t.Turno
FROM Projeto p
JOIN Turma t ON p.ID_Turma = t.idTurma;

-- 7) Mostrar nome, data e hora do evento, endereço, nome completo do usuário responsável
SELECT e.Nome_do_evento,
       e.Data_do_evento,
       e.Hora_do_evento,
       e.Endereco,
       CONCAT(u.Nome, ' ', u.Sobrenome) AS Nome_responsavel
FROM Eventos e
JOIN Usuario u ON e.ID_Usuario = u.idUsuario;

-- -----------------------------------------------------
-- Procedures
-- -----------------------------------------------------

 -- Criar um professor
DELIMITER //

create procedure CriarProfessor(
	in p_Tipo varchar(20),
    in p_Nome varchar(100),
    in p_Sobrenome varchar(20),
    in p_Email varchar(50),
    in p_Senha varchar(50)
)
begin
	INSERT INTO Usuario (Tipo, Nome, Sobrenome, Email, Senha) VALUES 
	(p_Tipo, p_Nome, p_Sobrenome, p_Email, p_Senha);
end //

DELIMITER ;

call CriarProfessor('Professor', 'Theodoro', 'Cesar', 'Cesar@gmail.com', '1234');

-- Atualizar Descricao de um usuário
DELIMITER //

create procedure AtualizarDescricao(
    in p_idUsuario int,
    in p_Descricao varchar(100)
)
begin
	update usuario
    set Descricao = p_Descricao
    where idUsuario = p_idUsuario;
end //

DELIMITER ;

call AtualizarDescricao(2, 'Teste de Descrição');

-- Selecionar todos os professores
DELIMITER //

create procedure SelecionarProfessores()
begin
	select * from usuario
    where Tipo = 'Professor';
end //

DELIMITER ;

call SelecionarProfessores();

-- Selecionar todos os alunos
DELIMITER //

create procedure SelecionarAlunos()
begin
	select * from usuario
    where Tipo = 'Aluno';
end //

DELIMITER ;

call SelecionarAlunos();

-- Selecionar todos os coordenadores
DELIMITER //

create procedure SelecionarCoordenadores()
begin
	select * from usuario
    where Tipo = 'Coordenador';
end //

DELIMITER ;

call SelecionarCoordenadores();

-- Deletar Usuário
DELIMITER //

create procedure DeletarUsuario(
	in p_idUsuario int
)
begin
	delete from usuario
    where idUsuario = p_idUsuario;
end //

DELIMITER ;

call DeletarUsuario(19);

-- Criar eventos
DELIMITER //

create procedure CriarEvento(
	p_Nome_do_evento varchar(30),
	p_Hora_do_evento time,
	p_Data_do_evento date,
	p_Descricao varchar(100), 
	p_Endereco varchar(30),
    p_ID_Usuario int
)
begin
	INSERT INTO Eventos (Nome_do_evento, Hora_do_evento, Data_do_evento, Descricao, Endereco, ID_Usuario) VALUES 
    (p_Nome_do_evento,
	p_Hora_do_evento,
	p_Data_do_evento,
	p_Descricao, 
	p_Endereco,
    p_ID_Usuario);
end //

DELIMITER ;

call CriarEvento('Lojin', '20:15:00', '2025-05-19', 'Um workshop sobre a Lojin', 'Shopping Boulevard', 20);

-- Criar Cursos
DELIMITER //

create procedure CriarCurso(
	p_Nome_curso varchar(45),
	p_Descricao_curso varchar(100),
	p_Data_inicio date,
	p_Data_final date,
	p_ID_Usuario int
)
begin
	INSERT INTO Curso(Nome_curso, Descricao_curso, Data_inicio, Data_final, ID_Usuario) VALUES 
    (p_Nome_curso,
	p_Descricao_curso,
	p_Data_inicio,
	p_Data_final,
	p_ID_Usuario);
end //

DELIMITER ;

call CriarCurso('Databases Diários', 'Descrição', '2025-09-10', '2026-04-10', 7);

-- selecionar projeto pela data
DELIMITER // 

create procedure SelecionarDataProjeto(
	in p_Data_de_criacao date
)
begin
	select * from projeto
    where Data_de_criacao = p_Data_de_criacao;
end //

DELIMITER ;

call SelecionarDataProjeto('2025-06-10');

-- selecionar os cursos pela sua data de iniciação
DELIMITER //

create procedure SelecionarDataInicioCurso(
	in p_Data_inicio date
)
begin
	select * from curso
    where Data_inicio = p_Data_inicio;
end //

DELIMITER ;

call SelecionarDataInicioCurso('2025-08-10');

-- selecionar os cursos pela sua data de término
DELIMITER //

create procedure SelecionarDataFinalCurso(
	in p_Data_final date
)
begin
	select * from curso
    where Data_final = p_Data_final;
end //

DELIMITER ;

call SelecionarDataFinalCurso('2026-04-05');

-- -----------------------------------------------------
-- Restaura variáveis
-- -----------------------------------------------------
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;