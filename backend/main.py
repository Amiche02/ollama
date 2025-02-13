"""
Entry point for the Python Ollama Brainstorming Chat CLI.
"""

import sys

from config.config import SYSTEM_PROMPT
from services.ollama import chat_with_model, fetch_models

try:
    import pyfiglet
except ImportError:
    pyfiglet = None


def display_ascii_logo():
    """Display an ASCII logo similar to the Go version's figure.NewColorFigure."""
    if pyfiglet:
        ascii_banner = pyfiglet.figlet_format("HELLO PULSE")
        print(ascii_banner)
    else:
        # Fallback if pyfiglet is not installed
        print("HELLO PULSE")
    print("🚀 Welcome to HELLO PULSE AI Chat")
    print("🧠 Powered by Python and Ollama API")
    print("-------------------------------------------------\n")


def main():
    display_ascii_logo()

    # Fetch the models
    try:
        models = fetch_models()
    except ConnectionError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not models:
        print(
            "❌ Aucun modèle trouvé. Vérifiez qu'Ollama est bien en cours d'exécution."
        )
        sys.exit(1)

    print("📌 Modèles disponibles :")
    for i, model in enumerate(models):
        print(f"{i+1}: {model}")

    # Let user choose a model
    choice = input("\nSélectionnez un modèle : ")
    try:
        choice_idx = int(choice) - 1
        selected_model = models[choice_idx]
    except (ValueError, IndexError):
        print("❌ Choix invalide.")
        sys.exit(1)

    print(f"\n✅ Modèle sélectionné : {selected_model}")
    print("\n💬 Brainstorming Chatbot (Tapez 'exit' pour quitter)")

    # Initialize conversation history
    conversation_history = f"System: {SYSTEM_PROMPT}"

    while True:
        user_input = input("\n👤 Vous : ").strip()

        if user_input.lower() == "exit":
            print("\n👋 À bientôt !")
            break

        # Add user message to conversation
        conversation_history += f"\nUser: {user_input}"

        # Stream AI response
        print("\n🧠 Animateur IA : ", end="", flush=True)

        ai_response_accumulator = []
        for chunk in chat_with_model(selected_model, conversation_history):
            print(chunk, end="", flush=True)
            ai_response_accumulator.append(chunk)

        ai_response_text = "".join(ai_response_accumulator)
        print()  # New line after the streamed response

        # Add AI's full response to conversation history
        conversation_history += f"\nAI: {ai_response_text}"


if __name__ == "__main__":
    main()
