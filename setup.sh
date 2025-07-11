#!/bin/bash
# THOR Agent Setup Script with ElevenLabs Support

echo "🔨 THOR Agent Setup Script"
echo "========================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - ANTHROPIC_API_KEY (required for Claude)"
    echo "   - ELEVENLABS_API_KEY (required for voice)"
    echo "   - ELEVENLABS_VOICE_ID (your preferred voice)"
    echo "   - PICOVOICE_ACCESS_KEY (optional for wake word)"
    echo ""
fi

# Create necessary directories
mkdir -p logs
mkdir -p config/wake_words

# Download Whisper model
echo "Downloading Whisper model (this may take a while)..."
python3 -c "import whisper; whisper.load_model('base')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Get your ElevenLabs voice ID:"
echo "   - Go to https://elevenlabs.io/app/voice-lab"
echo "   - Copy your preferred voice ID"
echo "   - Add it to .env as ELEVENLABS_VOICE_ID"
echo ""
echo "3. Start LM Studio and load Phi-4 Mini Reasoning:"
echo "   - Open LM Studio"
echo "   - Load 'phi-4-mini-reasoning' model"
echo "   - Start local server on port 1234"
echo ""
echo "4. Run THOR:"
echo "   source venv/bin/activate"
echo "   python src/main.py"
echo ""
echo "🎤 THOR is ready for voice commands!"
