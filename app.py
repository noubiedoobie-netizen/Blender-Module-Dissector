import os
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

    try:
        metadata = parse_blend_header(file.stream)
        file.stream.seek(0, os.SEEK_END)
        size_bytes = file.stream.tell()
        return render_template("result.html", filename=file.filename, size=size_bytes, metadata=metadata)
    except Exception as exc:
        flash(str(exc))
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
