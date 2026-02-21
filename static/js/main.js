// ============================================================
// main.js — 前端交互逻辑
// ============================================================

const dropZone        = document.getElementById("drop-zone");
const fileInput       = document.getElementById("file-input");
const previewThumb    = document.getElementById("preview-thumb");
const fileName        = document.getElementById("file-name");
const pixelSlider     = document.getElementById("pixel-size");
const pixelVal        = document.getElementById("pixel-val");
const processBtn      = document.getElementById("process-btn");
const resultImg       = document.getElementById("result-img");
const downloadBtn     = document.getElementById("download-btn");
const loading         = document.getElementById("loading");
const infoBar         = document.getElementById("info-bar");
const infoSize        = document.getElementById("info-size");
const infoFmt         = document.getElementById("info-fmt");
const toast           = document.getElementById("toast");
const placeholder     = document.getElementById("placeholder");
const quickPreviewWrap = document.getElementById("quick-preview-wrap");
const quickPreviewImg  = document.getElementById("quick-preview-img");

let selectedFile   = null;
let selectedMode   = "full";
let selectedFormat = "png";
let keepAlpha      = false;
let resultData     = null;
let resultFormat   = null;
let previewTimer   = null;

// ── 滑块实时显示 + 触发预览 ──
pixelSlider.addEventListener("input", () => {
  pixelVal.textContent = pixelSlider.value + "px";
  schedulePreview();
});

// ── 色彩模式 pills ──
document.querySelectorAll(".pill").forEach(pill => {
  pill.addEventListener("click", () => {
    document.querySelectorAll(".pill").forEach(p => p.classList.remove("active"));
    pill.classList.add("active");
    selectedMode = pill.dataset.mode;
    schedulePreview();
  });
});

// ── 格式切换 ──
document.querySelectorAll(".fmt-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".fmt-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedFormat = btn.dataset.fmt;
  });
});

// ── 透明背景切换 ──
document.querySelectorAll(".alpha-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".alpha-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    keepAlpha = btn.dataset.alpha === "true";
  });
});

// ── 拖拽上传 ──
dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));

dropZone.addEventListener("drop", e => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) loadFile(file);
});

dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) loadFile(fileInput.files[0]);
});

function loadFile(file) {
  if (!file.type.startsWith("image/")) {
    showToast("请上传图片文件");
    return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    previewThumb.src = e.target.result;
    previewThumb.style.display = "block";
    fileName.textContent = file.name;
    fileName.style.display = "block";
    dropZone.querySelector(".upload-icon").textContent = "✅";
    schedulePreview();
  };
  reader.readAsDataURL(file);
}

// ── 实时预览（防抖 600ms，请求后端 /preview）──
function schedulePreview() {
  if (!selectedFile) return;
  clearTimeout(previewTimer);
  previewTimer = setTimeout(fetchPreview, 600);
}

async function fetchPreview() {
  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("pixel_size", pixelSlider.value);
  formData.append("color_mode", selectedMode);

  try {
    const res  = await fetch("/preview", { method: "POST", body: formData });
    const json = await res.json();
    if (json.data) {
      quickPreviewImg.src = "data:image/png;base64," + json.data;
      quickPreviewImg.style.display = "block";
      quickPreviewWrap.style.display = "block";
    }
  } catch (_) {
    // 预览失败静默处理，不影响主流程
  }
}

// ── 处理按钮 ──
processBtn.addEventListener("click", async () => {
  if (!selectedFile) { showToast("请先上传图片"); return; }

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("pixel_size", pixelSlider.value);
  formData.append("color_mode", selectedMode);
  formData.append("export_format", selectedFormat);
  formData.append("keep_alpha", keepAlpha ? "true" : "false");

  loading.classList.add("show");
  processBtn.disabled = true;
  resultImg.style.display = "none";
  placeholder.style.display = "flex";
  downloadBtn.style.display = "none";
  infoBar.style.display = "none";

  try {
    const res  = await fetch("/process", { method: "POST", body: formData });
    const json = await res.json();

    if (json.error) { showToast(json.error); return; }

    resultData   = json.data;
    resultFormat = json.format;

    if (json.format === "svg") {
      const svgStr = atob(json.data);
      const blob   = new Blob([svgStr], { type: "image/svg+xml" });
      resultImg.src = URL.createObjectURL(blob);
    } else {
      resultImg.src = "data:image/png;base64," + json.data;
    }

    resultImg.style.display = "block";
    placeholder.style.display = "none";
    downloadBtn.style.display = "inline-block";

    infoSize.textContent = json.width + " × " + json.height + "px";
    infoFmt.textContent  = json.format.toUpperCase();
    infoBar.style.display = "block";

  } catch (err) {
    showToast("请求失败，请检查服务是否启动");
  } finally {
    loading.classList.remove("show");
    processBtn.disabled = false;
  }
});

// ── 下载 ──
downloadBtn.addEventListener("click", () => {
  if (!resultData) return;
  const a = document.createElement("a");
  if (resultFormat === "svg") {
    const svgStr = atob(resultData);
    const blob   = new Blob([svgStr], { type: "image/svg+xml" });
    a.href = URL.createObjectURL(blob);
    a.download = "pixel-art.svg";
  } else {
    a.href = "data:image/png;base64," + resultData;
    a.download = "pixel-art.png";
  }
  a.click();
});

// ── Toast 提示 ──
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}
