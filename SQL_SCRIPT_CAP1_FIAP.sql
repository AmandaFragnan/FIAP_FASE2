
-- Cria��o da tabela SENSOR para armazenar informa��es sobre os sensores utilizados nas planta��es
CREATE TABLE [dbo].[SENSOR] (
    [SEN_ID] [bigint] IDENTITY(1,1) NOT NULL,  -- Identificador �nico para cada sensor, gerado automaticamente
    [SEN_TIPO] varchar(100) NOT NULL,           -- Tipo de sensor (ex: umidade, pH, nutrientes)
    [SEN_LOCALIZACAO] varchar(100) NOT NULL,    -- Localiza��o do sensor na planta��o (ex: �rea do campo)
PRIMARY KEY CLUSTERED 
(
    [SEN_ID] ASC  -- Definindo SEN_ID como chave prim�ria da tabela
) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
GO

-- Cria��o da tabela CULTURA para armazenar informa��es sobre as diferentes culturas plantadas
CREATE TABLE [dbo].[CULTURA] (
    [CUL_ID] [bigint] IDENTITY(1,1) NOT NULL,  -- Identificador �nico para cada cultura, gerado automaticamente
    [CUL_NOME] varchar(100) NOT NULL,          -- Nome da cultura (ex: milho, soja)
    [CUL_HUMIDADE_MIN] [float] NOT NULL,      -- Umidade m�nima ideal para a cultura
    [CUL_HUMIDADE_MAX] [float] NOT NULL,      -- Umidade m�xima ideal para a cultura
    [CUL_PH_MIN] [float] NOT NULL,            -- pH m�nimo ideal para a cultura
    [CUL_PH_MAX] [float] NOT NULL,            -- pH m�ximo ideal para a cultura
    [CUL_N_MIN] [float] NOT NULL,             -- N�vel m�nimo de nutrientes N necess�rios
    [CUL_N_MAX] [float] NOT NULL,             -- N�vel m�ximo de nutrientes N necess�rios
    [CUL_P_MIN] [float] NOT NULL,             -- N�vel m�nimo de nutrientes P necess�rios
    [CUL_P_MAX] [float] NOT NULL,             -- N�vel m�ximo de nutrientes P necess�rios
    [CUL_K_MIN] [float] NOT NULL,             -- N�vel m�nimo de nutrientes K necess�rios
    [CUL_K_MAX] [float] NOT NULL,             -- N�vel m�ximo de nutrientes K necess�rios
PRIMARY KEY CLUSTERED 
(
    [CUL_ID] ASC  -- Definindo CUL_ID como chave prim�ria da tabela
) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
GO

-- Cria��o da tabela LEITURA_SENSOR para armazenar as leituras realizadas pelos sensores
CREATE TABLE [dbo].[LEITURA_SENSOR] (
    [LEI_ID] [bigint] IDENTITY(1,1) NOT NULL,  -- Identificador �nico para cada leitura, gerado automaticamente
    [LEI_SENSOR_ID] [bigint] NOT NULL,         -- Refer�ncia ao sensor que fez a leitura (chave estrangeira)
    [LEI_CULTURA_ID] [bigint] NOT NULL,        -- Refer�ncia � cultura relacionada � leitura (chave estrangeira)
    [LEI_DATA_HORA] [datetime] NOT NULL,       -- Data e hora da leitura do sensor
    [LEI_VALOR] [float] NOT NULL,              -- Valor da leitura (ex: n�vel de umidade, pH, nutrientes)
PRIMARY KEY CLUSTERED 
(
    [LEI_ID] ASC  -- Definindo LEI_ID como chave prim�ria da tabela
) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
GO

-- Definindo a rela��o entre LEITURA_SENSOR e SENSOR, garantindo integridade referencial
ALTER TABLE [dbo].[LEITURA_SENSOR] 
WITH CHECK ADD CONSTRAINT [FK_LEI_SENSOR_ID] FOREIGN KEY([LEI_SENSOR_ID])
REFERENCES [dbo].[SENSOR] ([SEN_ID])  -- LEI_SENSOR_ID deve corresponder a um SEN_ID existente
ON UPDATE CASCADE  -- Se SEN_ID for atualizado, a mudan�a reflete em LEI_SENSOR_ID
ON DELETE CASCADE; -- Se SEN_ID for deletado, as leituras associadas tamb�m ser�o deletadas
GO

-- Definindo a rela��o entre LEITURA_SENSOR e CULTURA, garantindo integridade referencial
ALTER TABLE [dbo].[LEITURA_SENSOR] 
WITH CHECK ADD CONSTRAINT [FK_LEI_CULTURA_ID] FOREIGN KEY([LEI_CULTURA_ID])
REFERENCES [dbo].[CULTURA] ([CUL_ID])  -- LEI_CULTURA_ID deve corresponder a um CUL_ID existente
ON UPDATE CASCADE  -- Se CUL_ID for atualizado, a mudan�a reflete em LEI_CULTURA_ID
ON DELETE CASCADE; -- Se CUL_ID for deletado, as leituras associadas tamb�m ser�o deletadas
GO

-- Cria��o da tabela AJUSTE_APLICACAO para armazenar os ajustes realizados na aplica��o de �gua e nutrientes
CREATE TABLE [dbo].[AJUSTE_APLICACAO] (
    [AJU_ID] [bigint] IDENTITY(1,1) NOT NULL,  -- Identificador �nico para cada ajuste, gerado automaticamente
    [AJU_CULTURA_ID] [bigint] NOT NULL,        -- Refer�ncia � cultura que recebeu o ajuste (chave estrangeira)
    [AJU_DATA_HORA] [datetime] NOT NULL,       -- Data e hora do ajuste realizado
    [AJU_QUANTIDADE_AGUA] [float] NOT NULL,    -- Quantidade de �gua aplicada no ajuste
    [AJU_QUANTIDADE_NUTRIENTES] [float] NOT NULL, -- Quantidade de nutrientes aplicados no ajuste
PRIMARY KEY CLUSTERED 
(
    [AJU_ID] ASC  -- Definindo AJU_ID como chave prim�ria da tabela
) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
GO

-- Definindo a rela��o entre AJUSTE_APLICACAO e CULTURA, garantindo integridade referencial
ALTER TABLE [dbo].[AJUSTE_APLICACAO] 
WITH CHECK ADD CONSTRAINT [FK_AJU_CULTURA_ID] FOREIGN KEY([AJU_CULTURA_ID])
REFERENCES [dbo].[CULTURA] ([CUL_ID])  -- AJU_CULTURA_ID deve corresponder a um CUL_ID existente
ON UPDATE CASCADE  -- Se CUL_ID for atualizado, a mudan�a reflete em AJU_CULTURA_ID
ON DELETE CASCADE; -- Se CUL_ID for deletado, os ajustes associados tamb�m ser�o deletados
GO

-- Views para analise dos dados


-- View para calcular a quantidade total de �gua aplicada em cada m�s
CREATE VIEW [dbo].[VIEW_AJUSTE_APLICACAO_MENSAL] AS
SELECT 
    YEAR(AJU_DATA_HORA) AS Ano,
    MONTH(AJU_DATA_HORA) AS Mes,
    SUM(AJU_QUANTIDADE_AGUA) AS Total_Agua
FROM 
    [dbo].[AJUSTE_APLICACAO]
GROUP BY 
    YEAR(AJU_DATA_HORA), MONTH(AJU_DATA_HORA);
GO

-- View para analisar as varia��es do n�vel de pH ao longo do ano
CREATE VIEW [dbo].[VIEW_LEITURA_PH_ANUAL] AS
SELECT 
    YEAR(LEI_DATA_HORA) AS Ano,
    MONTH(LEI_DATA_HORA) AS Mes,
    AVG(CASE WHEN S.SEN_TIPO = 'pH' THEN LEI_VALOR END) AS Media_PH
FROM 
    [dbo].[LEITURA_SENSOR] L
JOIN 
    [dbo].[SENSOR] S ON L.LEI_SENSOR_ID = S.SEN_ID
GROUP BY 
    YEAR(LEI_DATA_HORA), MONTH(LEI_DATA_HORA);
GO

-- View para calcular a m�dia de nutrientes aplicados por cultura
CREATE VIEW [dbo].[VIEW_NUTRIENTES_APLICADOS] AS
SELECT 
    C.CUL_NOME AS Cultura,
    AVG(AJU_QUANTIDADE_NUTRIENTES) AS Media_Nutrientes
FROM 
    [dbo].[AJUSTE_APLICACAO] A
JOIN 
    [dbo].[CULTURA] C ON A.AJU_CULTURA_ID = C.CUL_ID
GROUP BY 
    C.CUL_NOME;
GO

-- View para verificar a aplica��o de �gua e nutrientes em cada cultura
CREATE VIEW [dbo].[VIEW_APLICACAO_AGUA_NUTRIENTES_CULTURA] AS
SELECT 
    C.CUL_NOME AS Cultura,
    SUM(AJU_QUANTIDADE_AGUA) AS Total_Agua_Aplicada,
    SUM(AJU_QUANTIDADE_NUTRIENTES) AS Total_Nutrientes_Aplicados
FROM 
    [dbo].[AJUSTE_APLICACAO] A
JOIN 
    [dbo].[CULTURA] C ON A.AJU_CULTURA_ID = C.CUL_ID
GROUP BY 
    C.CUL_NOME;
GO

-- View para analisar as leituras de umidade ao longo do tempo
CREATE VIEW [dbo].[VIEW_LEITURAS_UMIDADE] AS
SELECT 
    YEAR(LEI_DATA_HORA) AS Ano,
    MONTH(LEI_DATA_HORA) AS Mes,
    AVG(CASE WHEN S.SEN_TIPO = 'umidade' THEN LEI_VALOR END) AS Media_Umidade
FROM 
    [dbo].[LEITURA_SENSOR] L
JOIN 
    [dbo].[SENSOR] S ON L.LEI_SENSOR_ID = S.SEN_ID
GROUP BY 
    YEAR(LEI_DATA_HORA), MONTH(LEI_DATA_HORA);
GO


