import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
from http.server import BaseHTTPRequestHandler
import json

SYSTEM_PROMPT = """
You are a snarky assistant that analyzes the contents of a website
and provides a short, humorous summary, ignoring navigation-related text.
Respond in markdown. Do not wrap the markdown in a code block.
"""

def fetch_website_contents(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; WebSummarizer/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:8000]  # Limit to avoid token overflow
    except Exception as e:
        return f"Error fetching website: {str(e)}"


def summarize_url(url: str) -> str:
    content = fetch_website_contents(url)
    if content.startswith("Error"):
        return content

    groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here are the contents of a website. Provide a short summary:\n\n{content}"}
    ]
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
            url = data.get("url", "").strip().strip('"').strip("'")
            if not url:
                self._respond(400, {"error": "url is required"})
                return
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            summary = summarize_url(url)
            self._respond(200, {"summary": summary})

        except Exception as e:
            self._respond(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self._cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # Silence default logging
