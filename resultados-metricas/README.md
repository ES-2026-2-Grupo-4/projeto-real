# Coleta de Métricas — OpenMRS Core

## 1. Objetivo

Este diretório contém os arquivos e scripts utilizados na atividade **10.1.a — Coletar Métricas**, da disciplina de Engenharia de Software.

O objetivo foi coletar e analisar métricas estáticas de código Java do projeto OpenMRS Core, identificando características estruturais e elementos com valores extremos.

## 2. Projeto analisado

- **Projeto:** OpenMRS Core
- **Repositório original:** https://github.com/openmrs/openmrs-core
- **Versão:** 2.7.6
- **Commit analisado:** `d8057a05f2796c8286bbba914350cce45793736c`
- **Escopo:** `api/src/main/java`

A coleta abrangeu 820 registros de classes e 9.008 registros de métodos.

## 3. Ferramenta utilizada

Foi utilizada a ferramenta **CK (Chidamber & Kemerer Java Metrics)**, desenvolvida por Mauricio Aniche.

- **Repositório:** https://github.com/mauricioaniche/ck
- **Versão do projeto:** `0.7.1-SNAPSHOT`
- **Commit da ferramenta:** `8a1ef916d597d33ad619d748b616bb7dbc3f0c36`

Ambiente utilizado:

- Linux
- Java 21
- Apache Maven 3.8.7
- Python 3.12.3

## 4. Reprodução da coleta

Primeiro, obtenha o OpenMRS Core e selecione o commit indicado na seção 2.

Em seguida, clone e compile a ferramenta CK:

```bash
git clone https://github.com/mauricioaniche/ck.git
cd ck
git checkout 8a1ef916d597d33ad619d748b616bb7dbc3f0c36
mvn clean compile package
```

A partir do diretório da ferramenta CK, execute:

```bash
java -Xmx4g -jar target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar \
  /CAMINHO/DO/OPENMRS/api/src/main/java \
  false 0 false \
  /CAMINHO/DE/SAIDA
```

Substitua os caminhos pelos diretórios correspondentes em seu computador.

Os parâmetros utilizados foram:

- `false`: não informar dependências externas à ferramenta;
- `0`: utilizar o particionamento automático;
- `false`: não gerar métricas de variáveis e campos.

Os arquivos principais gerados foram `class.csv` e `method.csv`.

## 5. Organização dos arquivos

| Diretório | Descrição |
|---|---|
| `coleta-api/` | CSVs originais produzidos pelo CK |
| `analise-api/` | Resumo estatístico e valores extremos |
| `scripts/` | Script Python de processamento |
| `teste/` | Resultados do teste preliminar da ferramenta |

O teste preliminar foi realizado com três arquivos Java do próprio OpenMRS: `DoubleRange.java`, `NaturalStrings.java` e `DateUtil.java`.

## 6. Análise dos resultados

O script `scripts/analisarMetricas.py` processa os arquivos CSV originais e produz:

- `analise-api/resumo_metricas.csv`: estatísticas descritivas das métricas selecionadas;
- `analise-api/valores_extremos.csv`: registros associados aos valores máximos, incluindo empates.

Foram selecionadas 27 métricas para análise: 20 em nível de classe e 7 em nível de método.

Para executar o script a partir da raiz do repositório da equipe:

```bash
python3 resultados-metricas/scripts/analisarMetricas.py
```

## 7. Limitações e cuidados

A coleta foi restrita ao módulo `api/src/main/java`, portanto os resultados não representam todo o repositório OpenMRS Core.

A ferramenta foi executada sem informar dependências externas, o que pode afetar a resolução de tipos e a precisão de algumas métricas.

Durante o processamento, valores não finitos foram desconsiderados. Para TCC e LCC, também foram excluídos valores `-1`, utilizados pela implementação do CK para indicar casos sem valor razoável.

Os valores válidos de TCC e LCC encontrados nesta coleta foram iguais a zero. Por isso, esses resultados devem ser interpretados com cautela, sem concluir automaticamente que as classes não apresentam coesão.

