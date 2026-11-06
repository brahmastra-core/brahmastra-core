FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

EXPOSE 9001 9002

CMD ["python3", "-c", "print('Brahmastra Sovereign Node initialized successfully.')"]
