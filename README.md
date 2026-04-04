# 🐄 Calculadora de Nutrição Bovina

Ferramenta desenvolvida em Python para calcular a necessidade diária de matéria seca e o custo de alimentação de bovinos, com base no peso e categoria do animal.

## 💡 Motivação

Projeto desenvolvido para unir conhecimento em Medicina Veterinária com programação em Python, aplicando conceitos reais de nutrição animal em uma ferramenta prática para o agronegócio.

## ⚙️ Funcionalidades

- Seleção de categoria animal (bezerro, novilha, vaca em lactação, vaca seca, touro)
- Cálculo da necessidade diária de matéria seca com base no peso vivo
- Estimativa de custo diário e mensal por tipo de alimento
- Alerta automático quando o alimento não atende à exigência proteica mínima da categoria

## 🐾 Categorias suportadas

| Categoria | % Matéria Seca | Proteína mínima |
|---|---|---|
| Bezerro (até 6 meses) | 3,0% | 16% |
| Novilha (7–18 meses) | 2,5% | 14% |
| Vaca em lactação | 3,5% | 18% |
| Vaca seca | 2,0% | 12% |
| Touro | 2,2% | 13% |

## 🌾 Alimentos disponíveis

- Milho grão
- Farelo de soja
- Silagem de milho
- Feno de tifton
- Capim-elefante

## 🚀 Como usar

**Pré-requisito:** Python 3.7 ou superior instalado.

```bash
# Clone o repositório
git clone https://github.com/dmrodrigues-dev/calculadora-nutricao-bovina.git

# Acesse a pasta
cd calculadora-nutricao-bovina

# Execute o programa
python calculadora.py
```

## 📋 Exemplo de uso

```
==========================================
  🐄 CALCULADORA DE NUTRIÇÃO BOVINA
  Desenvolvido por: Davi Matos Rodrigues
==========================================

  [1] Bezerro (até 6 meses)
  [2] Novilha (7-18 meses)
  [3] Vaca em lactação
  [4] Vaca seca
  [5] Touro

  Escolha a categoria: 3
  Informe o peso do animal (kg): 550

  [1] Milho grão
  [2] Farelo de soja
  ...

==========================================
  RESULTADO DO CÁLCULO
==========================================
  Animal     : Vaca em lactação
  Peso       : 550.0 kg
  Alimento   : Farelo de soja
==========================================
  Matéria seca/dia : 19.25 kg
  Custo diário     : R$ 67.38
  Custo mensal     : R$ 2021.25
==========================================
  ✅ Atende à exigência proteica mínima
==========================================
```

## 🛠️ Tecnologias

- Python 3 (sem dependências externas)

## 📚 Referências técnicas

- Nutrient Requirements of Beef Cattle — NRC
- Tabelas de exigências nutricionais para bovinos — Embrapa

## 👨‍💻 Autor

**Davi Matos Rodrigues**  
Estudante de Medicina Veterinária (UFPI) e ADS (Uninter)  
[GitHub](https://github.com/dmrodrigues-dev) · [LinkedIn](https://linkedin.com/in/seu-perfil)

---

> Projeto em desenvolvimento — novas funcionalidades em breve.
