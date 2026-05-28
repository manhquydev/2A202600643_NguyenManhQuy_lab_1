"""
Gradio web UI for the AI Chatbot Lab.
Usage: python web_app.py
Then open: http://localhost:7860
"""

import os
import gradio as gr
import openai
from solution.solution import (
    OPENAI_MODEL,
    OPENAI_MINI_MODEL,
    compare_models,
    batch_compare,
    format_comparison_table,
)


def chat_stream(message: str, history: list, model: str, temperature: float, max_tokens: int):
    """Gradio streaming chat function."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "mock-key")

    messages = []
    for human, assistant in history[-3:]:
        messages.append({"role": "user", "content": human})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})

    partial = ""
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            partial += delta
            yield partial
    except Exception as e:
        yield f"[Lỗi] {e}"


def run_comparison(prompt: str) -> tuple:
    """Return (gpt4o_response, mini_response, metrics_markdown)."""
    if not prompt.strip():
        return "Vui lòng nhập prompt.", "", ""

    try:
        result = compare_models(prompt)
    except Exception as e:
        return f"[Lỗi] {e}", "", ""

    metrics = (
        f"**GPT-4o latency:** {result['gpt4o_latency']:.2f}s  \n"
        f"**Mini latency:** {result['mini_latency']:.2f}s  \n"
        f"**GPT-4o cost estimate:** ${result['gpt4o_cost_estimate']:.6f}  \n"
        f"**Mini ~{16.7:.0f}x rẻ hơn GPT-4o**"
    )
    return result["gpt4o_response"], result["mini_response"], metrics


def run_batch_comparison(prompts_text: str) -> str:
    """Accept newline-separated prompts, return formatted comparison table."""
    prompts = [p.strip() for p in prompts_text.strip().split("\n") if p.strip()]
    if not prompts:
        return "Không có prompt hợp lệ."
    prompts = prompts[:5]  # cap to 5 to avoid rate limits
    results = batch_compare(prompts)
    table = format_comparison_table(results)
    return f"```\n{table}\n```"


def build_app() -> gr.Blocks:
    with gr.Blocks(title="AI Chatbot — Day 1 Lab", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🤖 AI Chatbot Lab\nPowered by OpenAI GPT-4o / GPT-4o-mini")

        with gr.Tabs():
            # --- Tab 1: Chat ---
            with gr.Tab("💬 Chat"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### ⚙️ Cài đặt")
                        model_choice = gr.Dropdown(
                            choices=[OPENAI_MODEL, OPENAI_MINI_MODEL],
                            value=OPENAI_MODEL,
                            label="Model",
                        )
                        temperature = gr.Slider(0.0, 2.0, value=0.7, step=0.1, label="Temperature")
                        max_tokens = gr.Slider(64, 1024, value=256, step=64, label="Max Tokens")
                    with gr.Column(scale=3):
                        gr.ChatInterface(
                            fn=chat_stream,
                            additional_inputs=[model_choice, temperature, max_tokens],
                            title=None,
                            retry_btn=None,
                            undo_btn=None,
                        )

            # --- Tab 2: Model Comparison ---
            with gr.Tab("🔬 So Sánh Models"):
                gr.Markdown("### So sánh GPT-4o vs GPT-4o-mini với cùng một prompt")

                prompt_input = gr.Textbox(
                    label="Prompt",
                    placeholder="Nhập câu hỏi để so sánh...",
                    lines=3,
                )
                compare_btn = gr.Button("⚡ So Sánh", variant="primary")

                with gr.Row():
                    gpt4o_out = gr.Textbox(label="GPT-4o Response", lines=8, interactive=False)
                    mini_out = gr.Textbox(label="GPT-4o-mini Response", lines=8, interactive=False)

                metrics_out = gr.Markdown()

                compare_btn.click(
                    fn=run_comparison,
                    inputs=[prompt_input],
                    outputs=[gpt4o_out, mini_out, metrics_out],
                )

                gr.Markdown("---\n### Batch So Sánh (nhiều prompt, 1 dòng/prompt)")
                batch_input = gr.Textbox(
                    label="Prompts (mỗi dòng 1 prompt, tối đa 5)",
                    placeholder="Giải thích AI là gì?\nViết haiku về Python\nTemperature trong LLM là gì?",
                    lines=5,
                )
                batch_btn = gr.Button("📊 So Sánh Batch")
                batch_out = gr.Textbox(label="Kết quả bảng so sánh", lines=10, interactive=False)
                batch_btn.click(fn=run_batch_comparison, inputs=[batch_input], outputs=[batch_out])

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(server_name="127.0.0.1", server_port=7860, share=False)
