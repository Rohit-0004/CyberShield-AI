# CyberShield AI

CyberShield AI is an early-stage cyber-safety awareness prototype. It screens suspicious messages and URLs for common warning signs and explains why they may deserve extra caution.

## Current features

- Streamlit web interface
- Rule-based message screening for urgency, credential requests, rewards, payment requests, and click/login pressure
- Basic URL structure checks
- Human-readable warning indicators and safety recommendations
- Does not open, visit, or submit URLs

## Technology

- Python
- Streamlit
- Python standard library (`re`, `urllib.parse`)

## Run locally on Windows

1. Install Python 3.10 or newer and VS Code.
2. Open this project folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push the contents of this folder to a GitHub repository.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create an app, select this repository and the `main` branch.
4. Set the main file path to `app.py`, then deploy.

## Current limitations

- This version is rule-based. It does not yet use Gemini or another AI model and is not an autonomous AI agent.
- Rules can produce false positives and can miss sophisticated scams.
- It does not check domain reputation, DNS records, certificates, or live threat-intelligence feeds.
- A result saying no warning patterns were found does **not** mean content is safe.
- Do not paste private information, credentials, OTPs, or financial details.

## Responsible use

Use this prototype for education and awareness. Independently verify suspicious communications through official channels. Do not use the tool as the sole basis for security decisions.
