#!/usr/bin/env python3
"""
Arquivo principal do projeto Python.
Este é o ponto de entrada da aplicação.
"""

def saudacao(nome: str) -> str:
    """
    Retorna uma saudação personalizada.
    
    Args:
        nome (str): Nome da pessoa a ser saudada
        
    Returns:
        str: Mensagem de saudação
    """
    return f"Olá, {nome}! Bem-vindo ao seu projeto Python!"

def calcular_soma(a: float, b: float) -> float:
    """
    Calcula a soma de dois números.
    
    Args:
        a (float): Primeiro número
        b (float): Segundo número
        
    Returns:
        float: Soma dos dois números
    """
    return a + b

def main():
    """Função principal que executa o programa."""
    print("=" * 50)
    print("PROJETO PYTHON INICIADO COM SUCESSO!")
    print("=" * 50)
    
    # Exemplo de uso das funções
    nome = input("Digite seu nome: ")
    print(saudacao(nome))
    
    # Exemplo de cálculo
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    resultado = calcular_soma(num1, num2)
    print(f"A soma de {num1} + {num2} = {resultado}")
    
    print("\nProjeto executado com sucesso!")

if __name__ == "__main__":
    main()
