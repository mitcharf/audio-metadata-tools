import typer

app = typer.Typer(help="Audio Library Tooling Ecosystem")

@app.command()
def version():
    typer.echo("Audio Library Tools - Development Build")

def run():
    app()

if __name__ == "__main__":
    run()
