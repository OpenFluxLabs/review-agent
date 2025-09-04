# Review Agent MVP 🎤

[![CI](https://github.com/OpenFluxLabs/review-agent/workflows/Review%20Agent%20CI/badge.svg)](https://github.com/OpenFluxLabs/review-agent/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An AI-powered review management system that generates and posts reviews across multiple platforms using voice input and LangChain.

## Features

- 🎤 **Voice Input Processing**: Convert voice recordings to text (file-based and simulated)
- 🤖 **AI Review Generation**: Uses LangChain and OpenAI to generate authentic reviews
- 📝 **Multi-Platform Posting**: Post to Google, Yelp, and other review platforms (currently mock implementation)
- ⭐ **Smart Rating Integration**: Contextual review generation based on ratings
- 📁 **Review Management**: Local storage and tracking of generated reviews
- 🔄 **Fallback Systems**: Works without API keys using mock generators

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd review-agent

# Install dependencies
pip install -r requirements-minimal.txt
```

### 2. Basic Setup

```bash
# Copy environment template
cp .env.example .env

# Add your OpenAI API key (optional but recommended)
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

### 3. Run Demos

```bash
# Basic demo with sample reviews
python3 demo.py

# Voice input demo (auto mode)
python3 voice_demo_auto.py

# Interactive example (requires manual input)
python3 example.py
```

## Usage Examples

### Voice-to-Review Workflow

```python
from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.utils.simple_voice import SimpleVoiceProcessor

# Initialize components
voice_processor = SimpleVoiceProcessor()
agent = ReviewAgent(api_key="your-openai-key")

# Process voice input (from file or simulation)
experience_text = voice_processor.process_audio_file("my_experience.wav")

# Create review
review_input = ReviewInput(
    business_name="Joe's Pizza",
    experience_text=experience_text,
    rating=5
)

# Generate and post review
review = agent.generate_review(review_input)
print(f"Generated: {review}")
```

### Platform Integration

```python
from review_agent.platforms.mock import MockPlatform
from review_agent.platforms.local_directory import LocalDirectoryPlatform

# Use mock platforms for testing
mock_platform = MockPlatform("Google Reviews")
mock_platform.login({"username": "demo", "password": "demo"})

# Search and post
business_id = mock_platform.search_business("Restaurant Name", "Location")
result = mock_platform.post_review(business_id, review_text, rating)
```

## Project Structure

```
review_agent/
├── __init__.py
├── agent.py                 # Main ReviewAgent class with LangChain
├── platforms/
│   ├── base.py             # Abstract platform interface
│   ├── mock.py             # Mock implementation for testing
│   ├── local_directory.py  # Local API platform
│   ├── facebook.py         # Facebook integration (skeleton)
│   ├── google.py           # Google Reviews (skeleton)
│   └── trustpilot.py       # Trustpilot integration (skeleton)
└── utils/
    ├── voice_processor.py   # Original voice processing (needs pyaudio)
    └── simple_voice.py      # Simplified voice processing

# Demo scripts
demo.py                      # Basic multi-review demo
voice_demo_auto.py          # Automated voice input demo
voice_demo.py               # Interactive voice demo
example.py                  # Interactive text input demo

# Configuration
requirements.txt             # Full dependencies (may have install issues)
requirements-minimal.txt     # Core dependencies only
.env.example                # Environment template
```

## Current Capabilities

### ✅ **Working MVP Features:**
- Text and simulated voice input
- AI-powered review generation using LangChain + OpenAI
- Mock platform posting (Google, Yelp, TripAdvisor simulation)
- Local review storage and management
- Fallback systems when APIs unavailable
- File-based voice processing
- Interactive and automated demos

### 🚧 **In Development:**
- Real platform integrations (Google, Yelp APIs)
- Real-time microphone recording
- Advanced review customization
- Web interface

### 📋 **Planned Features:**
- Batch review processing
- Review scheduling
- Multiple review styles (professional, casual, detailed)
- Review analytics and management dashboard

## Voice Input Options

### Option 1: File-Based (Recommended for MVP)
1. Record audio on your phone/computer
2. Save as .wav or .mp3 in `audio_input/` directory
3. Run voice demo to process

### Option 2: Simulated Voice (For Testing)
- Uses text input to simulate voice transcription
- Perfect for testing the full workflow

### Option 3: Real Voice Recording (Advanced Setup)
```bash
# Install audio dependencies (may require system packages)
sudo apt-get install portaudio19-dev  # Linux
# or
brew install portaudio                # macOS

# Install Python packages
pip install pyaudio SpeechRecognition
```

## Demo Outputs

The system generates:
- **Review files**: Saved in `mock_reviews/` as JSON
- **Voice transcriptions**: Saved in `audio_input/` as text files
- **Console output**: Real-time processing feedback

### Sample Generated Review

**Input**: "Amazing pasta, friendly staff, cozy atmosphere. The tiramisu was incredible!"

**Generated Review**: 
> I visited Mario's Italian Bistro and had this to say: Amazing pasta, friendly staff, cozy atmosphere. The tiramisu was incredible! Excellent experience! I would rate this 5 out of 5 stars. Highly recommended!

## Configuration

### Environment Variables (.env)
```bash
# Required for AI generation (recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For future real platform integrations
GOOGLE_EMAIL=your_google_email
GOOGLE_PASSWORD=your_google_password
YELP_API_KEY=your_yelp_api_key
FACEBOOK_ACCESS_TOKEN=your_facebook_token
```

## Next Steps for Production

1. **Real Platform Integration**
   - Implement Trustpilot API (most accessible)
   - Add Facebook Business reviews
   - Research Google/Yelp API alternatives

2. **Enhanced Voice Processing**
   - Integrate OpenAI Whisper API
   - Add real-time microphone recording
   - Support multiple audio formats

3. **Advanced Features**
   - Review templates and styles
   - Batch processing
   - Review scheduling
   - Analytics dashboard

4. **User Interface**
   - Web interface with file upload
   - Mobile app integration
   - Browser extension

## Contributing

Focus areas for contributions:
- Real platform API integrations
- Enhanced voice processing
- Better error handling and retry logic
- UI/UX improvements
- Testing and validation

## Legal Notes

- Ensure compliance with platform terms of service
- Only post authentic reviews based on real experiences
- Respect rate limiting and anti-spam measures
- Consider disclosure requirements for automated reviews

## Troubleshooting

### Common Issues:

1. **Import errors**: Use `requirements-minimal.txt` instead of full requirements
2. **No audio files**: Use simulation mode or add sample files to `audio_input/`
3. **API key missing**: System works in fallback mode without OpenAI key
4. **Platform posting fails**: Currently expected - using mock implementations

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Feel free to check [issues page](https://github.com/OpenFluxLabs/review-agent/issues).

## 📝 License

This project is [MIT](LICENSE) licensed.

## 🏢 Organization

**OpenFluxLabs**
- GitHub: [@OpenFluxLabs](https://github.com/OpenFluxLabs)
- Website: Coming soon!

## 👨‍💻 Lead Developer

**Brian Olson**
- GitHub: [@brian-olson](https://github.com/brian-olson)

---

<div align="center">
  <strong>Built with ❤️ by OpenFluxLabs</strong>
</div>