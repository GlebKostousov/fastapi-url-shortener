from typing import Annotated

import typer
from rich import print
from rich.console import Console
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens

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
) -> None:
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


@app.command(name="list")
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


@app.command(name="rm")
def delete(
    token_to_delete: Annotated[
        str, typer.Argument(help="Token needed to delete from DB")
    ],
) -> None:
    """
    Remove the token from the database.
    """
    if redis_tokens.token_exists(token_to_delete):
        redis_tokens.delete_token(token_to_delete)
        print(f"[green]Token  {token_to_delete} removed[/green]")
        return

    print(f"[red]Token: {token_to_delete} not found.[/red]")


@app.command()
def add(
    token_to_add: Annotated[str, typer.Argument(help="Token needed to add in db")],
) -> None:
    """
    Add a new token.
    """
    if not redis_tokens.token_exists(token_to_add):
        redis_tokens.add_token(token_to_add)
        print("[green]Token %s added[/green]", token_to_add)
        return

    print("[red]Token %s already exists[/red]", token_to_add)


@app.command()
def create() -> None:
    """
    Create and add a new token.
    """
    redis_tokens.generate_and_save_token()
    print("[green]Token created[/green]")
