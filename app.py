# ============================================================
# app.py — Flask 主程序
# ============================================================

from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
import io
import base64
from config import HOST, PORT, DEBUG, MAX_UPLOAD_MB, ALLOWED_EXTENSIONS, COLOR_MODES
from pixel_engine import pixelate, to_png_bytes, to_svg_string

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", color_modes=COLOR_MODES)


@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "没有上传图片"}), 400

    file = request.files["image"]
    if not allowed_file(file.filename):
        return jsonify({"error": "不支持的图片格式"}), 400

    pixel_size = int(request.form.get("pixel_size", 16))
    color_mode = request.form.get("color_mode", "full")
    export_format = request.form.get("export_format", "png")
    keep_alpha = request.form.get("keep_alpha", "false") == "true"

    num_colors = COLOR_MODES.get(color_mode, {}).get("colors")

    try:
        img = Image.open(file.stream)
        result = pixelate(img, pixel_size, color_mode, num_colors, keep_alpha)

        if export_format == "svg":
            svg_str = to_svg_string(result, pixel_size)
            svg_b64 = base64.b64encode(svg_str.encode()).decode()
            return jsonify({
                "format": "svg",
                "data": svg_b64,
                "width": result.width,
                "height": result.height,
            })
        else:
            png_bytes = to_png_bytes(result)
            png_b64 = base64.b64encode(png_bytes).decode()
            return jsonify({
                "format": "png",
                "data": png_b64,
                "width": result.width,
                "height": result.height,
            })

    except Exception as e:
        return jsonify({"error": f"处理失败：{str(e)}"}), 500


@app.route("/preview", methods=["POST"])
def preview():
    """快速低分辨率预览接口（Python后端处理，缩小到128px宽）"""
    if "image" not in request.files:
        return jsonify({"error": "没有上传图片"}), 400

    file = request.files["image"]
    pixel_size = int(request.form.get("pixel_size", 16))
    color_mode = request.form.get("color_mode", "full")
    num_colors = COLOR_MODES.get(color_mode, {}).get("colors")

    try:
        img = Image.open(file.stream)
        # 缩小到 128px 宽做快速预览
        preview_w = 128
        ratio = preview_w / img.width
        preview_h = max(1, int(img.height * ratio))
        img_small = img.resize((preview_w, preview_h), Image.BOX)

        # 预览用最小像素块（至少1px）
        preview_pixel = max(1, int(pixel_size * ratio))
        result = pixelate(img_small, preview_pixel, color_mode, num_colors)

        png_bytes = to_png_bytes(result)
        png_b64 = base64.b64encode(png_bytes).decode()
        return jsonify({"data": png_b64})

    except Exception as e:
        return jsonify({"error": f"预览失败：{str(e)}"}), 500


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
