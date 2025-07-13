import click
import json
from ..api.grants import GrantsClient

@click.group()
def grants():
    """Commands for the Europe PMC Grants API."""
    pass

@grants.command()
@click.argument("query")
@click.option("--page", default=1)
@click.option("--page-size", default=25)
@click.pass_context
def search(ctx, query, page, page_size):
    """Search grants by query."""
    client = GrantsClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    data = client.search(query, page, page_size)
    click.echo(json.dumps(data, indent=2))
