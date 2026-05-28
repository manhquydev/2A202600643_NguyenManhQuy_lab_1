from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

console = Console()


def print_user_message(text: str) -> None:
    console.print(Panel(text, title="[bold cyan]You[/]", border_style="cyan"))


def print_assistant_message(text: str) -> None:
    md = Markdown(text)
    console.print(Panel(md, title="[bold green]Assistant[/]", border_style="green"))


def print_comparison_table(results: list) -> None:
    table = Table(title="Model Comparison", show_lines=True)
    table.add_column("Prompt", style="cyan", max_width=30)
    table.add_column("GPT-4o Response", max_width=40)
    table.add_column("Mini Response", max_width=40)
    table.add_column("GPT-4o Latency", style="yellow", justify="right")
    table.add_column("Mini Latency", style="green", justify="right")
    for r in results:
        table.add_row(
            str(r.get("prompt", ""))[:30],
            str(r.get("gpt4o_response", ""))[:40],
            str(r.get("mini_response", ""))[:40],
            f"{r.get('gpt4o_latency', 0):.2f}s",
            f"{r.get('mini_latency', 0):.2f}s",
        )
    console.print(table)


def spinner_context(message: str):
    return console.status(f"[bold yellow]{message}[/]", spinner="dots")
