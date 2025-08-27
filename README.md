# Unipark → ChatGPT API Integration

A lightweight demo showing how to integrate a Unipark survey (or any web form) with the **ChatGPT API**. This project includes:

- `backend.py` – simple Python backend that forwards prompts to ChatGPT and returns responses.
- `llm.html` – minimal frontend which lets users send inputs and view AI responses.

**Perfect for prototyping** interactive assistants embedded in surveys—for summarizing answers, offering suggestions, or guiding users through questions!

---

## Table of Contents

1. [Quick Start](#quick-start)  
   - [Clone](#clone)  
   - [Install Dependencies](#install-dependencies)  
   - [Configure Environment](#configure-environment)  
   - [Run Backend](#run-backend)  
   - [Use Frontend](#use-frontend)  
2. [Project Structure](#project-structure)  
3. [How It Works](#how-it-works)  
   - Frontend (`llm.html`)  
   - Backend (`backend.py`)  
4. [Configuration](#configuration)  
   - Setting up `.env`  
   - CORS handling  
5. [Embedding in Unipark](#embedding-in-unipark)  
6. [Development & Deployment](#development--deployment)  
7. [Security & Privacy](#security--privacy)  
8. [Roadmap](#roadmap)  
9. [License](#license)

---

## 1. Quick Start

### Clone
```bash
git clone https://github.com/GerhardK90/unipark-llm-integration.git
cd unipark-llm-integration
```

### Install Dependencies  
This project uses **Flask** as the backend.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors python-dotenv requests openai
```

### Configure Environment  
Create a `.env` file in the repo root:

```ini
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4      # or gpt-3.5-turbo
HOST=127.0.0.1
PORT=8000
```

### Run Backend
```bash
python backend.py
```

### Use Frontend  
Open `llm.html` in your browser or serve it locally:

```bash
python -m http.server 8080
```

Ensure the fetch URL in `llm.html` points to `http://127.0.0.1:8000/api/chat`.

---

## 2. Project Structure
```
unipark-llm-integration/
├── backend.py      # Python backend using Flask + OpenAI
├── llm.html        # Simple HTML/JS frontend
├── .env            # Local environment variables
└── README.md
```

---

## 3. How It Works

### Frontend (`llm.html`)
- Displays a textarea and "Submit" button.
- Sends `{ prompt: "...", system: "...", temperature: 0.7 }` via `fetch()` to the backend endpoint (`/api/chat`).
- Shows the AI’s reply directly on the page.

### Backend (`backend.py`)
- Exposes `POST /api/chat`
- Receives JSON `{ prompt, system?, temperature? }`
- Forwards to OpenAI’s Chat API (`/v1/chat/completions`)
- Returns JSON `{ response: "...", usage: {...} }`

---

## 4. Configuration

### Example `backend.py`
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    system = data.get("system", "")
    temp = data.get("temperature", 0.7)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=float(temp)
    )

    reply = resp.choices[0].message.content
    usage = resp.usage

    return jsonify({
        "response": reply,
        "usage": usage
    })

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))
```

### CORS
- `flask-cors` is included and allows all origins (`*`) by default.
- For production, restrict to your Unipark survey domain.

---

## 5. Embedding in Unipark

Host `llm.html` and embed via iFrame in Unipark:

```html
<iframe
  src="https://your-domain.example/llm.html"
  width="100%"
  height="480"
  style="border: none;"
  title="ChatGPT Assistant">
</iframe>
```

**Tips**
- Host frontend and backend under the same domain to avoid CORS.
- Keep prompts short.
- Implement a timeout to ensure a smooth user experience.

---

## 6. Development & Deployment

### Development
- `.env` holds secrets (not committed).
- Add `requirements.txt`:

```txt
flask
flask-cors
python-dotenv
requests
openai
```

- Optionally create a `Makefile`:
```makefile
run:
    python backend.py
```

### Deployment
- **Dockerfile** example:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=8000 HOST=0.0.0.0
CMD ["python", "backend.py"]
```

- Use a reverse proxy to secure and expose only API routes; serve `llm.html` statically.
- Inject environment vars at runtime (no secrets baked into image).

---

## 7. Security & Privacy
- Don’t log full prompts—avoid exposing PII.
- Use HTTPS in production.
- Add an auth token if this endpoint is publicly accessible.
- Review OpenAI’s data usage policy.

---

## 8. Roadmap
- [ ] Streaming token-by-token responses to the frontend  
- [ ] Prompt templates (e.g., assistant persona or instructions)  
- [ ] User input moderation and safety filters  
- [ ] Caching common responses for latency/cost savings  
- [ ] CI workflows (linting, unit testing)

---

## 9. License
CC BY, check out the LICENSE File



