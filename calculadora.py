# Calculadora de Nutrição Bovina
# Autor: Davi Matos Rodrigues
# GitHub: github.com/dmrodrigues-dev

import pandas as pd
import os
from datetime import date

CATEGORIAS = {
    "1": {"nome": "Bezerro (até 6 meses)", "percentual_ms": 0.03, "proteina_min": 16},
    "2": {"nome": "Novilha (7-18 meses)", "percentual_ms": 0.025, "proteina_min": 14},
    "3": {"nome": "Vaca em lactação", "percentual_ms": 0.035, "proteina_min": 18},
    "4": {"nome": "Vaca seca", "percentual_ms": 0.02, "proteina_min": 12},
    "5": {"nome": "Touro", "percentual_ms": 0.022, "proteina_min": 13},
}

INGREDIENTES = {
    "1": {"nome": "Milho grão", "proteina": 8.5, "preco_kg": 1.20},
    "2": {"nome": "Farelo de soja", "proteina": 45.0, "preco_kg": 3.50},
    "3": {"nome": "Silagem de milho", "proteina": 7.0, "preco_kg": 0.35},
    "4": {"nome": "Feno de tifton", "proteina": 10.0, "preco_kg": 1.80},
    "5": {"nome": "Capim-elefante", "proteina": 9.0, "preco_kg": 0.25},
    "0": {"nome": "Finalizar seleção"}
}

def arq_existe(nome_arquivo):
    if os.path.exists(nome_arquivo):
        print('Histórico encontrado.')
    else:
        print('Histórico não encontrado, criando arquivo...')
        df = pd.DataFrame(columns=['data',
                                   'categoria',
                                   'peso',
                                   'ingrediente 1',
                                   'Kg ingrediente 1',
                                   'ingrediente 2',
                                   'Kg ingrediente 2',
                                   'matéria seca/dia',
                                   'custo diário',
                                   'custo mensal',
                                   'atende proteína'])
        df.to_csv(nome_arquivo, index=False)
        print(f'Histórico criado em {nome_arquivo}')


def exibir_menu(titulo, opcoes):
    print(f"\n{'='*45}")
    print(f"  {titulo}")
    print(f"{'='*45}")
    for chave, valor in opcoes.items():
        nome = valor["nome"]
        print(f"  [{chave}] {nome}")
    print(f"{'='*45}")


def obter_opcao(opcoes, mensagem):
    while True:
        escolha = input(mensagem).strip()
        if escolha in opcoes:
            return escolha
        print("  ⚠ Opção inválida. Tente novamente.")


def obter_peso():
    while True:
        try:
            peso = float(input("\n  Informe o peso do animal (kg): ").strip())
            if peso <= 0:
                print("  ⚠ O peso deve ser maior que zero.")
            elif peso > 1500:
                print("  ⚠ Peso muito alto. Verifique o valor informado.")
            else:
                return peso
        except ValueError:
            print("  ⚠ Digite apenas números (ex: 450 ou 450.5).")


def calcular(peso, categoria, ingredientes):
    necessidade_ms = peso * categoria["percentual_ms"]
    necessidade_proteina = categoria['proteina_min']
    if len(ingredientes) == 2:
        ing_alto = max(ingredientes, key=lambda i: i["proteina"])
        ing_baixo = min(ingredientes, key=lambda i: i["proteina"])

        if ing_alto["proteina"] < necessidade_proteina:
            custo_diario = necessidade_ms * ing_alto["preco_kg"]
            atende_proteina = ing_alto["proteina"] >= categoria["proteina_min"]
            peso_ing = [{"nome": ing_alto["nome"],
                         "peso": necessidade_ms},
                        {"nome": ing_baixo["nome"],
                         "peso": 0}]

        elif ing_baixo["proteina"] >= necessidade_proteina:
            ing = min(ingredientes, key=lambda i: i["preco_kg"])
            custo_diario = necessidade_ms * ing["preco_kg"]
            atende_proteina = ing_alto["proteina"] >= categoria["proteina_min"]
            peso_ing = [{"nome": ing["nome"],
                         "peso": necessidade_ms},
                        {"nome": (max(ingredientes, key=lambda i: i["preco_kg"]))["nome"],
                         "peso": 0}]

        else:
            result = calcular_dois_ingredientes(necessidade_ms, necessidade_proteina, ing_alto, ing_baixo, categoria)
            custo_diario = result["custo_diario"]
            atende_proteina = result["atende_proteina"]
            peso_ing = result["peso_ing"]

    else:
        custo_diario = necessidade_ms * ingredientes[0]["preco_kg"]
        atende_proteina = ingredientes[0]["proteina"] >= categoria["proteina_min"]
        peso_ing = [{"nome": ingredientes[0]["nome"],
                     "peso": necessidade_ms}]

    custo_mensal = custo_diario * 30

    return {
        "necessidade_ms": necessidade_ms,
        "custo_diario": custo_diario,
        "custo_mensal": custo_mensal,
        "atende_proteina": atende_proteina,
        "pesos": peso_ing,
            }


