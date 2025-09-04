# Contributing to Review Agent

Thank you for your interest in contributing to Review Agent! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/review-agent.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements-minimal.txt`
5. Make your changes
6. Test your changes: `python demo.py` and `python voice_demo_auto.py`
7. Commit and push your changes
8. Create a Pull Request to **OpenFluxLabs/review-agent**

## 🎯 Priority Areas for Contributions

### High Priority
- **Real Platform Integrations**: Implement actual APIs for Google, Yelp, Trustpilot
- **Enhanced Voice Processing**: OpenAI Whisper integration, real-time recording
- **Error Handling**: Better error recovery and user feedback
- **Testing**: Unit tests, integration tests, CI/CD improvements

### Medium Priority
- **Web Interface**: Flask/FastAPI web UI
- **Advanced AI Prompts**: Multiple review styles, customization
- **Review Management**: Editing, scheduling, analytics
- **Documentation**: API docs, tutorials, examples

### Low Priority
- **Mobile App**: React Native or Flutter app
- **Browser Extension**: Chrome/Firefox extensions
- **Batch Processing**: Multiple reviews at once
- **Review Templates**: Pre-defined review formats

## 🏗️ Development Setup

### Environment Setup
```bash
# Clone the repo
git clone https://github.com/OpenFluxLabs/review-agent.git
cd review-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-minimal.txt

# Install development dependencies (optional)
pip install -r requirements.txt  # May fail on some systems
```

### Project Structure
```
review_agent/
├── agent.py                 # Core ReviewAgent class
├── platforms/               # Platform integrations
│   ├── base.py             # Abstract base class
│   ├── mock.py             # Mock implementation
│   └── [platform].py       # Real platform implementations
└── utils/                   # Utility modules
    ├── voice_processor.py   # Voice processing
    └── simple_voice.py      # Simplified voice processing
```

## 🧪 Testing

### Running Tests
```bash
# Basic functionality test
python -c "from review_agent.agent import ReviewAgent; print('✅ Import test passed')"

# Run demos
python demo.py
python voice_demo_auto.py

# Check file generation
ls mock_reviews/
ls audio_input/
```

### Adding Tests
- Create test files in `tests/` directory
- Use pytest for unit tests
- Test both success and failure cases
- Mock external API calls

## 📝 Code Style

### Python Style Guidelines
- Follow PEP 8
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example Code Style
```python
from typing import Optional, Dict, Any

class ExamplePlatform(ReviewPlatform):
    """
    Example platform implementation.
    
    This class demonstrates the expected code style and structure.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the platform with optional API key."""
        self.api_key = api_key
        self.is_authenticated = False
    
    def login(self, credentials: Dict[str, str]) -> bool:
        """
        Authenticate with the platform.
        
        Args:
            credentials: Dictionary containing authentication info
            
        Returns:
            bool: True if authentication successful
            
        Raises:
            ValueError: If credentials are invalid
        """
        # Implementation here
        pass
```

## 🔧 Platform Integration Guidelines

### Adding a New Platform

1. **Create Platform File**: `review_agent/platforms/your_platform.py`
2. **Inherit from Base**: Extend `ReviewPlatform` class
3. **Implement Required Methods**:
   - `login(credentials)`: Authentication
   - `search_business(name, location)`: Business search
   - `post_review(business_id, text, rating)`: Review posting
4. **Add Error Handling**: Graceful failure and recovery
5. **Create Tests**: Unit tests for your platform
6. **Update Documentation**: Add usage examples

### Platform Implementation Template
```python
from .base import ReviewPlatform
from typing import Dict, Any

class YourPlatform(ReviewPlatform):
    def __init__(self):
        self.base_url = "https://api.yourplatform.com"
        self.session = requests.Session()
    
    def login(self, credentials: Dict[str, str]):
        # Implement authentication
        pass
    
    def search_business(self, business_name: str, location: str = None) -> str:
        # Implement business search
        pass
    
    def post_review(self, business_id: str, review_text: str, rating: int):
        # Implement review posting
        pass
```

## 📚 Documentation Guidelines

### Code Documentation
- Add docstrings to all public functions and classes
- Include parameter types and descriptions
- Provide usage examples
- Document any side effects or exceptions

### README Updates
- Update feature lists when adding functionality
- Add new usage examples
- Update installation instructions if needed
- Keep troubleshooting section current

## 🐛 Bug Reports

### Before Submitting
1. Check existing issues
2. Test with latest version
3. Try the minimal reproduction case

### Bug Report Template
```
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template
```
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Any alternative approaches?

**Additional Context**
Any other relevant information
```

## 🔒 Security Guidelines

### API Keys and Credentials
- Never commit API keys or passwords
- Use environment variables for sensitive data
- Document required environment variables
- Provide secure credential storage options

### Review Content
- Ensure all reviews are based on authentic experiences
- Respect platform terms of service
- Implement rate limiting
- Add user consent mechanisms

## 📋 Pull Request Process

### Before Submitting
1. Test your changes thoroughly
2. Update documentation if needed
3. Add/update tests for new features
4. Ensure CI tests pass
5. Follow code style guidelines

### PR Description Template
```
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
How has this been tested?

**Checklist**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to hard-to-understand areas
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CI tests pass
```

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate diverse perspectives

### Communication
- Use clear, concise language
- Be patient with new contributors
- Provide helpful feedback
- Ask questions when unsure

## 📞 Getting Help

### Where to Ask
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: Direct contact for sensitive issues

### Response Times
- Issues: Within 48 hours
- Pull Requests: Within 72 hours
- Questions: Within 24 hours (best effort)

Thank you for contributing to Review Agent! 🎉