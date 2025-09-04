#!/usr/bin/env python3
"""
Review Agent CLI

Command-line interface for the Review Agent system.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.platforms.mock import MockPlatform
from review_agent.utils.simple_voice import SimpleVoiceProcessor

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Review Agent - AI-powered review management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  review-agent demo                    # Run basic demo
  review-agent voice                   # Run voice demo
  review-agent generate --help         # Generate single review
  
For more information, visit: https://github.com/brian-olson/review-agent
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    demo_parser.add_argument('--voice', action='store_true', help='Use voice demo')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a single review')
    generate_parser.add_argument('--business', required=True, help='Business name')
    generate_parser.add_argument('--experience', required=True, help='Experience description')
    generate_parser.add_argument('--rating', type=int, choices=[1,2,3,4,5], required=True, help='Rating (1-5)')
    generate_parser.add_argument('--location', help='Business location')
    generate_parser.add_argument('--date', help='Visit date (YYYY-MM-DD)')
    generate_parser.add_argument('--no-post', action='store_true', help='Generate only, do not post')
    
    # Voice command
    voice_parser = subparsers.add_parser('voice', help='Process voice input')
    voice_parser.add_argument('--file', help='Audio file path')
    voice_parser.add_argument('--business', help='Business name')
    voice_parser.add_argument('--rating', type=int, choices=[1,2,3,4,5], help='Rating (1-5)')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')
    
    args = parser.parse_args()
    
    if args.command == 'demo':
        run_demo(use_voice=args.voice)
    elif args.command == 'generate':
        run_generate(args)
    elif args.command == 'voice':
        run_voice(args)
    elif args.command == 'version':
        print("Review Agent v0.1.0")
        print("https://github.com/brian-olson/review-agent")
    else:
        parser.print_help()

def run_demo(use_voice=False):
    """Run the demonstration."""
    if use_voice:
        print("🎤 Running Voice Demo...")
        from voice_demo_auto import voice_demo_auto
        voice_demo_auto()
    else:
        print("🤖 Running Basic Demo...")
        from demo import demo_review_agent
        demo_review_agent()

def run_generate(args):
    """Generate a single review."""
    print(f"🤖 Generating review for {args.business}...")
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create review input
    review_input = ReviewInput(
        business_name=args.business,
        experience_text=args.experience,
        rating=args.rating,
        visit_date=args.date
    )
    
    # Generate review
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            agent = ReviewAgent(api_key=api_key)
            review = agent.generate_review(review_input)
        except Exception as e:
            print(f"AI generation failed: {e}")
            review = generate_fallback_review(review_input)
    else:
        print("⚠️  No OpenAI API key found, using fallback generator...")
        review = generate_fallback_review(review_input)
    
    print("\n📝 Generated Review:")
    print("=" * 50)
    print(review)
    print("=" * 50)
    
    if not args.no_post:
        # Post to mock platforms
        print("\n📤 Posting to platforms...")
        platform = MockPlatform("Demo Platform")
        platform.login({"username": "cli_user", "password": "demo"})
        business_id = platform.search_business(args.business, args.location)
        result = platform.post_review(business_id, review, args.rating)
        print("✅ Review posted successfully!")

def run_voice(args):
    """Process voice input."""
    voice_processor = SimpleVoiceProcessor()
    
    if args.file:
        print(f"🎤 Processing audio file: {args.file}")
        try:
            experience_text = voice_processor.process_audio_file(args.file)
        except FileNotFoundError:
            print(f"❌ Audio file not found: {args.file}")
            return
    else:
        print("🎤 No audio file specified, using simulation...")
        experience_text = voice_processor.record_voice_simulation()
    
    if args.business and args.rating:
        # Generate review from voice input
        review_input = ReviewInput(
            business_name=args.business,
            experience_text=experience_text,
            rating=args.rating
        )
        
        # Load environment and generate
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                agent = ReviewAgent(api_key=api_key)
                review = agent.generate_review(review_input)
                print(f"\n📝 Generated Review:\n{review}")
            except Exception as e:
                print(f"AI generation failed: {e}")
        else:
            print("⚠️  Add OPENAI_API_KEY to .env for AI generation")
    else:
        print(f"\n💬 Transcribed Text:\n{experience_text}")

def generate_fallback_review(review_input):
    """Generate a simple review without AI."""
    rating_text = {
        5: "Excellent experience!",
        4: "Very good experience.",
        3: "Good experience overall.",
        2: "Okay experience, could be better.",
        1: "Poor experience."
    }
    
    review = f"I visited {review_input.business_name} and {review_input.experience_text} "
    review += f"{rating_text.get(review_input.rating, 'Had an experience.')} "
    review += f"I would rate this {review_input.rating} out of 5 stars."
    
    if review_input.rating >= 4:
        review += " Highly recommended!"
    elif review_input.rating <= 2:
        review += " Hope they can improve."
    
    return review

if __name__ == "__main__":
    main()