"""Multi-language support for the game."""

class LanguageManager:
    def __init__(self, language: str = 'zh'):
        self.language = language
        self.translations = {
            'zh': {
                'title': '飞行大战',
                'health': '生命值: {0}',
                'score': '得分: {0}',
                'game_over': '游戏结束!',
                'final_score': '最终得分: {0}',
                'play_again': '再来一次 (按R键)',
                'quit': '退出 (按Q键)',
                'instructions': '使用←→键移动，空格键射击'
            },
            'en': {
                'title': 'Airplane Battle',
                'health': 'Health: {0}',
                'score': 'Score: {0}',
                'game_over': 'Game Over!',
                'final_score': 'Final Score: {0}',
                'play_again': 'Play Again (Press R)',
                'quit': 'Quit (Press Q)',
                'instructions': 'Use ←→ keys to move, Space to shoot'
            }
        }
    
    def set_language(self, language: str) -> None:
        """Set the current language."""
        if language in self.translations:
            self.language = language
    
    def get_text(self, key: str, *args) -> str:
        """Get translated text for a given key."""
        return self.translations[self.language][key].format(*args)
    
    def toggle_language(self) -> None:
        """Toggle between Chinese and English."""
        if self.language == 'zh':
            self.set_language('en')
        else:
            self.set_language('zh')
