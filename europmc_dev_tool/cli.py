import click
from .api.articles import ArticlesClient
from .commands.articles import articles
from .commands.grants import grants
from .commands.annotations import annotations
from .commands.oai import oai
from .commands.local import local



@click.group()
@click.option("--email", help="Contact email for API identification.")
@click.option("--tool", help="Tool name for API identification.")
@click.pass_context
def cli(ctx, email, tool):
    """epmc-cli: Command-line interface for Europe PMC."""
    ctx.ensure_object(dict)
    ctx.obj["email"] = email
    ctx.obj["tool"] = tool
    # The client is now instantiated within each command group
    # to ensure the correct client is used for each API.
    pass

cli.add_command(articles)
cli.add_command(grants)
cli.add_command(annotations)
cli.add_command(oai)
cli.add_command(local)

if __name__ == "__main__":
    cli()
