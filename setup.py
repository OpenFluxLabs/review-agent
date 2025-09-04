from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements-minimal.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="review-agent",
    version="0.1.0",
    author="OpenFluxLabs",
    author_email="contact@openfluxlabs.com",  # Update with actual email
    description="AI-powered review management system with voice input and multi-platform posting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenFluxLabs/review-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Communications",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "full": [
            "pyaudio>=0.2.11",
            "SpeechRecognition>=3.8.1",
            "selenium>=4.1.0",
            "beautifulsoup4>=4.9.3",
        ],
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "review-agent=review_agent.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/OpenFluxLabs/review-agent/issues",
        "Source": "https://github.com/OpenFluxLabs/review-agent",
        "Documentation": "https://github.com/OpenFluxLabs/review-agent#readme",
    },
)