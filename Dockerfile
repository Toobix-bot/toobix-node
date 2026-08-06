FROM python:3.10-slim

LABEL maintainer="Toobix-bot"
LABEL description="Toobix Node 2.0 – Dezentrales Solidaritäts-Netzwerk (Alle für alle!)"

WORKDIR /app

# Keine externen Abhängigkeiten nötig – reines Python stdlib Backend!
# Optional: FastAPI/Uvicorn für Produktions-Deployment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

COPY . /app

ENV HOST=0.0.0.0
ENV PORT=8000
ENV DB_PATH=/data/toobix_node.db

# Persistentes Datenverzeichnis
VOLUME ["/data"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

CMD ["python3", "-m", "app.main"]
