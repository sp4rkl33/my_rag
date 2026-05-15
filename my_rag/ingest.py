import typer
from pathlib import Path
from src.rag import RAGPipeline
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import sys

app = typer.Typer()
console = Console()


@app.command()
def ingest(
    file: str = typer.Option(None, "--file", "-f", help="Path to a single file to ingest"),
    directory: str = typer.Option(None, "--dir", "-d", help="Path to a directory to ingest recursively"),
    persist_dir: str = typer.Option("./storage/chroma", help="Vector database storage directory")
):
    """
    Ingest documents into the RAG system.

    Supports PDF, TXT, and Markdown files.
    """
    if not file and not directory:
        console.print("[red]Error: Please specify either --file or --dir[/red]")
        console.print("\nUsage:")
        console.print("  python ingest.py --file path/to/document.pdf")
        console.print("  python ingest.py --dir path/to/documents/")
        sys.exit(1)

    if file and directory:
        console.print("[red]Error: Please specify only one of --file or --dir[/red]")
        sys.exit(1)

    console.print("[bold cyan]Initializing RAG Pipeline...[/bold cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Loading models...", total=None)
        rag = RAGPipeline(persist_directory=persist_dir)
        progress.update(task, completed=True)

    if file:
        file_path = Path(file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            sys.exit(1)

        console.print(f"\n[bold]Ingesting file:[/bold] {file}")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing...", total=None)
            success = rag.ingest_file(str(file_path))
            progress.update(task, completed=True)

        if success:
            console.print("[green]✓ File ingested successfully[/green]")
        else:
            console.print("[yellow]⚠ File skipped (already exists or failed to parse)[/yellow]")

    elif directory:
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            console.print(f"[red]Error: Directory not found: {directory}[/red]")
            sys.exit(1)

        console.print(f"\n[bold]Ingesting directory:[/bold] {directory}")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing files...", total=None)
            stats = rag.ingest_directory(str(dir_path))
            progress.update(task, completed=True)

        console.print("\n[bold]Ingestion Summary:[/bold]")
        console.print(f"  [green]✓ Success:[/green] {stats['success']} files")
        console.print(f"  [yellow]⊘ Skipped:[/yellow] {stats['skipped']} files")
        console.print(f"  [red]✗ Failed:[/red] {stats['failed']} files")

    db_stats = rag.get_stats()
    console.print(f"\n[bold cyan]Database Stats:[/bold cyan]")
    console.print(f"  Total chunks: {db_stats['document_count']}")
    console.print(f"  Unique sources: {len(db_stats['sources'])}")

    console.print("\n[green]Done! You can now query the documents.[/green]")


if __name__ == "__main__":
    app()
