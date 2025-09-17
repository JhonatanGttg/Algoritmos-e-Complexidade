#!/usr/bin/env python3
"""
Script to help setup Safari for automation
"""

import subprocess
import sys

def setup_safari_automation():
    """Guide user to enable Safari automation"""
    print("🔧 Configurando Safari para automação...")
    print()
    print("Para usar o Safari com Selenium, você precisa habilitar a automação remota:")
    print()
    print("1. Abra o Safari")
    print("2. Vá em Safari > Configurações (ou Preferências)")
    print("3. Clique na aba 'Avançado'")
    print("4. Marque a opção 'Mostrar menu Desenvolver na barra de menus'")
    print("5. Vá em Desenvolver > Permitir Automação Remota")
    print()
    print("Depois disso, o bot poderá usar o Safari!")
    print()
    
    # Try to open Safari developer settings
    try:
        subprocess.run(["open", "-a", "Safari"], check=True)
        print("✅ Safari foi aberto. Siga as instruções acima.")
    except subprocess.CalledProcessError:
        print("❌ Não foi possível abrir o Safari automaticamente.")
        print("Por favor, abra o Safari manualmente e siga as instruções.")
    
    input("\nPressione ENTER após configurar o Safari...")

if __name__ == "__main__":
    setup_safari_automation()