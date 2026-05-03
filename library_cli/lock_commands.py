from pathlib import Path

import typer

from lib.locks import RWLock
from lib.config import DB_ROOT

app = typer.Typer(help="Lock management commands")

@app.command()
def status() -> None:
    """Show the current lock status."""
    lock = RWLock(DB_ROOT)
    typer.echo(f"read.lock: {'present' if lock.read_lock.exists() else 'absent'}")
    typer.echo(f"write.lock: {'present' if lock.write_lock.exists() else 'absent'}")
    typer.echo(f"writer_waiting.lock: {'present' if lock.writer_waiting.exists() else 'absent'}")

@app.command()
def clear(force: bool = typer.Option(False, "--force", help="Force remove all locks")) -> None:
    """Clear lock files."""
    lock = RWLock(DB_ROOT)
    if not force:
        typer.echo("Use --force to clear locks")
        raise typer.Exit(1)

    lock.force_clear()
    typer.echo("All locks cleared.")
