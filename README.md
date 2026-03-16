# Blender-Module-Dissector

A minimal Flask web app for uploading a Blender `.blend` file and inspecting its header metadata (Blender version, pointer size, and endianness).

## ✅ What it does

- Accepts a `.blend` upload
- Parses the Blender file header (magic bytes, pointer size, endianness, and version)
- Displays the extracted metadata in a clean UI

## 🚀 Getting Started

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the app

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## 🧩 Next steps (ideas)

- Parse more structure from `.blend` files (data-block tables, library links, etc.)
- Add file history / session tracking
- Add a REST API endpoint for automated inspection
