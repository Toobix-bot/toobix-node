#!/bin/bash
set -e

# Cleanup database files if present
rm -f node1.db node2.db

# Trap signal to ensure process and db cleanup on exit
trap 'kill $NODE1_PID $NODE2_PID 2>/dev/null || true; rm -f node1.db node2.db' EXIT

echo "=== Starting Toobix Node 1 (Port 8001) and Node 2 (Port 8002) ==="
PORT=8001 DB_PATH=node1.db python3 -m app.main & NODE1_PID=$!
PORT=8002 DB_PATH=node2.db python3 -m app.main & NODE2_PID=$!

echo "=== Polling node health endpoints (up to 10s) ==="
READY=0
for i in $(seq 1 20); do
  NODE1_HEALTH=$(curl -s http://127.0.0.1:8001/api/health || true)
  NODE2_HEALTH=$(curl -s http://127.0.0.1:8002/api/health || true)
  if [[ "$NODE1_HEALTH" == *"ok"* ]] && [[ "$NODE2_HEALTH" == *"ok"* ]]; then
    READY=1
    echo "Both nodes are ready!"
    break
  fi
  sleep 0.5
done

if [ $READY -ne 1 ]; then
  echo "Error: Nodes failed to start in time!"
  exit 1
fi

echo "=== Registering Node 2 as peer on Node 1 ==="
REG_RESPONSE=$(curl -s -X POST http://127.0.0.1:8001/api/peers/register \
  -H "Content-Type: application/json" \
  -d '{"peer_url": "http://127.0.0.1:8002"}')
echo "Register Response: $REG_RESPONSE"

echo "=== Creating test Mangel entry on Node 1 ==="
CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:8001/api/scarcity \
  -H "Content-Type: application/json" \
  -d '{"title": "Warmkleidung Winter", "category": "Kleidung", "description": "Benötige 5 Decken", "location": "Berlin", "contact": "notfall@solidaritaet.de"}')
echo "Create Response: $CREATE_RESPONSE"

echo "=== Waiting for P2P state propagation (2s) ==="
sleep 2

echo "=== Fetching scarcity entries from Node 2 ==="
NODE2_ENTRIES=$(curl -s http://127.0.0.1:8002/api/scarcity)
echo "Node 2 Scarcity Entries: $NODE2_ENTRIES"

if [[ "$NODE2_ENTRIES" != *"Warmkleidung Winter"* ]]; then
  echo "Error: Title 'Warmkleidung Winter' not found in Node 2 response!"
  exit 1
fi
echo "[+] Entry successfully synchronized to Node 2!"

echo "=== Fetching Peer Awareness from Node 1 ==="
AWARENESS_RESPONSE=$(curl -s http://127.0.0.1:8001/api/peers/awareness)
echo "Peer Awareness Output: $AWARENESS_RESPONSE"

if [[ "$AWARENESS_RESPONSE" != *"reputation"* ]] && [[ "$AWARENESS_RESPONSE" != *"praised"* ]] && [[ "$AWARENESS_RESPONSE" != *"scores"* ]]; then
  echo "Error: Reputation output missing in awareness response!"
  exit 1
fi
echo "[+] Peer awareness verified!"

echo "P2P Synchronization successful!"
exit 0
