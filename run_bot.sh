#!/bin/bash

# Script para executar o bot Selenium com ambiente virtual
echo "🤖 Executando Selenium Bot..."
echo "📁 Diretório: $(pwd)"

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se Chrome está instalado
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null && ! command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" &> /dev/null; then
    echo "⚠️  Aviso: Google Chrome não encontrado. Certifique-se de que o Chrome está instalado."
fi

# Executar o bot
echo "🚀 Iniciando bot..."
python selenium_bot.py

echo "✅ Execução concluída!"
echo "📄 Verifique os arquivos de log gerados para ver os resultados."