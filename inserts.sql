-- inserts para o pgadmin

-- Inserts para tabela Usuario
INSERT INTO Usuario ("Tipo", "Nome", "Sobrenome", "Email", "Senha", "Descricao") VALUES 
('Aluno', 'Augusto', 'Sousa', 'Augusto@gmail.com', '1234', NULL),
('Professor', 'Felipe', 'Monteiro', 'Felip01@gmail.com', '1234', NULL),
('Coordenador', 'Jonatanh', 'Costa', 'JonyMal@gmail.com', '1234', NULL),
('Aluno', 'Kleber', 'Marques', 'Klebin@gmail.com', '1234', NULL),
('Professor', 'Maria', 'Fernandes', 'maria.fernandes@gmail.com', 'abcd', NULL),
('Aluno', 'João', 'Pereira', 'joao.pereira@gmail.com', 'abcd', NULL),
('Coordenador', 'Paula', 'Mendes', 'paula.mendes@gmail.com', 'abcd', NULL),
('Aluno', 'Ricardo', 'Oliveira', 'ricardo.oliveira@gmail.com', 'abcd', NULL),
('Aluno', 'Mariana', 'Silva', 'mariana.silva@gmail.com', 'senha123', NULL),
('Professor', 'Carlos', 'Almeida', 'carlos.almeida@gmail.com', 'senha123', NULL),
('Aluno', 'Ana', 'Pereira', 'ana.pereira@gmail.com', 'senha123', NULL),
('Coordenador', 'Ricardo', 'Santos', 'ricardo.santos@gmail.com', 'senha123', NULL),
('Aluno', 'Lucas', 'Fernandes', 'lucas.fernandes@gmail.com', 'senha123', NULL),
('Professor', 'Fernanda', 'Costa', 'fernanda.costa@gmail.com', 'senha123', NULL),
('Aluno', 'Bruna', 'Rodrigues', 'bruna.rodrigues@gmail.com', 'senha123', NULL),
('Coordenador', 'Marcos', 'Oliveira', 'marcos.oliveira@gmail.com', 'senha123', NULL),
('Aluno', 'Pedro', 'Moura', 'pedro.moura@gmail.com', 'senha123', NULL),
('Aluno', 'Joana', 'Lima', 'joana.lima@gmail.com', 'senha123', NULL),
('Professor', 'Roberto', 'Dias', 'roberto.dias@gmail.com', 'senha123', NULL);

-- Inserts para tabela Curso
INSERT INTO Curso ("Nome_curso", "Descricao_curso", "Data_inicio", "Data_final", "ID_Usuario") VALUES
('Desenvolvimento de sistemas', 'Descrição', '2025-02-01', '2026-04-05', 96),
('Administrador de Banco de dados', 'Descrição', '2025-02-20', '2026-04-29', 96),
('Administrador de Redes', 'Descrição', '2025-02-25', '2026-05-10', 96),
('IT Essentials', 'Descrição', '2025-03-10', '2026-07-20', 96),
('Programação Web', 'Curso focado em desenvolvimento web', '2025-05-15', '2026-08-10', 96),
('Segurança da Informação', 'Curso de cibersegurança', '2024-09-01', '2025-12-20', 96),
('Design Gráfico', 'Curso de criação e edição de imagens', '2025-06-01', '2026-09-15', 96),
('Engenharia de Software', 'Curso sobre desenvolvimento ágil', '2025-07-01', '2026-12-15', 96),
('Banco de Dados Avançado', 'Curso avançado em SQL e NoSQL', '2025-08-10', '2026-11-30', 96),
('Redes e Segurança', 'Curso avançado em redes e cibersegurança', '2025-09-05', '2026-10-20', 96);

-- Inserts para tabela Turma
INSERT INTO Turma ("Codigo_Turma", "Turno", "Ano", "ID_Curso") VALUES
('2025.10.111', 'Manha', 2025, 51),
('2025.02.001', 'Tarde', 2025, 52),
('2025.10.201', 'Noite', 2025, 53),
('2025.12.115', 'Manha', 2025, 54),
('2025.05.210', 'Tarde', 2025, 55),
('2024.09.001', 'Noite', 2024, 56),
('2025.06.300', 'Manha', 2025, 57),
('2025.07.101', 'Noite', 2025, 58),
('2025.08.502', 'Tarde', 2025, 59),
('2025.09.305', 'Manha', 2025, 60),
('2025.11.150', 'Noite', 2025, 51),
('2025.12.210', 'Tarde', 2025, 53);

-- Inserts para tabela Usuario_da_Turma
INSERT INTO Usuario_da_Turma ("ID_Usuario", "ID_Turma") VALUES
(96, 51),
(97, 52),
(98, 53),
(99, 54),
(100, 55),
(101, 55),
(102, 56),
(103, 57);

-- Inserts para tabela Projeto
INSERT INTO Projeto ("Nome_projeto", "data_de_criacao", "data_de_modificacao", "ID_Turma", "ID_Curso") VALUES
('Sistema de Ligações', '2020-03-19', '2022-01-04', 61, 51),
('PetShop', '2020-05-20', '2023-03-10', 61, 51),
('Hot Dog', '2020-01-01', '2024-01-10', 61, 51),
('Odonto', '2020-07-10', '2025-04-30', 62, 52),
('Hotelaria', '2021-09-14', '2025-01-01', 62, 52),
('Canal de Rede', '2024-01-10', '2025-03-23', 61, 53),
('Distribuidora', '2020-04-23', '2021-04-02', 61, 53),
('Telefone', '2022-08-09', '2022-06-13', 62, 54),
('E-commerce', '2025-05-20', '2025-06-15', 62, 55),
('Firewall Config', '2024-10-05', '2025-01-10', 61, 56),
('Logo Designer', '2025-06-10', '2025-07-05', 62, 57);

-- Inserts para tabela Eventos
INSERT INTO Eventos ("Nome_do_evento", "Hora_do_evento", "Data_do_evento", "Descricao", "Endereco", "ID_Usuario") VALUES
('AgriTec', '12:20:00', '2025-01-01', 'Descrição', 'Senac Doca', 97),
('Exposição de Artes', '13:52:10', '2025-01-10', 'Descrição', 'Senac Doca', 97),
('Semana de Tecnologia', '09:00:00', '2025-05-25', 'Evento com palestras e workshops', 'Senac Centro', 100),
('Noite da Segurança', '19:30:00', '2025-10-15', 'Palestras sobre segurança digital', 'Auditório Central', 102);

-- Inserts para tabela Forum
INSERT INTO Forum ("Nome", "Data_criacao", "ID_Usuario") VALUES
('Administrador BD', '2021-02-01', 97),
('Desenvolvimento de Sistemas', '2023-03-10', 97),
('Administrador de Redes', '2023-05-20', 97);