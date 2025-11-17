🛡️ Sentinel – Next-Generation Framework for Combating AI-Accelerated Misinformation

Sentinel is a next-generation hybrid security framework designed to detect, analyze, and counter AI-generated misinformation across text, images, and web content.
It combines:

Cognitive Linguistic Analysis

Misinformation Pattern Detection

Image Provenance Verification (Genesis Engine)

Source Diversity Mapping (Echo Chamber Radar)

A Real-Time Chrome Extension Shield

A FastAPI-powered backend with ML/NLP models

This creates a full-stack, real-time misinformation defense system operating directly inside the browser.

📌 Overview

As generative AI systems accelerate misinformation, detection systems must evolve beyond traditional NLP.
Sentinel is built for this new era—real-time, privacy-preserving, and multi-modal.

The framework provides:

🔍 Real-time misinformation scanning on web pages

📉 Automatic logical fallacy recognition

⚠️ Emotional manipulation analysis

🖼️ AI vs real image verification (GENESIS system)

📡 Source diversity & bias visualization

🔐 Local-first inference (browser + local API)

🚨 Adaptive risk scoring (green / yellow / red)

🧠 News-bias interpretation using curated lexicons

Built for:
Journalists • Researchers • Policy Analysts • Cybersecurity Teams • Regular Internet Users

✨ Key Features
🧠 1. Cognitive Shield — Text Misinformation Scanner

Real-time detection of manipulative text using a hybrid NLP pipeline:

Emotional manipulation scoring

Logical fallacy pattern recognition

Sentiment & polarity drift detection

Risk scoring: Green / Yellow / Red

Lightweight lexicon + rule-based fallacy engine

Optional HuggingFace sentiment model support

Possible alerts include:

“Emotional Language Detected”

“Potential False Dilemma”

“Possible Straw Man Argument”

“Ad Hominem Indicators”

Runs fully automatically, without user input.

🖼️ 2. Genesis Engine — Image Authenticity Verification

Right-click → “Verify Image (Genesis)”

Backend processes:

Perceptual Hashing (pHash)

SHA-256 integrity hashing

SQLite-based image manifest ledger

Signature & originality checks

(Future) EXIF, CLIP similarity, tampering fingerprinting

Outputs:

✔ Authentic / Likely Original

⚠ Potentially Manipulated

❌ Suspicious / Possibly AI-Generated

🌐 3. Echo Chamber Radar — Source Diversity Visualization

Tracks sources visited by the user and maps:

Political bias (left / right / center)

News diversity and echo chambers

Polarization patterns

Consumption imbalance

Rendered using D3.js charts inside the popup.

Uses the custom bias dataset (bias.json).

🧩 4. Chrome Extension (Frontend Intelligence Layer)
Core Components

content.js → Extracts webpage text & sends to backend

background.js → Manages analysis requests, caching, Genesis checks

popup.html → UI shell for reporting

popup.js → Renders alerts, risk badges, charts

Capabilities

Real-time DOM monitoring (MutationObserver)

Smart 5-minute hash caching

MV3-compliant service worker architecture

Robust notification handling

Zero external requests (local-first security)

⚙️ 5. FastAPI Backend (Analysis Engine)

Backend logic is defined in main.py and performs:

Text Verification

Emotional lexicon detection

Logical fallacy pattern recognition

Sentiment inference (optional HF models)

Category extraction (Emotional, Fallacies, Manipulation)

Risk scoring logic

Image Verification (Genesis)

Image download

Hash-based authenticity verification

Database manifesting

Suspicion-level classification

Storage

SQLite ledger for image fingerprints

Runs locally → no external data exposure.

🧠 How Sentinel Works — System Pipeline
1. Real-Time Text Collection

content.js extracts text continuously from webpage DOM.

2. Backchannel Processing (background.js)

Handles:

Cache check via deterministic hashing

API forwarding to /verify

Storage of structured results

Notification dispatch

3. ML/NLP + Rule Engine (FastAPI)

Processes text through:

Emotional lexicon scan

Regex-based fallacy scanning

Optional HuggingFace sentiment model

Combined risk inference

4. Visual Feedback (popup.js)

User sees:

Status badge (Green/Yellow/Red)

Detailed manipulation/fallacy alerts

Source diversity charts

Genesis verification results

5. Image Verification (Genesis Engine)

Via right-click context menu → backend performs:

pHash similarity

SHA-256 fingerprint validation

Suspicion-level flagging

📊 Risk Classification Model
Status	Meaning
🟢 Green	No manipulative or fallacious indicators detected
🟡 Yellow	Emotional / sensational language present
🔴 Red	Strong fallacy or manipulation indicators

Risk scoring is adaptive and explainable.

📦 Installation Guide
Chrome Extension

Go to: chrome://extensions

Enable Developer Mode

Click Load unpacked

Select the Sentinel project folder

Backend Setup
pip install -r requirements.txt
uvicorn main:app --reload --port 8000


Runs at:
➡ http://127.0.0.1:8000

🧪 Example API Usage
Text Verification

Request

POST /verify
{
  "text": "This shocking news proves everything is corrupt!"
}


Response

{
  "status": "red",
  "categories": ["Emotional Language", "Ad Hominem"],
  "alerts": [...]
}

🔬 Technical Deep Dive
NLP Modules

Regex-based fallacy detection

Emotion lexicon scanning

Sentiment inference (HuggingFace optional)

Image Verification

Perceptual hashing (pHash)

SHA-256 fingerprinting

SQLite manifest ledger

Architecture Paradigm

Chrome Manifest V3

MV3 service worker (background.js)

FastAPI for analysis endpoints

Local-first privacy model

Event-driven communication (message passing & storage events)

🔮 Future Enhancements

CLIP-based multimodal forgery detection

LLM-powered misinformation classifier

Network-level disinformation pattern recognition

Crowdsourced misinformation fingerprinting

Blockchain-anchored content manifests

Multi-language fallacy engine

Real-time misinformation radar for social media

Browser-level “Trust Score” for each domain
