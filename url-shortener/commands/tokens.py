from typing import Annotated

from api.api_v1.auth.services import redis_tokens

import typer
from rich import print
from rich.console import Console
from rich.markdown import Markdown

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


@app.command()
def tokens_list() -> None:
    """
    Print the list of all available tokens.
    """
    base_md_text = "# **List of all available tokens**\n"
    for token in redis_tokens.get_all_tokens():
        line_md_text = f"- token: `{token}`\n"
        base_md_text += line_md_text

    markdown = Markdown(base_md_text)
    console = Console()
    console.print(markdown)
