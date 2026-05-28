"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
import sys
import openai
from typing import Any, Callable

# Bind this module to the parent package if loaded dynamically in tests.
# This prevents "AttributeError: module 'day1' has no attribute 'solution'" under pytest.
if __name__ in sys.modules:
    parts = __name__.split('.')
    if len(parts) > 1:
        parent_name = parts[0]
        if parent_name in sys.modules:
            setattr(sys.modules[parent_name], parts[1], sys.modules[__name__])

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_API_KEY") or "mock-key"
    client = openai.OpenAI(api_key=api_key)
    
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start_time
    if latency <= 0.0:
        latency = 0.0001
    response_text = response.choices[0].message.content or ""
    return response_text, latency



# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.

    Args:
        prompt:      The user message to send.
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        Reuse call_openai() by passing model=OPENAI_MINI_MODEL.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys:
            - "gpt4o_response":      str
            - "mini_response":       str
            - "gpt4o_latency":       float
            - "mini_latency":        float
            - "gpt4o_cost_estimate": float  (estimated USD for the response)

    Hint:
        Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
        (0.75 words ≈ 1 token is a rough approximation)
    """
    gpt4o_res, gpt4o_lat = call_openai(prompt, model=OPENAI_MODEL)
    mini_res, mini_lat = call_openai_mini(prompt)
    
    # Calculate word count for GPT-4o response
    word_count = len(gpt4o_res.split())
    # Estimate tokens
    estimated_tokens = word_count / 0.75
    # Calculate cost estimate using COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    cost_estimate = (estimated_tokens / 1000.0) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    
    return {
        "gpt4o_response": gpt4o_res,
        "mini_response": mini_res,
        "gpt4o_latency": gpt4o_lat,
        "mini_latency": mini_lat,
        "gpt4o_cost_estimate": cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.

    Behaviour:
        - Streams tokens from OpenAI as they arrive (print each chunk).
        - Maintains the last 3 conversation turns in history.
        - Typing 'quit' or 'exit' ends the loop.

    Hints:
        - Keep a list `history` of {"role": ..., "content": ...} dicts.
        - Use stream=True in client.chat.completions.create() and iterate:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - After each turn, append the assistant reply to history.
        - Trim history to the last 3 turns: history = history[-3:]
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_API_KEY") or "mock-key"
    client = openai.OpenAI(api_key=api_key)
    
    history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break
            
        if user_input.lower() in ["quit", "exit"]:
            break
            
        if not user_input:
            continue
            
        # Append user message
        history.append({"role": "user", "content": user_input})
        
        # Call API
        try:
            print("Assistant: ", end="", flush=True)
            stream = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=history,
                stream=True,
            )
            
            assistant_response = ""
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    assistant_response += delta
            print() # new line
            
            # Append assistant message
            history.append({"role": "assistant", "content": assistant_response})
            
            # Trim history to the last 3 turns
            # We follow the hint exactly: history = history[-3:]
            history = history[-3:]
            
        except Exception as e:
            print(f"\nError: {e}")


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).

    Args:
        fn:          Zero-argument callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay:  Initial delay in seconds before the first retry.

    Returns:
        The return value of fn() on success.

    Raises:
        The last exception raised by fn() after all retries are exhausted.
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt >= max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.

    Args:
        prompts: List of prompt strings.

    Returns:
        List of dicts, each being the compare_models result with an extra
        key "prompt" containing the original prompt string.
    """
    results = []
    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.

    Args:
        results: List of dicts as returned by batch_compare.

    Returns:
        A formatted string table with columns:
        Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency

    Hint:
        Truncate long text to 40 characters for readability.
    """
    def truncate(text: str, max_len: int = 40) -> str:
        text_str = str(text).replace('\n', ' ')
        if len(text_str) > max_len:
            return text_str[:max_len-3] + "..."
        return text_str

    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    
    # Calculate column widths based on headers and results
    widths = [len(h) for h in headers]
    
    rows_data = []
    for r in results:
        prompt = truncate(r.get("prompt", ""))
        gpt4o_res = truncate(r.get("gpt4o_response", ""))
        mini_res = truncate(r.get("mini_response", ""))
        gpt4o_lat = f"{r.get('gpt4o_latency', 0.0):.3f}s"
        mini_lat = f"{r.get('mini_latency', 0.0):.3f}s"
        
        row = [prompt, gpt4o_res, mini_res, gpt4o_lat, mini_lat]
        rows_data.append(row)
        for i in range(len(row)):
            widths[i] = max(widths[i], len(row[i]))
            
    # Format the table
    header_str = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
    
    table_lines = [header_str, separator]
    for row in rows_data:
        row_str = " | ".join(row[i].ljust(widths[i]) for i in range(len(row)))
        table_lines.append(row_str)
        
    return "\n".join(table_lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
