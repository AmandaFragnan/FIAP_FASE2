use 

pip install -r requirements.txt

to install all dependencies.

# Projeto: Sistema de Sensoriamento para Agricultura

Este repositório contém o modelo de banco de dados e o código desenvolvido para o sistema de sensoriamento de uma plantação. O sistema coleta dados de sensores em tempo real e faz ajustes automáticos na irrigação e aplicação de nutrientes, utilizando uma base de dados Oracle.

## Objetivo

O objetivo do sistema é otimizar o uso de água e nutrientes, ajustando automaticamente a quantidade aplicada com base nos dados coletados por três tipos de sensores (umidade, pH, nutrientes) instalados em diferentes culturas.

## Estrutura do Banco de Dados (MER)

### Entidades e Atributos:

#### 1. Entidade **Sensor**
- **sensorId (PK)**: Identificador único do sensor
- **tipoSensor (varchar)**: Tipo de sensor (Umidade, pH, Nutrientes)
- **descricao (varchar)**: Descrição detalhada do sensor

#### 2. Entidade **Leitura**
- **leituraId (PK)**: Identificador da leitura
- **sensorId (FK)**: Referência ao sensor que coletou a leitura
- **dataHora (timestamp)**: Data e hora da leitura
- **valor (double)**: Valor lido pelo sensor (umidade, pH, nutrientes)

#### 3. Entidade **Cultura**
- **culturaId (PK)**: Identificador único da cultura
- **nomeCultura (varchar)**: Nome da cultura plantada (milho, alface, tomate)
- **areaCultivada (double)**: Área cultivada em hectares

#### 4. Entidade **AplicacaoAgua**
- **aplicacaoAguaId (PK)**: Identificador da aplicação de água
- **culturaId (FK)**: Cultura que recebeu a aplicação
- **dataHoraAplicacao (timestamp)**: Data e hora da aplicação de água
- **quantidadeAgua (double)**: Quantidade de água aplicada (em litros)

#### 5. Entidade **AplicacaoNutriente**
- **aplicacaoNutrienteId (PK)**: Identificador da aplicação de nutrientes
- **culturaId (FK)**: Cultura que recebeu a aplicação
- **dataHoraAplicacao (timestamp)**: Data e hora da aplicação de nutrientes
- **quantidadeFosforo (double)**: Quantidade de fósforo aplicada (em gramas)
- **quantidadePotassio (double)**: Quantidade de potássio aplicada (em gramas)

### Relacionamentos
- Cada **Cultura** pode ter várias **Aplicacoes de Agua** (1:N).
- Cada **Cultura** pode ter várias **Aplicacoes de Nutriente** (1:N).
- Cada **Sensor** pode ter várias **Leituras** (1:N).

## Diagrama MER

inserir uma imagem para o diagrama MER


## Tecnologias Utilizadas

- **VSCode** para o desenvolvimento do código.
- **Oracle** como banco de dados relacional.
- **SQLDesigner** para criar o diagrama de Entidade-Relacionamento (MER).
- **Markdown** para a documentação no GitHub.
- **GitHub** para versionamento de código.

## Configuração do Ambiente de Desenvolvimento

### Requisitos:

1. **Visual Studio Code (VSCode)**: Editor de código para escrever o código SQL e de integração com o banco de dados.
2. **Oracle Database**: Base de dados para armazenamento das informações.
3. **Oracle SQL Developer** ou outro cliente para interagir com o Oracle Database.

### Configuração do Banco de Dados Oracle:

1. Instale o Oracle Database localmente ou use uma instância em nuvem.
2. Conecte-se ao banco de dados usando o Oracle SQL Developer ou outro cliente.
3. Crie as tabelas necessárias usando os scripts
