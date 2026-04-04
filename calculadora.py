# Calculadora de Nutrição Bovina
# Autor: Davi Matos Rodrigues
# GitHub: github.com/dmrodrigues-dev

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
}


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


def calcular(peso, categoria, ingrediente):
    necessidade_ms = peso * categoria["percentual_ms"]
    custo_diario = necessidade_ms * ingrediente["preco_kg"]
    custo_mensal = custo_diario * 30
    atende_proteina = ingrediente["proteina"] >= categoria["proteina_min"]

    return {
        "necessidade_ms": necessidade_ms,
        "custo_diario": custo_diario,
        "custo_mensal": custo_mensal,
        "atende_proteina": atende_proteina,
    }


def exibir_resultado(peso, categoria, ingrediente, resultado):
    print(f"\n{'='*45}")
    print(f"  RESULTADO DO CÁLCULO")
    print(f"{'='*45}")
    print(f"  Animal     : {categoria['nome']}")
    print(f"  Peso       : {peso:.1f} kg")
    print(f"  Alimento   : {ingrediente['nome']}")
    print(f"{'='*45}")
    print(f"  Matéria seca/dia : {resultado['necessidade_ms']:.2f} kg")
    print(f"  Custo diário     : R$ {resultado['custo_diario']:.2f}")
    print(f"  Custo mensal     : R$ {resultado['custo_mensal']:.2f}")
    print(f"{'='*45}")

    proteina_status = (
        "✅ Atende à exigência proteica mínima"
        if resultado["atende_proteina"]
        else f"⚠ ATENÇÃO: Proteína insuficiente!\n"
             f"  Mínimo recomendado: {categoria['proteina_min']}% | "
             f"Alimento: {ingrediente['proteina']}%"
    )
    print(f"  {proteina_status}")
    print(f"{'='*45}\n")


def main():
    print("\n" + "="*45)
    print("  🐄 CALCULADORA DE NUTRIÇÃO BOVINA")
    print("  Desenvolvido por: Davi Matos Rodrigues")
    print("="*45)

    while True:
        exibir_menu("CATEGORIA DO ANIMAL", CATEGORIAS)
        chave_cat = obter_opcao(CATEGORIAS, "  Escolha a categoria: ")
        categoria = CATEGORIAS[chave_cat]

        peso = obter_peso()

        exibir_menu("TIPO DE ALIMENTO", INGREDIENTES)
        chave_ing = obter_opcao(INGREDIENTES, "  Escolha o alimento: ")
        ingrediente = INGREDIENTES[chave_ing]

        resultado = calcular(peso, categoria, ingrediente)
        exibir_resultado(peso, categoria, ingrediente, resultado)

        continuar = input("  Deseja calcular novamente? (s/n): ").strip().lower()
        if continuar != "s":
            print("\n  Até logo! 🐄\n")
            break


if __name__ == "__main__":
    main()
