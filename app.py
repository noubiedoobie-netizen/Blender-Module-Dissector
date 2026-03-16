import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-in-production")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max upload size


def parse_blend_header(stream):
    """Parse the first bytes of a .blend file and return basic metadata."""
    header = stream.read(12)
    if len(header) < 12:
        raise ValueError("File is too small to be a valid Blender file.")

    if not header.startswith(b"BLENDER"):
        raise ValueError("File does not start with the Blender magic bytes.")

    pointer_size = header[7:8].decode("ascii", errors="replace")
    endianness = header[8:9].decode("ascii", errors="replace")
    version = header[9:12].decode("ascii", errors="replace")

    return {
        "pointer_size": "64-bit" if pointer_size == "_" else "32-bit" if pointer_size == "-" else f"unknown ({pointer_size})",
        "endianness": "little" if endianness == "v" else "big" if endianness == "V" else f"unknown ({endianness})",
        "version": version,
    }


def analyze_python_source(source_text: str) -> dict:
    """Return simple analysis of a Python source file."""
    return {
        "lines": len(source_text.splitlines()),
        "functions": len([_ for _ in source_text.splitlines() if _.strip().startswith("def ")]),
        "imports": len([_ for _ in source_text.splitlines() if _.strip().startswith("import ") or _.strip().startswith("from ")]),
    }


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "blend_file" not in request.files:
        flash("No file part in the request.")
        return redirect(url_for("index"))

    file = request.files["blend_file"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    ext = Path(file.filename).suffix.lower()

    try:
        file.stream.seek(0)
        if ext == ".blend":
            metadata = parse_blend_header(file.stream)
            file_type = "blend"
            context = {"metadata": metadata}

        elif ext == ".py":
            content = file.stream.read().decode("utf-8", errors="replace")
            analysis = analyze_python_source(content)
            file_type = "python"
            context = {
                "analysis": analysis,
                "preview": content[:2048],
            }

        else:
            raise ValueError("Unsupported file type. Please upload a .blend or .py file.")

        file.stream.seek(0, os.SEEK_END)
        size_bytes = file.stream.tell()

        return render_template(
            "result.html",
            filename=file.filename,
            size=size_bytes,
            file_type=file_type,
            **context,
        )

    except Exception as exc:
        flash(str(exc))
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
