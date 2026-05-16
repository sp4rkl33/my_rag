"""Terminal UI utilities for the RAG system using Rich library."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from contextlib import contextmanager
from typing import List, Dict, Any


class TerminalUI:
    """Handles all terminal display formatting using Rich."""

    def __init__(self):
        self.console = Console()

    def display_welcome(self):
        """Display startup banner."""
        welcome_text = """
[bold cyan]RAG Terminal[/bold cyan]
[dim]Interactive command-line interface for RAG queries[/dim]

Type your questions or use slash commands:
  [cyan]/help[/cyan]     - Show available commands
  [cyan]/exit[/cyan]     - Exit the application

Press Ctrl+C to interrupt, Ctrl+D to exit
"""
        panel = Panel(welcome_text, border_style="cyan", padding=(1, 2))
        self.console.print(panel)
        self.console.print()

    def display_prompt(self, model_name: str = "llama3.1:8b") -> str:
        """Display input prompt and return user input."""
        return f"[bold cyan]{model_name}>[/bold cyan] "

    def display_query(self, query: str):
        """Display user query in cyan."""
        self.console.print(f"[cyan]You:[/cyan] {query}")
        self.console.print()

    def display_response(self, response: str):
        """Display assistant response with formatting."""
        md = Markdown(response)
        self.console.print(md)
        self.console.print()

    def display_sources(self, sources: List[Dict[str, Any]]):
        """Display retrieved document sources."""
        if not sources:
            return

        self.console.print("[dim]Sources:[/dim]")
        for i, source in enumerate(sources, 1):
            doc_name = source.get("metadata", {}).get("source", "Unknown")
            score = source.get("score", 0.0)
            self.console.print(f"  [dim]{i}. {doc_name} (relevance: {score:.2f})[/dim]")
        self.console.print()

    def display_error(self, message: str):
        """Display error message in red."""
        self.console.print(f"[bold red]✗ Error:[/bold red] {message}")
        self.console.print()

    def display_success(self, message: str):
        """Display success message in green."""
        self.console.print(f"[bold green]✓[/bold green] {message}")
        self.console.print()

    def display_info(self, message: str):
        """Display informational message in gray."""
        self.console.print(f"[dim]{message}[/dim]")
        self.console.print()

    @contextmanager
    def show_spinner(self, text: str):
        """Context manager for progress indicators."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(text, total=None)
            yield progress

    def stream_response(self, tokens):
        """Display streaming tokens in real-time."""
        for token in tokens:
            self.console.print(token, end="")
        self.console.print()
        self.console.print()

    def display_table(self, title: str, columns: List[str], rows: List[List[str]]):
        """Display formatted table."""
        table = Table(title=title, show_header=True, header_style="bold cyan")

        for col in columns:
            table.add_column(col)

        for row in rows:
            table.add_row(*row)

        self.console.print(table)
        self.console.print()

