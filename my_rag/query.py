import typer
from src.rag import RAGPipeline
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import sys

app = typer.Typer()
console = Console()


@app.command()
def query(
    question: str = typer.Argument(..., help="The question to ask"),
    persist_dir: str = typer.Option("./storage/chroma", help="Vector database storage directory"),
    top_k: int = typer.Option(5, help="Number of chunks to retrieve"),
    threshold: float = typer.Option(0.3, help="Similarity threshold (0.0-1.0)"),
    temperature: float = typer.Option(0.7, help="LLM temperature (0.0-1.0)"),
    max_tokens: int = typer.Option(512, help="Maximum tokens in response"),
    show_sources: bool = typer.Option(True, help="Show source citations")
):
    """
    Query the RAG system with a question.

    Example:
        python query.py "What is Python?"
    """
    console.print(Panel.fit(
        f"[bold cyan]Question:[/bold cyan] {question}",
        border_style="cyan"
    ))

    console.print("\n[dim]Initializing RAG pipeline...[/dim]")
    rag = RAGPipeline(persist_directory=persist_dir)

    db_stats = rag.get_stats()
    if db_stats['document_count'] == 0:
        console.print("[red]Error: No documents indexed. Please run ingest.py first.[/red]")
        sys.exit(1)

    console.print(f"[dim]Database: {db_stats['document_count']} chunks from {len(db_stats['sources'])} sources[/dim]")

    console.print("\n[dim]Retrieving relevant context...[/dim]")

    try:
        result = rag.query(
            query=question,
            top_k=top_k,
            similarity_threshold=threshold,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )

        if "error" in result:
            if result["error"] == "empty_database":
                console.print("[red]No documents indexed.[/red]")
            elif result["error"] == "no_results":
                console.print("[yellow]No relevant information found.[/yellow]")
            console.print(f"\n{result['response']}")
            sys.exit(0)

        console.print("\n" + "=" * 70)
        console.print("[bold green]Response:[/bold green]\n")
        console.print(result['response'])
        console.print("\n" + "=" * 70)

        if show_sources and result.get('context_chunks'):
            console.print("\n[bold cyan]Sources:[/bold cyan]")
            for i, chunk in enumerate(result['context_chunks'], 1):
                console.print(f"\n[bold]{i}. {chunk['source']}[/bold] (chunk {chunk['chunk_index']}, similarity: {chunk['similarity_score']:.3f})")
                console.print(f"[dim]{chunk['text'][:150]}...[/dim]")

        console.print(f"\n[dim]Generation time: {result.get('generation_time', 0):.2f}s | Tokens: {result.get('token_count', 0)}[/dim]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    app()
