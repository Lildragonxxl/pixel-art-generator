# ============================================================
# config.py — 统一配置，后续维护只需修改此文件
# ============================================================

# Flask 服务配置
HOST = "0.0.0.0"
PORT = 8080
DEBUG = False

# 上传限制
MAX_UPLOAD_MB = 20
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}

# 像素化参数范围
PIXEL_SIZE_MIN = 4
PIXEL_SIZE_MAX = 64
PIXEL_SIZE_DEFAULT = 16

# 色彩风格定义
COLOR_MODES = {
    "full":     {"label": "全彩",     "colors": None},
    "64color":  {"label": "64 色",    "colors": 64},
    "32color":  {"label": "32 色",    "colors": 32},
    "16color":  {"label": "16 色",    "colors": 16},
    "8color":   {"label": "8 色",     "colors": 8},
    "gameboy":  {"label": "GameBoy",  "colors": None},  # 特殊调色板
    "bw":       {"label": "黑白",     "colors": 2},
}

# GameBoy 调色板（4色）
GAMEBOY_PALETTE = [
    (15, 56, 15),
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15),
]
