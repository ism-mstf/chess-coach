python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install stockfish
RUN wget -qO /tmp/stockfish.zip https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish_16_x64_avx2.zip \
    && apt-get update && apt-get install -y unzip \
    && unzip /tmp/stockfish.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/stockfish_16_x64_avx2

WORKDIR /app

COPY ./backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY ./backend /app/backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
