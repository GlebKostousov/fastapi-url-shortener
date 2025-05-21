from typing import Annotated

from api.api_v1.auth.services import redis_tokens

import typer
from rich import print

app = typer.Typer(
    name="tokens",
    no_args_is_help=True,
    help="Management tokens actions",
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="token to check"),
    ],
):
    """
    Check the token exists.
    """
    print(
        f"[bold]token: {token}[/bold]",
        (
            "[green]exist[/green]"
            if redis_tokens.token_exists(token)
            else "[red]does not exists[/red]"
        ),
    )
