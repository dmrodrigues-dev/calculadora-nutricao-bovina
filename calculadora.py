# Calculadora de Nutrição Bovina
# Autor: Davi Matos Rodrigues
# GitHub: github.com/dmrodrigues-dev

import pandas as pd
import os
from datetime import date

MENU = {
    0: {'nome': 'Calcular Ração'},
    1: {'nome': 'Consultar Histórico'},
    2: {'nome': 'Cadastrar novo ingrediente'},
    3: {'nome': 'Sair'}

}

CATEGORIAS = {
    0: {"nome": "Bezerro (até 6 meses)", "percentual_ms": 0.03, "proteina_min": 16},
    1: {"nome": "Novilha (7-18 meses)", "percentual_ms": 0.025, "proteina_min": 14},
    2: {"nome": "Vaca em lactação", "percentual_ms": 0.035, "proteina_min": 18},
    3: {"nome": "Vaca seca", "percentual_ms": 0.02, "proteina_min": 12},
    4: {"nome": "Touro", "percentual_ms": 0.022, "proteina_min": 13},
}

COLUNAS_HISTORICO = ['data',
                     'categoria',
                     'peso',
                     'ingrediente 1',
                     'Kg ingrediente 1',
                     'ingrediente 2',
                     'Kg ingrediente 2',
                     'matéria seca/dia',
                     'custo diário',
                     'custo mensal',
                     'atende proteína']

COLUNAS_INGREDIENTES = ['nome',
                        'proteina',
                        'preco_kg']

def arq_existe(nome_arquivo, colunas, default=False):
    if os.path.exists(nome_arquivo):
        print(f'{nome_arquivo} encontrado.')
    else:
        print(f'{nome_arquivo} não encontrado, criando arquivo...')
        df = pd.DataFrame(columns=colunas)
        df.to_csv(nome_arquivo, index=False)
        if default:
            for i in [{"nome": "Milho grão", "proteina": 8.5, "preco_kg": 1.20},
                      {"nome": "Farelo de soja", "proteina": 45.0, "preco_kg": 3.50},
                      {"nome": "Silagem de milho", "proteina": 7.0, "preco_kg": 0.35},
                      {"nome": "Feno de tifton", "proteina": 10.0, "preco_kg": 1.80},
                      {"nome": "Capim-elefante", "proteina": 9.0, "preco_kg": 0.25},]:
                novo_registro(nome_arquivo, i)
        print(f'Arquivo criado em {nome_arquivo}')


def exibir_menu(titulo, opcoes, saida=False):
    print(f"\n{'='*45}")
    print(f"  {titulo}")
    print(f"{'='*45}")
    for chave, valor in opcoes.items():
        nome = valor["nome"]
        print(f"  [{chave+1}] {nome}")
    if saida:
        print(f'  [x] Terminar seleção')
    print(f"{'='*45}")


def obter_opcao(opcoes, mensagem):
    while True:
        escolha = input(mensagem).strip()
        if escolha == 'x':
            return escolha
        elif escolha.isdigit():
            if int(escolha)-1 in opcoes:
                return int(escolha)-1
        print("  ⚠ Opção inválida. Tente novamente.")


def validar_float(texto, minimo, maximo):
    while True:
        try:
            dado = float(input(f"  {texto}: ").strip())
            if minimo <= dado <= maximo:
                return dado
            else:
                print('  Dado fora do intervalo aceito!')
        except ValueError:
            print("  Digite apenas números (ex: 450 ou 450.5).")


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


def receber_ing():
    retorno = {'nome': input('  Nome - '),
               'proteina': validar_float('Proteína', 0, 100),
               'preco_kg': validar_float('Preço do Kg ', 0, 500)}
    return retorno


def selecionar_ing(ingredientes):
    selec_ing = []
    while len(selec_ing) < 2:
        chave_ing = obter_opcao(ingredientes, "  Escolha o alimento: ")
        if chave_ing == "x":
            if selec_ing != []:
                break
        elif chave_ing in selec_ing:
            continue
        else:
            selec_ing.append(chave_ing)
    return selec_ing


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


def exibir_racoes():
    rac_df = pd.read_csv('arquivo.csv')
    registros = dict(rac_df.iterrows())
    if not registros:
        print('  Não há rações salvas no histórico.')
        return
    for i in registros:
        racao = registros[i]
        for j in racao.keys():
            racao[j] = str(racao[j])
        print(f'  {racao['data']} | {racao['categoria'].ljust(21,' ')} | {racao["peso"].ljust(5,' ')} Kg | '
              f'{racao["ingrediente 1"].ljust(16,' ')} | {racao['Kg ingrediente 1'].ljust(5,' ')} Kg | '
              f'{racao['ingrediente 2'].ljust(16,' ')} | {racao['Kg ingrediente 2'].ljust(5,' ')} Kg | '
              f'{racao['matéria seca/dia'].ljust(5,' ')} Kg/dia | R$ {racao['custo diário'].ljust(6,' ')}/dia | '
              f'R$ {racao['custo mensal'].ljust(6,' ')}/mês | '
              f'{('Atende proteína' if racao['atende proteína'] else 'Não atende proteína').ljust(19,' ')}')


def main():
    print("\n" + "="*45)
    print("  🐄 CALCULADORA DE NUTRIÇÃO BOVINA")
    print("  Desenvolvido por: Davi Matos Rodrigues")
    print("="*45)
    arq_existe('arquivo.csv', COLUNAS_HISTORICO)
    arq_existe('ingredientes.csv', COLUNAS_INGREDIENTES, True)


    while True:
        ing_df = pd.read_csv('ingredientes.csv')
        INGREDIENTES = dict(ing_df.iterrows())

        exibir_menu("MENU PRINCIPAL", MENU)
        chave_menu = obter_opcao(MENU, '  Escolha uma opção: ')
        if chave_menu == 0:

            exibir_menu("CATEGORIA DO ANIMAL", CATEGORIAS)
            chave_cat = obter_opcao(CATEGORIAS, "  Escolha a categoria: ")
            categoria = CATEGORIAS[chave_cat]
            peso = validar_float('Informe o peso do animal (kg)',0, 1500)

            exibir_menu("TIPO DE ALIMENTO", INGREDIENTES, True)
            selec_ing_index = selecionar_ing(INGREDIENTES)

            selec_ing = [INGREDIENTES[int(i)] for i in selec_ing_index]
            resultado = calcular(peso, categoria, selec_ing)
            exibir_resultado(peso, categoria, resultado)
            dados_montados = montar_dados(categoria, peso, resultado)
            novo_registro('arquivo.csv', dados_montados)

            input("  Pressione qualquer tecla para continuar: ")

        elif chave_menu == 1:
            print("\n" + "="*45)
            print('  Exibir Histórico')
            print("=" * 45)
            exibir_racoes()

        elif chave_menu == 2:
            print("\n" + "="*45)
            print('  Cadastrar ingrediente')
            print("=" * 45)
            novo_ing = receber_ing()
            novo_registro('ingredientes.csv', novo_ing)

        elif chave_menu == 3:
            print("\n" + "="*45)
            print('  Fechando programa...')
            print("=" * 45)
            break


if __name__ == "__main__":
    main()
