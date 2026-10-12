import math
import csv
import statistics
from pathlib import Path

# Diretório principal dos resultados
BASE = Path.home() / "projeto-real" / "resultados-metricas"

ENTRADA = BASE / "coleta-api"
SAIDA = BASE / "analise-api"

# Cria a pasta onde salvaremos as tabelas
SAIDA.mkdir(parents=True, exist_ok=True)

# Métricas escolhidas para análise
METRICAS_CLASSE = [
    "loc",
    "cbo",
    "cboModified",
    "fanin",
    "fanout",
    "wmc",
    "dit",
    "noc",
    "rfc",
    "lcom",
    "lcom*",
    "tcc",
    "lcc",
    "totalMethodsQty",
    "totalFieldsQty",
    "nosi",
    "loopQty",
    "comparisonsQty",
    "maxNestedBlocksQty",
    "uniqueWordsQty"
]

METRICAS_METODO = [
    "loc",
    "wmc",
    "parametersQty",
    "methodsInvokedQty",
    "loopQty",
    "comparisonsQty",
    "maxNestedBlocksQty"
]


def ler_csv(nome_arquivo):
    caminho = ENTRADA / nome_arquivo

    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def analisar(registros, metricas, nivel):
    resultados = []
    extremos = []

    for metrica in metricas:
        valores = []

        for registro in registros:
            valor = registro.get(metrica, "")

            if valor not in ("", None):
                try:
                    numero = float(valor)

                    # CK usa -1 para indicar TCC/LCC nao aplicaveis
                    if metrica in("tcc", "lcc") and numero == -1:
                        continue

                    # Ignora NaN e valores infinitos
                    if math.isfinite(numero):
                        valores.append((numero, registro))

                except ValueError:
                    continue

        if not valores:
            print(f"Sem dados para: {metrica}")
            continue

        numeros = [item[0] for item in valores]
        maior = max(numeros)

        resultados.append({
            "nivel": nivel,
            "metrica": metrica,
            "quantidade": len(numeros),
            "media": round(statistics.mean(numeros), 2),
            "mediana": round(statistics.median(numeros), 2),
            "minimo": min(numeros),
            "maximo": maior
        })

        # Registra todos os elementos empatados no maximo
        for numero, registro in valores:
            if numero == maior:
                extremos.append({
                    "nivel": nivel,
                    "metrica": metrica,
                    "valor": numero,
                    "classe": registro.get("class", ""),
                    "metodo": registro.get("method", ""),
                    "arquivo": registro.get("file", ""),
                    "linha": registro.get("line", "")
                })

    return resultados, extremos


def salvar_csv(nome, registros):
    if not registros:
        return

    caminho = SAIDA / nome

    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=registros[0].keys()
        )
        escritor.writeheader()
        escritor.writerows(registros)

    print(f"Arquivo gerado: {caminho}")


classes = ler_csv("class.csv")
metodos = ler_csv("method.csv")

print(f"Registros de classes: {len(classes)}")
print(f"Registros de métodos: {len(metodos)}")

resumo_classes, extremos_classes = analisar(
    classes, METRICAS_CLASSE, "classe"
)

resumo_metodos, extremos_metodos = analisar(
    metodos, METRICAS_METODO, "metodo"
)

salvar_csv(
    "resumo_metricas.csv",
    resumo_classes + resumo_metodos
)

salvar_csv(
    "valores_extremos.csv",
    extremos_classes + extremos_metodos
)

print("Análise finalizada!")
