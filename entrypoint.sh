#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &

# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

ollama pull llama3.2
ollama pull deepseek-r1:1.5b
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
