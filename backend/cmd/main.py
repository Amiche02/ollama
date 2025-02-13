"""
CLI entry point for local testing of Ollama Brainstorming Chat.
Now requires user to pick from the dynamically fetched models (no default).
"""

import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))

from config.config import SYSTEM_PROMPT
from services.ollama import async_chat_with_model, fetch_models

try:
    import pyfiglet
except ImportError:
    pyfiglet = None


def display_ascii_logo():
    """Display an ASCII logo for the CLI."""
    if pyfiglet:
        ascii_banner = pyfiglet.figlet_format("HELLO PULSE")
        print(ascii_banner)
    else:
        print("HELLO PULSE")
    print("🚀 Welcome to HELLO PULSE AI Chat")
    print("🧠 Powered by Python + Ollama")
    print("-------------------------------------------------\n")


async def main_async():
    display_ascii_logo()

    # Dynamically fetch models from Ollama
    try:
        models = await fetch_models()
    except ConnectionError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not models:
        print("❌ No models found. Ensure Ollama is running and has models.")
        sys.exit(1)

    print("📌 Models currently available in Ollama:")
    for i, model in enumerate(models):
        print(f"{i+1}: {model}")

    # Let user pick
    choice = input("\nSelect a model by number: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(models):
            raise ValueError
        selected_model = models[idx]
    except ValueError:
        print("❌ Invalid choice.")
        sys.exit(1)

    print(f"\n✅ Model selected: {selected_model}")
    print("\n💬 Brainstorming Chatbot (type 'exit' to quit)")

    # Start conversation
    conversation_history = f"System: {SYSTEM_PROMPT}"

    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() == "exit":
            print("\n👋 Bye!")
            break

        # Add user turn
        conversation_history += f"\nUser: {user_input}"

        # Stream response
        print("\n🧠 AI: ", end="", flush=True)

        chunks_collected = []
        try:
            async for chunk in async_chat_with_model(
                selected_model, conversation_history
            ):
                print(chunk, end="", flush=True)
                chunks_collected.append(chunk)
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            continue

        ai_text = "".join(chunks_collected)
        print()  # newline
        # Add to conversation
        conversation_history += f"\nAI: {ai_text}"


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
