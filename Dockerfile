FROM python:3.10-slim

LABEL maintainer="Toobix-bot"
LABEL description="Toobix Node 2.0 – experimental local solidarity network node"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DB_PATH=/data/toobix_node.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 toobix \
    && mkdir -p /data \
    && chown -R toobix:toobix /data /app

COPY --chown=toobix:toobix . /app

VOLUME ["/data"]
EXPOSE 8000

USER toobix

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health', timeout=3)" || exit 1

# A non-loopback bind requires TOOBIX_API_TOKEN unless
# TOOBIX_ALLOW_INSECURE_REMOTE=1 is explicitly set.
CMD ["python3", "-m", "app.main"]
