"""
Rich TUI chatbot entry point.
Usage: python chatbot_rich.py
"""

import os
import openai
from ui.terminal import console, print_user_message, spinner_context
from solution.solution import OPENAI_MODEL


def run_rich_chatbot() -> None:
    console.rule("[bold blue]AI Chatbot — GPT-4o[/]")
    console.print("[dim]Gõ 'quit' hoặc 'exit' để thoát[/]\n")

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "mock-key")
    history = []

    while True:
        user_input = console.input("[bold cyan]You:[/] ").strip()
        if user_input.lower() in ["quit", "exit"]:
            console.print("[dim]Tạm biệt![/]")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        print_user_message(user_input)

        with spinner_context("Đang suy nghĩ..."):
            stream = client.chat.completions.create(
                model=OPENAI_MODEL, messages=history, stream=True
            )

        console.print("[bold green]Assistant:[/] ", end="")
        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            console.print(delta, end="", markup=False)
            full_response += delta
        console.print()

        history.append({"role": "assistant", "content": full_response})
        history = history[-3:]


if __name__ == "__main__":
    run_rich_chatbot()
