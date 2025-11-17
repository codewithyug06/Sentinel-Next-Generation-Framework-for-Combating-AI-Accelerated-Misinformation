# main.py
import os, re, hashlib, json, time, sqlite3
from io import BytesIO
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import imagehash
import requests

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# Hugging Face config (optional)
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
HF_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# Lexicon & fallacy patterns
emotional_words = set("""
shocking outrage scandal disastrous horrific terrifying explosive alarming unbelievable corrupt evil
manipulated disgusting furious hate anger panic crisis
""".split())

fallacy_patterns = {
    "False Dilemma": {
        "pattern": r"\beither\b.*\bor\b",
        "explanation": "This presents a complex issue as if there are only two possible options, ignoring other possibilities."
    },
    "Straw Man": {
        "pattern": r"\bso (you|you're|they're|we're) saying\b",
        "explanation": "This misrepresents an opponent's argument to make it easier to attack."
    },
    "Ad Hominem": {
        "pattern": r"\b(idiot|moron|clown|stupid|dumb|crazy)\b",
        "explanation": "This attacks the person making an argument, rather than addressing the argument itself."
    }
}

class VerifyRequest(BaseModel):
    text: str

def hf_sentiment(text: str):
    if not HF_TOKEN:
        return {"label": "NEUTRAL", "score": 0.5, "note": "HF token missing"}
    try:
        r = requests.post(HF_URL, headers=HF_HEADERS, json={"inputs": text[:4000]}, timeout=12)
        r.raise_for_status()
        out = r.json()
        candidate = out[0][0] if isinstance(out, list) and out and isinstance(out[0], list) else (out[0] if isinstance(out, list) else out)
        if isinstance(candidate, dict) and "label" in candidate:
            return {"label": candidate.get("label", "NEUTRAL"), "score": float(candidate.get("score", 0.5))}
        return {"label": "NEUTRAL", "score": 0.5, "note": "unexpected hf response"}
    except Exception as e:
        return {"label": "NEUTRAL", "score": 0.5, "error": str(e)}

@app.post("/verify")
def verify_text(req: VerifyRequest):
    text = req.text or ""
    lower = text.lower()

    alerts = []
    categories = []

    # 1) Emotion Lexicon Analysis
    found_emotions = sorted({w for w in emotional_words if w in lower})
    if len(found_emotions) > 2:
        categories.append("Emotional Language")
        alerts.append({
            "title": "Emotional Language Detected",
            "content": f"This text uses words like '{', '.join(found_emotions[:3])}' to provoke a strong emotional reaction. Read critically to separate feelings from facts."
        })

    # 2) Logical Fallacy Analysis
    for name, data in fallacy_patterns.items():
        if re.search(data["pattern"], text, re.I):
            categories.append(name)
            alerts.append({
                "title": f"Potential Fallacy: {name}",
                "content": data["explanation"]
            })

    # 3) Determine overall status
    status = "green"
    if "Emotional Language" in categories:
        status = "yellow"
    if any(name in categories for name in fallacy_patterns.keys()):
        status = "red"

    return {
        "status": status,
        "categories": sorted(list(set(categories))),
        "alerts": alerts
    }

# ----- The Genesis and Manifest endpoints are kept for future use but are not the focus -----

DB_PATH = "genesis.db"

def db_init():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS manifests(
          id INTEGER PRIMARY KEY,
          sha256 TEXT UNIQUE, phash TEXT, source TEXT,
          signature TEXT, cid TEXT, created_at INTEGER
        )""")

db_init()

class ImageVerifyRequest(BaseModel):
    url: str

@app.post("/image/verify")
def image_verify(req: ImageVerifyRequest):
    try:
        r = requests.get(req.url, timeout=12)
        r.raise_for_status()
        b = r.content
        sha = hashlib.sha256(b).hexdigest()
        img = Image.open(BytesIO(b)).convert("RGB")
        ph = str(imagehash.phash(img))

        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT source, cid FROM manifests WHERE sha256=?", (sha,))
            row = cur.fetchone()
            if row:
                return {"status": "green", "reason": "Exact hash match in registry", "sha256": sha, "phash": ph, "source": row[0], "cid": row[1]}

            cur.execute("SELECT sha256, phash, source, cid FROM manifests")
            for sha2, ph2, src2, cid2 in cur.fetchall():
                dist = imagehash.hex_to_hash(ph) - imagehash.hex_to_hash(ph2)
                if dist <= 8:
                    return {"status": "yellow", "reason": "Perceptual near-match found (possible edit/resize)", "sha256": sha, "phash": ph}

        return {"status": "red", "reason": "No manifest match", "sha256": sha, "phash": ph}
    except Exception as e:
        return {"status": "error", "error": str(e)}
