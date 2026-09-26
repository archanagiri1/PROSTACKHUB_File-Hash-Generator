from flask import Flask, render_template, request
import hashlib
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB upload limit

ALGORITHMS = ("md5", "sha1", "sha256")

def calculate_hashes(file_bytes):
    return {name.upper(): hashlib.new(name, file_bytes).hexdigest() for name in ALGORITHMS}

def normalize_hash(value):
    return re.sub(r"\s+", "", value).lower()

@app.route("/", methods=["GET", "POST"])
def index():
    hashes = {}
    filename = None
    error = None
    comparison = None
    first_hash = ""
    second_hash = ""

    if request.method == "POST":
        action = request.form.get("action", "generate")

        if action == "compare":
            first_hash = request.form.get("first_hash", "").strip()
            second_hash = request.form.get("second_hash", "").strip()
            if not first_hash or not second_hash:
                error = "Enter both hash values before comparing."
            else:
                match = normalize_hash(first_hash) == normalize_hash(second_hash)
                comparison = "Match: the hash values are identical." if match else "No match: the hash values are different."
        else:
            uploaded = request.files.get("file")
            if not uploaded or not uploaded.filename:
                error = "Choose a file first."
            else:
                filename = uploaded.filename
                file_bytes = uploaded.read()
                hashes = calculate_hashes(file_bytes)
                if not file_bytes:
                    error = "The selected file is empty. Hashes were still generated for the empty file."

    return render_template(
        "index.html",
        hashes=hashes,
        filename=filename,
        error=error,
        comparison=comparison,
        first_hash=first_hash,
        second_hash=second_hash,
    )

@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html",
        hashes={},
        filename=None,
        error="The file is larger than the 25 MB limit.",
        comparison=None,
        first_hash="",
        second_hash="",
    ), 413

if __name__ == "__main__":
    app.run(debug=True)
