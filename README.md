# File Hash Generator

A Flask web application for the ProStackHub Ethical Hacking internship task. It calculates file hashes and compares hash strings.

## Features
- Upload a file (up to 25 MB) and calculate MD5, SHA-1, and SHA-256.
- Copy each generated hash to the clipboard.
- Compare two hashes; comparison ignores letter case and whitespace.
- Responsive interface with basic upload error handling.

## Requirements
- Python 3.9 or newer
- Flask

## Run locally
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install flask
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## How hashing works
A cryptographic hash function converts file bytes into a fixed-length digest. Even a small change to the file normally produces a different digest. Comparing a newly calculated digest with a trusted reference digest is a common way to check file integrity.

## Forensic considerations
- Preserve the original evidence and work from a forensic copy where appropriate.
- Record the hash algorithm, hash value, date/time, examiner, and evidence identifier.
- MD5 and SHA-1 are provided because the task requests them and older tools may use them. They have known collision weaknesses and should not be used where collision resistance is required. SHA-256 is preferred here.
- A matching hash supports content integrity but does not establish authorship, source, or chain of custody by itself.
- This is a local learning demo, not a hardened evidence-handling platform.
