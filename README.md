# 🎮 Pixel Art Generator — 像素风格图片生成器

把你的照片或图片，一键变成复古像素风格艺术！

---

## 📦 第一步：安装必要工具

### 1. 安装 Python

打开浏览器，访问 👉 https://www.python.org/downloads/

点击黄色大按钮「Download Python」下载并安装。

> ⚠️ 安装时记得勾选 **「Add Python to PATH」**，否则后续步骤会报错。

安装完成后，打开终端（Mac）或命令提示符（Windows），输入以下命令确认安装成功：

```
python3 --version
```

看到类似 `Python 3.x.x` 的输出就表示成功了。

---

## 🚀 第二步：启动程序

### Mac 用户

1. 打开「终端」（在启动台搜索「终端」或「Terminal」）
2. 把 `pixel-art` 文件夹拖入终端窗口，前面加上 `cd `（注意有空格），回车
3. 依次输入以下命令，每行输入后按回车：

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python app.py
```

### Windows 用户

1. 打开「命令提示符」（按 Win+R，输入 cmd，回车）
2. 输入 `cd`，空格，然后把 `pixel-art` 文件夹拖进窗口，回车
3. 依次输入以下命令，每行输入后按回车：

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python app.py
```

---

## 🌐 第三步：打开网页

程序启动后，终端会显示类似这样的内容：

```
 * Running on http://127.0.0.1:5000
```

打开浏览器（Chrome、Safari 均可），在地址栏输入：

```
http://localhost:5000
```

回车，就能看到操作界面了！

---

## 🖼️ 第四步：使用方法

界面分为左侧「控制面板」和右侧「预览区」，操作非常简单：

| 步骤 | 操作 |
|------|------|
| ① 上传图片 | 点击左侧虚线框，或直接把图片拖进去 |
| ② 调整像素块大小 | 拖动滑块，数值越大像素感越强 |
| ③ 选择色彩风格 | 点击色彩按钮，可选全彩、8色、GameBoy 等 |
| ④ 选择导出格式 | PNG（普通图片）或 SVG（矢量图，可无限放大） |
| ⑤ 生成 | 点击「✨ 生成像素风格」按钮 |
| ⑥ 下载 | 右侧预览满意后，点击「⬇ 下载」保存 |

---

## 🎨 色彩风格说明

| 风格 | 效果 |
|------|------|
| 全彩 | 保留原图所有颜色，只做像素化 |
| 32色 / 16色 / 8色 | 颜色数量越少，复古感越强 |
| GameBoy | 经典绿色四色调，像 1989 年的掌机游戏 |
| 黑白 | 纯黑白像素风 |

---

## ❓ 常见问题

**Q：终端显示「command not found: python3」？**
A：Python 没有正确安装，或安装时没有勾选「Add to PATH」，重新安装并勾选该选项。

**Q：浏览器打开 localhost:5000 显示「无法访问此网站」？**
A：程序还没启动，请先在终端运行 `venv/bin/python app.py`（Mac）或 `venv\Scripts\python app.py`（Windows）。

**Q：第二次使用还需要重新安装吗？**
A：不需要。第二次起只需运行最后一行启动命令即可：
- Mac：`venv/bin/python app.py`
- Windows：`venv\Scripts\python app.py`

**Q：关闭终端后网页就打不开了？**
A：正常现象。每次使用前都需要先在终端启动程序，用完后关闭终端即可停止服务。

---

## 🛑 停止程序

在终端窗口按 `Ctrl + C` 即可停止服务。

---

## 📁 文件说明（给有需要的人）

```
pixel-art/
├── app.py            # 后端服务主程序
├── pixel_engine.py   # 像素化算法核心
├── config.py         # 参数配置（可调整端口、文件大小限制等）
├── requirements.txt  # 依赖列表
├── static/           # 前端资源（CSS 样式、JS 脚本）
└── templates/        # 网页模板
```

如需修改默认端口（5000），打开 `config.py`，修改 `PORT = 5000` 这一行即可。
