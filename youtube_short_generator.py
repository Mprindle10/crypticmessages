"""
YouTube Short #1 Content Generator for Cryptic Message Service
Complete production package with Caesar cipher focus
"""

import random
import string
from typing import Tuple, List, Dict

class YouTubeShortGenerator:
    """Generate complete content for YouTube Short #1"""
    
    @staticmethod
    def generate_caesar_cipher(message: str, shift: int = 3) -> Tuple[str, str]:
        """Generate Caesar cipher for YouTube short"""
        encrypted = ""
        
        for char in message.upper():
            if char.isalpha():
                shifted = ord(char) - ord('A')
                shifted = (shifted + shift) % 26
                encrypted += chr(shifted + ord('A'))
            else:
                encrypted += char
                
        return encrypted, message.upper()
    
    @staticmethod
    def create_animation_steps() -> List[Dict]:
        """Create step-by-step reveal for animation"""
        message = "THIS IS A TEST"
        encrypted, _ = YouTubeShortGenerator.generate_caesar_cipher(message)
        
        steps = []
        for i, (orig, enc) in enumerate(zip(message, encrypted)):
            if orig.isalpha():
                steps.append({
                    'position': i,
                    'encrypted': enc,
                    'original': orig,
                    'shift_demo': f"{enc} → {orig} (shift -3)",
                    'timing': 9 + (i * 0.8)  # Staggered reveal timing
                })
        
        return steps
    
    @staticmethod
    def generate_script_data() -> Dict:
        """Generate all script data for YouTube Short #1"""
        main_challenge = YouTubeShortGenerator.generate_caesar_cipher("THIS IS A TEST")
        animation_steps = YouTubeShortGenerator.create_animation_steps()
        
        return {
            'title': 'Can You Crack This 2000-Year-Old Code?',
            'duration': 30,
            'target_audience': 'Puzzle enthusiasts who want to feel smart',
            'main_challenge': {
                'encrypted': main_challenge[0],
                'solution': main_challenge[1],
                'explanation': 'Caesar cipher with 3-letter shift'
            },
            'script_segments': {
                'hook': {
                    'time': '0-3s',
                    'voiceover': 'Julius Caesar used this code 2000 years ago... can YOUR brain crack it?',
                    'visual': 'Ancient Roman scroll unrolling',
                    'text_overlay': 'GENIUS TEST'
                },
                'challenge': {
                    'time': '4-8s',
                    'voiceover': 'This message has stumped people for centuries',
                    'visual': f'Dramatic zoom into: {main_challenge[0]}',
                    'text_overlay': 'Can you solve it?'
                },
                'solution': {
                    'time': '9-15s',
                    'voiceover': 'Here\'s the secret: shift each letter back 3 positions',
                    'visual': 'Letters shifting animation',
                    'animation_steps': animation_steps
                },
                'reveal': {
                    'time': '16-22s',
                    'voiceover': 'Congratulations! You just cracked Caesar\'s cipher!',
                    'visual': f'Golden reveal: {main_challenge[1]}',
                    'text_overlay': 'YOU\'RE A CRYPTOGRAPHER!'
                },
                'upsell': {
                    'time': '23-27s',
                    'voiceover': 'Ready for 272 MORE mind-bending puzzles?',
                    'visual': 'Montage of complex ciphers',
                    'text_overlay': '21-Month Genius Journey'
                },
                'cta': {
                    'time': '28-30s',
                    'voiceover': 'Join Cipher Academy Beta',
                    'visual': 'Beta signup form preview',
                    'button': 'Start Your Journey → crypticmessages.com/beta'
                }
            },
            'hashtags': ['#cryptography', '#puzzle', '#genius', '#caesar', '#codebreaking', '#shorts'],
            'description': 'Test your genius with Julius Caesar\'s secret cipher! Can you crack this 2000-year-old code? Join our beta for 272 more mind-bending challenges. Link in bio! 🔐🧠',
            'thumbnail_text': 'CAN YOU CRACK IT?'
        }

# Generate content for production
def create_production_package():
    """Create complete production package"""
    generator = YouTubeShortGenerator()
    script_data = generator.generate_script_data()
    
    return {
        'script': script_data,
        'technical_specs': {
            'aspect_ratio': '9:16',
            'resolution': '1080x1920',
            'frame_rate': '30fps',
            'duration': '30 seconds',
            'audio_format': '48kHz stereo'
        },
        'props_needed': [
            'Ancient Roman scroll (aged parchment)',
            'Wax seal for authenticity',
            'Dramatic lighting setup',
            'Gold foil for text effects'
        ],
        'software_requirements': [
            'After Effects for animations',
            'Premiere Pro for editing',
            'Audition for audio',
            'Photoshop for graphics'
        ]
    }

if __name__ == "__main__":
    package = create_production_package()
    print("🎬 YouTube Short #1 Production Package Generated!")
    print(f"Title: {package['script']['title']}")
    print(f"Challenge: {package['script']['main_challenge']['encrypted']}")
    print(f"Solution: {package['script']['main_challenge']['solution']}")
    print(f"Hashtags: {', '.join(package['script']['hashtags'])}")
