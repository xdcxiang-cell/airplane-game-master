"""Language handling module for bilingual UI."""

from typing import Dict, Any

class LanguageManager:
    def __init__(self, default_language: str = 'en') -> None:
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {
            'en': {
                'game_title': 'Airplane Battle',
                'score': 'Score',
                'hp': 'HP',
                'game_over': 'Game Over',
                'final_score': 'Final Score',
                'restart': 'Restart',
                'quit': 'Quit'
            },
            'zh': {
                'game_title': '飞行大战',
                'score': '得分',
                'hp': '生命值',
                'game_over': '游戏结束',
                'final_score': '最终得分',
                'restart': '重新开始',
                'quit': '退出'
            }
        }
    
    def switch_language(self, language: str) -> None:
        """Switch the current language."""
        if language in self.translations:
            self.current_language = language
    
    def translate(self, key: str, **kwargs: Any) -> str:
        """Translate a key to the current language, with optional formatting."""
        translation = self.translations[self.current_language].get(key, key)
        return translation.format(**kwargs)