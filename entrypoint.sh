#!/bin/bash

# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

ollama pull llama3.2
ollama pull qwen
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