def calcular_dois_ingredientes(necessidade_ms, necessidade_proteina, ing_alto, ing_baixo, categoria):
    ing_alto_part = necessidade_proteina - ing_baixo["proteina"]
    ing_baixo_part = ing_alto["proteina"] - necessidade_proteina
    ing_alto_per = ing_alto_part / (ing_alto_part + ing_baixo_part)
    ing_baixo_per = ing_baixo_part / (ing_alto_part + ing_baixo_part)
    ing_alto_kg = necessidade_ms * ing_alto_per
    ing_baixo_kg = necessidade_ms * ing_baixo_per

    return {
        'custo_diario': ing_alto_kg * ing_alto["preco_kg"] + ing_baixo_kg * ing_baixo["preco_kg"],
        'atende_proteina': ing_alto_per * ing_alto["proteina"] + ing_baixo_per * ing_baixo["proteina"] >= categoria["proteina_min"],
        'peso_ing': [{"nome": ing_alto["nome"],
                 "peso": ing_alto_kg},
                {"nome": ing_baixo["nome"],
                 "peso": ing_baixo_kg}]
    }


def montar_dados(categoria, peso, resultado):
    return {
            'data': date.today().strftime("%d/%m/%Y"),
            'categoria': categoria['nome'],
            'peso': peso,
            'ingrediente 1': resultado['pesos'][0]['nome'],
            'Kg ingrediente 1': f'{resultado['pesos'][0]['peso']:.2f}',
            'ingrediente 2': resultado['pesos'][1]['nome'] if len(resultado['pesos']) > 1 else None,
            'Kg ingrediente 2': f'{resultado['pesos'][1]['peso']:.2f}' if len(resultado['pesos']) > 1 else None,
            'matéria seca/dia': f'{resultado['necessidade_ms']:.2f}',
            'custo diário': f'{resultado['custo_diario']:.2f}',
            'custo mensal': f'{resultado['custo_mensal']:.2f}',
            'atende proteína': resultado['atende_proteina']
            }


def novo_registro(nome_arquivo, dados):
    nova_linha = pd.DataFrame([dados])
    nova_linha.to_csv(nome_arquivo,mode='a', header=False, index=False)


def exibir_resultado(peso, categoria, resultado):
    print(f"\n{'='*45}")
    print(f"  RESULTADO DO CÁLCULO")
    print(f"{'='*45}")
    print(f"  Animal     : {categoria['nome']}")
    print(f"  Peso       : {peso:.1f} kg")
    print(f"{'='*45}")
    print(f"  Matéria seca/dia : {resultado['necessidade_ms']:.2f} kg")
    print(f"  Custo diário     : R$ {resultado['custo_diario']:.2f}")
    print(f"  Custo mensal     : R$ {resultado['custo_mensal']:.2f}")
    for p in resultado["pesos"]:
        print(f"  Peso de {p['nome']} : KG {p['peso']:.2f}")

    print(f"{'='*45}")

    proteina_status = (
        "✅ Atende à exigência proteica mínima"
        if resultado["atende_proteina"]
        else f"⚠ ATENÇÃO: Proteína insuficiente!\n"
             f"  Mínimo recomendado: {categoria['proteina_min']}%"
    )
    print(f"  {proteina_status}")
    print(f"{'='*45}\n")


def main():
    print("\n" + "="*45)
    print("  🐄 CALCULADORA DE NUTRIÇÃO BOVINA")
    print("  Desenvolvido por: Davi Matos Rodrigues")
    print("="*45)
    arq_existe('arquivo.csv')

    while True:
        exibir_menu("CATEGORIA DO ANIMAL", CATEGORIAS)
        chave_cat = obter_opcao(CATEGORIAS, "  Escolha a categoria: ")
        categoria = CATEGORIAS[chave_cat]

        peso = obter_peso()

        exibir_menu("TIPO DE ALIMENTO", INGREDIENTES)
        selec_ing_index = []
        while len(selec_ing_index) < 2:
            chave_ing = obter_opcao(INGREDIENTES, "  Escolha o alimento: ")
            if chave_ing == "0":
                if selec_ing_index != []:
                    break
            elif chave_ing in selec_ing_index:
                continue
            else:
                selec_ing_index.append(chave_ing)

        selec_ing = [INGREDIENTES[i] for i in selec_ing_index]
        resultado = calcular(peso, categoria, selec_ing)
        exibir_resultado(peso, categoria, resultado)
        dados_montados = montar_dados(categoria, peso, resultado)
        novo_registro('arquivo.csv', dados_montados)

        continuar = input("  Deseja calcular novamente? (s/n): ").strip().lower()
        if continuar != "s":
            print("\n  Até logo! 🐄\n")
            break


if __name__ == "__main__":
    main()
