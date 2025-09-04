#!/usr/bin/env python3
"""
Script para verificar a configuração do Python no Cursor
"""

import sys
import os
import subprocess

print("=" * 60)
print("VERIFICAÇÃO DO PYTHON NO CURSOR")
print("=" * 60)

# Informações do Python atual
print(f"Python executável: {sys.executable}")
print(f"Versão do Python: {sys.version}")
print(f"Diretório do Python: {os.path.dirname(sys.executable)}")

# Verificar se pandas está disponível
try:
    import pandas as pd
    print(f"✓ Pandas instalado: {pd.__version__}")
except ImportError as e:
    print(f"✗ Erro ao importar pandas: {e}")

# Listar todos os Pythons disponíveis no sistema
print("\n" + "=" * 60)
print("PYTHONS DISPONÍVEIS NO SISTEMA:")
print("=" * 60)

try:
    # Tentar encontrar pythons no PATH
    result = subprocess.run(['where', 'python'], capture_output=True, text=True)
    if result.stdout:
        pythons = result.stdout.strip().split('\n')
        for i, python_path in enumerate(pythons, 1):
            print(f"{i}. {python_path}")
    else:
        print("Nenhum python encontrado no PATH")
except:
    print("Erro ao buscar pythons no sistema")

print("\n" + "=" * 60)
print("INSTRUÇÕES PARA CONFIGURAR O CURSOR:")
print("=" * 60)
print("1. Pressione Ctrl+Shift+P")
print("2. Digite 'Python: Select Interpreter'")
print("3. Selecione: " + sys.executable)
print("4. Reinicie o Cursor se necessário")
print("=" * 60)

