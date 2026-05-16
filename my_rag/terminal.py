"""Terminal-based interactive RAG application."""

import sys
from pathlib import Path
from typing import Tuple, List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag import RAGPipeline
from src.session import Session
from src.terminal_ui import TerminalUI


class Config:
    """Manages RAG configuration parameters."""

    def __init__(self):
        self.model = "llama3.1:8b"
        self.top_k = 5
        self.temperature = 0.7
        self.threshold = 0.3
        self.context_window = 5

    def validate_and_set(self, parameter: str, value: str) -> Tuple[bool, str]:
        """Validate and set a configuration parameter. Returns (success, message)."""
        parameter = parameter.lower()

        if parameter == "model":
            self.model = value
            return True, f"Model set to: {value}"
        elif parameter == "top_k":
            try:
                val = int(value)
                if val < 1 or val > 20:
                    return False, "top_k must be between 1 and 20"
                self.top_k = val
                return True, f"top_k set to: {val}"
            except ValueError:
                return False, "top_k must be an integer"
        elif parameter == "temperature":
            try:
                val = float(value)
                if val < 0 or val > 2:
                    return False, "temperature must be between 0 and 2"
                self.temperature = val
                return True, f"temperature set to: {val}"
            except ValueError:
                return False, "temperature must be a number"
        elif parameter == "threshold":
            try:
                val = float(value)
                if val < 0 or val > 1:
                    return False, "threshold must be between 0 and 1"
                self.threshold = val
                return True, f"threshold set to: {val}"
            except ValueError:
                return False, "threshold must be a number"
        elif parameter == "context_window":
            try:
                val = int(value)
                if val < 0:
                    return False, "context_window must be 0 or positive"
                self.context_window = val
                return True, f"context_window set to: {val}"
            except ValueError:
                return False, "context_window must be an integer"
        else:
            return False, f"Unknown parameter: {parameter}. Valid: model, top_k, temperature, threshold, context_window"

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration parameters."""
        return {
            "model": self.model,
            "top_k": self.top_k,
            "temperature": self.temperature,
            "threshold": self.threshold,
            "context_window": self.context_window
        }

    def get(self, parameter: str) -> Optional[Any]:
        """Get a specific configuration parameter."""
        return self.get_all().get(parameter.lower())


def is_command(user_input: str) -> bool:
    """Check if input starts with '/' to identify commands."""
    return user_input.strip().startswith("/")


def parse_command(user_input: str) -> Tuple[str, List[str]]:
    """Extract command name and arguments from input."""
    parts = user_input.strip()[1:].split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args


# Command handlers
def handle_help(ui: TerminalUI, args: List[str]):
    """Handle /help command."""
    if args:
        # Command-specific help
        command = args[0].lower()
        help_text = {
            "help": "Show available commands or detailed help for a specific command.\nUsage: /help [command]",
            "history": "Display conversation history.\nUsage: /history [n] - Show last n conversations",
            "clear": "Clear conversation history.\nUsage: /clear",
            "save": "Save current session to file.\nUsage: /save [filename] - Auto-generates filename if not provided",
            "load": "Load a previous session.\nUsage: /load <filename>",
            "sessions": "List all saved sessions.\nUsage: /sessions",
            "context": "View current conversation context being used for memory.\nUsage: /context",
            "list": "Display all ingested documents.\nUsage: /list",
            "upload": "Upload and ingest documents.\nUsage: /upload <filepath> [filepath2 ...]",
            "config": "View current configuration.\nUsage: /config [parameter]",
            "set": "Change configuration parameter.\nUsage: /set <parameter> <value>",
            "exit": "Exit the application.\nUsage: /exit or /quit",
            "quit": "Exit the application.\nUsage: /exit or /quit"
        }

        if command in help_text:
            ui.console.print(f"[bold cyan]/{command}[/bold cyan]")
            ui.console.print(help_text[command])
            ui.console.print()
        else:
            ui.display_error(f"No help available for: /{command}")
    else:
        # General help
        ui.console.print("[bold cyan]Available Commands:[/bold cyan]\n")
        ui.console.print("  [cyan]/help[/cyan]              - Show this help message")
        ui.console.print("  [cyan]/history[/cyan] [n]       - Show conversation history")
        ui.console.print("  [cyan]/clear[/cyan]             - Clear conversation history")
        ui.console.print("  [cyan]/save[/cyan] [filename]   - Save current session")
        ui.console.print("  [cyan]/load[/cyan] <filename>   - Load a previous session")
        ui.console.print("  [cyan]/sessions[/cyan]          - List all saved sessions")
        ui.console.print("  [cyan]/context[/cyan]           - View current conversation context")
        ui.console.print("  [cyan]/list[/cyan]              - Show ingested documents")
        ui.console.print("  [cyan]/upload[/cyan] <file>     - Upload and ingest documents")
        ui.console.print("  [cyan]/config[/cyan] [param]    - View configuration")
        ui.console.print("  [cyan]/set[/cyan] <param> <val> - Change configuration")
        ui.console.print("  [cyan]/exit[/cyan] or [cyan]/quit[/cyan]    - Exit the application")
        ui.console.print()
        ui.console.print("[dim]Configuration parameters: model, top_k, temperature, threshold, context_window[/dim]")
        ui.console.print()


def handle_history(ui: TerminalUI, session: Session, args: List[str]):
    """Handle /history command."""
    limit = None
    if args:
        try:
            limit = int(args[0])
        except ValueError:
            ui.display_error("Invalid number. Usage: /history [n]")
            return

    history = session.get_formatted_history(limit)

    if not history:
        ui.display_info("No conversation history yet.")
        return

    ui.console.print(f"[bold cyan]Conversation History[/bold cyan] ({len(history)} entries)\n")

    for i, entry in enumerate(history, 1):
        timestamp = entry.get("timestamp", "")
        query = entry.get("query", "")
        response = entry.get("response", "")

        ui.console.print(f"[dim]{timestamp}[/dim]")
        ui.console.print(f"[cyan]You:[/cyan] {query}")
        ui.console.print(f"[green]Assistant:[/green] {response[:200]}{'...' if len(response) > 200 else ''}")
        ui.console.print()


def handle_clear(ui: TerminalUI, session: Session, args: List[str]):
    """Handle /clear command."""
    if not session.saved and len(session.history) > 0:
        ui.console.print("[yellow]Warning:[/yellow] You have unsaved conversation history.")
        confirm = input("Clear anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            ui.display_info("Clear cancelled.")
            return

    session.clear()
    ui.display_success("Conversation history cleared.")


def handle_save(ui: TerminalUI, session: Session, args: List[str]):
    """Handle /save command."""
    if len(session.history) == 0:
        ui.display_info("No conversation to save.")
        return

    filename = args[0] if args else session.generate_filename()

    # Check if file exists
    from pathlib import Path
    filepath = Path("sessions") / f"{filename}.json"
    if filepath.exists():
        confirm = input(f"File '{filename}' already exists. Overwrite? (y/N): ").strip().lower()
        if confirm != 'y':
            ui.display_info("Save cancelled.")
            return

    if session.save_to_file(filename):
        ui.display_success(f"Session saved to: sessions/{filename}.json")
    else:
        ui.display_error("Failed to save session.")


def handle_load(ui: TerminalUI, session: Session, args: List[str]):
    """Handle /load command."""
    if not args:
        ui.display_error("Usage: /load <filename>")
        return

    filename = args[0]

    # Check if current session is unsaved
    if not session.saved and len(session.history) > 0:
        ui.console.print("[yellow]Warning:[/yellow] You have unsaved conversation history.")
        confirm = input("Load anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            ui.display_info("Load cancelled.")
            return

    if session.load_from_file(filename):
        ui.display_success(f"Session loaded: {filename} ({len(session.history)} conversations)")
    else:
        ui.display_error(f"Failed to load session: {filename}")
        # Show available sessions
        sessions = session.list_sessions()
        if sessions:
            ui.console.print("\n[dim]Available sessions:[/dim]")
            for s in sessions[:5]:
                ui.console.print(f"  - {s['filename']}")
            ui.console.print()


def handle_sessions(ui: TerminalUI, session: Session, args: List[str]):
    """Handle /sessions command."""
    sessions = session.list_sessions()

    if not sessions:
        ui.display_info("No saved sessions found.")
        return

    rows = []
    for s in sessions:
        rows.append([
            s["filename"],
            s.get("saved_at", "Unknown")[:19].replace("T", " "),
            str(s.get("conversation_count", 0))
        ])

    ui.display_table("Saved Sessions", ["Filename", "Saved At", "Conversations"], rows)


def handle_context(ui: TerminalUI, session: Session, config, args: List[str]):
    """Handle /context command."""
    context_window = config.context_window

    if context_window == 0:
        ui.display_info("Conversation memory is disabled (context_window = 0).")
        return

    context = session.get_context_window(context_window)

    if not context:
        ui.display_info("No conversation context available yet.")
        return

    ui.console.print(f"[bold cyan]Current Conversation Context[/bold cyan] (last {len(context)} of {context_window} turns)\n")

    for i, turn in enumerate(context, 1):
        query = turn.get("query", "")
        response = turn.get("response", "")
        ui.console.print(f"[dim]Turn {i}:[/dim]")
        ui.console.print(f"[cyan]User:[/cyan] {query}")
        ui.console.print(f"[green]Assistant:[/green] {response[:150]}{'...' if len(response) > 150 else ''}")
        ui.console.print()


def handle_list(ui: TerminalUI, pipeline: RAGPipeline, args: List[str]):
    """Handle /list command."""
    try:
        result = pipeline.vectorstore.collection.get()
        ids = result.get("ids", [])
        metadatas = result.get("metadatas", [])

        if not ids:
            ui.display_info("No documents ingested yet. Use /upload <filepath> to add documents.")
            return

        rows = []
        seen = set()
        for i, (doc_id, metadata) in enumerate(zip(ids, metadatas)):
            source = metadata.get("source", "Unknown")
            if source not in seen:
                seen.add(source)
                rows.append([str(len(seen)), source, metadata.get("ingested_at", "Unknown")[:10]])

        ui.display_table("Ingested Documents", ["#", "Document", "Ingested"], rows)
    except Exception as e:
        ui.display_error(f"Failed to list documents: {str(e)}")


def handle_upload(ui: TerminalUI, pipeline: RAGPipeline, args: List[str]):
    """Handle /upload command."""
    if not args:
        ui.display_error("Usage: /upload <filepath> [filepath2 ...]")
        return

    for filepath in args:
        from pathlib import Path
        path = Path(filepath)

        if not path.exists():
            ui.display_error(f"File not found: {filepath}")
            continue

        try:
            with ui.show_spinner(f"Ingesting {path.name}..."):
                success = pipeline.ingest_file(str(path))

            if success:
                ui.display_success(f"Ingested: {path.name}")
            else:
                ui.display_error(f"Failed to ingest: {path.name}")
        except Exception as e:
            ui.display_error(f"Error ingesting {path.name}: {str(e)}")


def handle_config(ui: TerminalUI, config, args: List[str]):
    """Handle /config command."""
    if args:
        # Show specific parameter
        param = args[0].lower()
        value = config.get(param)
        if value is not None:
            ui.console.print(f"[cyan]{param}:[/cyan] {value}")
            ui.console.print()
        else:
            ui.display_error(f"Unknown parameter: {param}")
    else:
        # Show all configuration
        cfg = config.get_all()
        rows = [[k, str(v)] for k, v in cfg.items()]
        ui.display_table("Current Configuration", ["Parameter", "Value"], rows)


def handle_set(ui: TerminalUI, config, args: List[str]):
    """Handle /set command."""
    if len(args) < 2:
        ui.display_error("Usage: /set <parameter> <value>")
        ui.console.print("[dim]Valid parameters: model, top_k, temperature, threshold[/dim]")
        ui.console.print()
        return

    parameter = args[0]
    value = args[1]

    success, message = config.validate_and_set(parameter, value)
    if success:
        ui.display_success(message)
    else:
        ui.display_error(message)


def handle_exit(ui: TerminalUI, session: Session, args: List[str]) -> bool:
    """Handle /exit and /quit commands. Returns True to exit."""
    if not session.saved and len(session.history) > 0:
        ui.console.print("[yellow]You have unsaved conversation history.[/yellow]")
        confirm = input("Save before exiting? (Y/n): ").strip().lower()
        if confirm != 'n':
            filename = session.generate_filename()
            if session.save_to_file(filename):
                ui.display_success(f"Session saved to: sessions/{filename}.json")

    ui.console.print("\n[cyan]Goodbye![/cyan]\n")
    return True


# Command registry
COMMANDS = {
    "help": handle_help,
    "history": handle_history,
    "clear": handle_clear,
    "save": handle_save,
    "load": handle_load,
    "sessions": handle_sessions,
    "context": handle_context,
    "list": handle_list,
    "upload": handle_upload,
    "config": handle_config,
    "set": handle_set,
    "exit": handle_exit,
    "quit": handle_exit,
}


def main():
    """Main entry point for terminal RAG application."""
    # Initialize components
    ui = TerminalUI()
    session = Session()
    pipeline = RAGPipeline()
    config = Config()

    # Display welcome banner
    ui.display_welcome()

    # Check Ollama availability
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code != 200:
            ui.display_error("Ollama is not running. Please start Ollama with: ollama serve")
    except Exception:
        ui.display_error("Ollama is not running. Please start Ollama with: ollama serve")

    # Check document store status
    try:
        # Check if any documents are ingested
        doc_count = len(pipeline.vectorstore.collection.get()["ids"])
        if doc_count == 0:
            ui.display_info("No documents ingested yet. Use /upload <filepath> to add documents.")
    except Exception:
        ui.display_info("Document store is empty. Use /upload <filepath> to add documents.")

    # Main REPL loop
    try:
        while True:
            try:
                # Display prompt and get input
                prompt_text = ui.display_prompt(config.model)
                user_input = input(prompt_text).strip()

                # Handle empty input
                if not user_input:
                    continue

                # Check if it's a command
                if is_command(user_input):
                    command, args = parse_command(user_input)

                    if command in COMMANDS:
                        # Special handling for exit command
                        if command in ["exit", "quit"]:
                            should_exit = handle_exit(ui, session, args)
                            if should_exit:
                                break
                        else:
                            # Route to appropriate handler
                            handler = COMMANDS[command]
                            if command in ["help"]:
                                handler(ui, args)
                            elif command in ["history", "clear", "save", "load", "sessions"]:
                                handler(ui, session, args)
                            elif command in ["context"]:
                                handler(ui, session, config, args)
                            elif command in ["list", "upload"]:
                                handler(ui, pipeline, args)
                            elif command in ["config", "set"]:
                                handler(ui, config, args)
                    else:
                        ui.display_error(f"Unknown command: /{command}. Type /help for available commands.")
                    continue

                # Process as RAG query
                ui.display_query(user_input)

                # Get conversation context from session
                conversation_context = None
                if config.context_window > 0:
                    conversation_context = session.get_context_window(config.context_window)

                # Query with streaming (apply config and conversation context)
                with ui.show_spinner("Searching documents..."):
                    result = pipeline.query(
                        user_input,
                        stream=True,
                        top_k=config.top_k,
                        temperature=config.temperature,
                        similarity_threshold=config.threshold,
                        conversation_history=conversation_context
                    )

                # Stream response
                if result.get("stream"):
                    response_text = ""
                    for token in result["stream"]:
                        ui.console.print(token, end="")
                        response_text += token
                    ui.console.print()
                    ui.console.print()
                else:
                    response_text = result.get("response", "No response generated.")
                    ui.display_response(response_text)

                # Get sources but don't display them (store for session history only)
                sources = result.get("context_chunks", [])

                # Store in session history
                session.append(user_input, response_text, sources)

            except KeyboardInterrupt:
                # Handle Ctrl+C during input or response
                ui.console.print()
                ui.display_info("Interrupted. Press Ctrl+D or type /exit to quit.")
                continue
            except EOFError:
                # Handle Ctrl+D
                ui.console.print()
                should_exit = handle_exit(ui, session, [])
                if should_exit:
                    break
            except Exception as e:
                ui.display_error(f"An error occurred: {str(e)}")
                continue

    except Exception as e:
        ui.display_error(f"Fatal error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()
