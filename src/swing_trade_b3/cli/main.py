from __future__ import annotations

import typer


app = typer.Typer(help="Swing Trade B3 CLI (Typer)")


@app.callback()
def _root() -> None:  # pragma: no cover - placeholder
    """Root command group (subcomandos serão adicionados nos próximos PRs)."""
    return None  # pragma: no cover
