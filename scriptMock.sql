USE SintoMed;

drop table medicamentos_mock;

-- cria uma cópia da estrutura
CREATE TABLE IF NOT EXISTS medicamentos_mock LIKE medicamentos;

-- limpa se já tiver lixo de testes
TRUNCATE TABLE medicamentos_mock;

-- copia os 304 reais pra tabela de mock
INSERT INTO medicamentos_mock
SELECT * FROM medicamentos;

ALTER TABLE medicamentos_mock
ADD COLUMN dataPreco DATE NULL;

ALTER TABLE medicamentos_mock
ADD COLUMN avaliacao DECIMAL(2,1) NULL;

ALTER TABLE medicamentos_mock
ADD COLUMN idMedicamento_base INT NULL;

select * from medicamentos_mock;

-- todo mundo na primeira raspagem
UPDATE medicamentos_mock
SET dataPreco = '2025-10-06';

-- o id da primeira raspagem vira o id fixo do produto
UPDATE medicamentos_mock
SET idMedicamento_base = idMedicamentos
WHERE dataPreco = '2025-10-06';

-- primeira raspagem
SET SQL_SAFE_UPDATES = 0;

UPDATE medicamentos_mock
SET avaliacao = ROUND(3 + RAND() * 2, 1)  -- notas entre 3.0 e 5.0
WHERE dataPreco = '2025-10-06';

SET SQL_SAFE_UPDATES = 1;

-- segunda raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 7 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- terceira raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 14 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- quarta raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 21 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- quinta raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 28 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- sexta raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 35 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- sétima raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 42 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- oitava raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 49 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- nona raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 56 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- décima raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 63 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

-- 11 raspagem
INSERT INTO medicamentos_mock (
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    preco,
    substancia,
    marca,
    quantidade,
    dataPreco,
    avaliacao
)
SELECT
    idMedicamento_base,
    nomeMedicamento,
    dosagem,
    link,
    ROUND(preco * (1 + (RAND() * 0.6 - 0.3)), 2) AS preco,     -- preço ±30%
    substancia,
    marca,
    quantidade,
    DATE_ADD('2025-10-06', INTERVAL 70 DAY) AS dataPreco,      -- nova semana
    LEAST(
        5.0,
        GREATEST(
            1.0,
            ROUND(avaliacao + (RAND() * 0.8 - 0.4), 1)        -- avaliação variando
        )
    )
FROM medicamentos_mock
WHERE dataPreco = '2025-10-06';

select * from medicamentos_mock;

delete from medicamentos_mock
where dataPreco > '2025-12-03';