#!/bin/bash
# Simple script to run the WhatsApp Message Sender UI

echo "🚀 Starting WhatsApp Message Sender UI..."
echo "📱 Make sure WhatsApp Web is logged in before sending messages!"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed!"
    echo "📦 Installing requirements..."
    pip install -r requirements_ui.txt
fi

# Run the Streamlit app
streamlit run ui_app.py

