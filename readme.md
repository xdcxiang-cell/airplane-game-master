## 飞行大战（pygame）

一个使用 `pygame` 编写的纵版射击小游戏，支持英雄飞机移动/射击、敌机巡航与随机射击、子弹碰撞判定、爆炸动画和素材集中管理。项目遵循 PEP 20 “The Zen of Python” 所倡导的清晰、模块化设计，核心逻辑拆分在 `game/` 包中，便于维护与扩展。

### 功能概览
- **英雄飞机**：左右移动、发射子弹，命中敌机会重置敌机位置，被击中后播放爆炸动画并结束游戏。
- **敌机与子弹**：敌机水平往返移动并按概率发射子弹，子弹越界自动清理，命中英雄触发失败。
- **资源管理**：`GameAssets` 集中加载图片素材，减少重复 IO。
- **输入系统**：同时支持离散按键事件和持续按键状态，确保操作顺畅。
- **基础碰撞**：英雄与敌机/子弹之间的碰撞采用 `pygame.Rect` 检测。

### 环境要求
- Python 3.10+
- `pygame` >= 2.5

### 安装与运行
```bash
python -m venv .venv
source .venv/bin/activate          # Windows 使用 .venv\Scripts\activate
pip install pygame

python app.py
```

### 项目结构
```
airplane-game-master/
├── app.py                 # 入口：初始化、主循环
├── game/
│   ├── __init__.py
│   ├── assets.py          # 素材加载
│   ├── constants.py       # 全局常量
│   ├── hero.py            # 英雄飞机
│   ├── enemy.py           # 敌机逻辑
│   ├── bullet.py          # 子弹实体
│   ├── collision.py       # 碰撞处理
│   └── input_handler.py   # 键盘监听
└── feiji/                 # 游戏素材
```

### 操作说明
- `← / A`：向左移动
- `→ / D`：向右移动
- `Space`：发射子弹

### 未来迭代建议
- 增加得分、生命值、关卡等 HUD。
- 支持多敌机/多波次与不同 AI 行为。
- 加入道具、音效、暂停菜单等提升体验的功能。
- 提供打包脚本（如 `pyinstaller`）方便发布。

欢迎基于当前模块化结构继续扩展玩法，如需帮助请随时提出！

