import typer

from library_cli.lock_commands import app as lock_app

app = typer.Typer(help="Audio Library Tooling Ecosystem")

# Register lock commands
app.add_typer(lock_app, name="lock")

@app.command()
def version() -> None:
    typer.echo("Audio Library Tools - Development Build")

def run() -> None:
    app()

if __name__ == "__main__":
    run()
