#!/usr/bin/env python3
"""
Testes unitários para o projeto Python.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from main import saudacao, calcular_soma

class TestMain:
    """Classe de testes para as funções do arquivo main.py"""
    
    def test_saudacao(self):
        """Testa a função de saudação."""
        resultado = saudacao("João")
        assert resultado == "Olá, João! Bem-vindo ao seu projeto Python!"
        
        resultado = saudacao("Maria")
        assert resultado == "Olá, Maria! Bem-vindo ao seu projeto Python!"
    
    def test_calcular_soma(self):
        """Testa a função de cálculo de soma."""
        resultado = calcular_soma(5, 3)
        assert resultado == 8
        
        resultado = calcular_soma(10.5, 2.5)
        assert resultado == 13.0
        
        resultado = calcular_soma(-5, 10)
        assert resultado == 5

if __name__ == "__main__":
    pytest.main([__file__])
