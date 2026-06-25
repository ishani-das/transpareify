import typer
from transpareify.runner import analyze_url

app = typer.Typer()

@app.command()
def analyze(url: str):
    """Analyze a URL across multiple browser envinorments."""
    run_dir = analyze_url(url)  
    print(f"\nRUN SAVED TO: {run_dir}")

if __name__ == "__main__":
    app()

#  python -m transpareify.cli https://boredbutton.com (-m instead of analyze arg when only one command)