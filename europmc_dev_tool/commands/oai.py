import click
from ..api.oai import OAIClient

@click.group()
def oai():
    """Commands for the Europe PMC OAI-PMH service."""
    pass

@oai.command()
@click.option("--verb", default="ListRecords", help="OAI-PMH verb.")
@click.option("--metadata-prefix", default="oai_dc", help="Metadata prefix.")
@click.option("--from-date", help="Start date for harvesting (YYYY-MM-DD).")
@click.option("--until", help="End date for harvesting (YYYY-MM-DD).")
@click.option("--set-spec", help="Set to harvest.")
@click.pass_context
def harvest(ctx, verb, metadata_prefix, from_date, until, set_spec):
    """Harvest metadata via OAI-PMH."""
    client = OAIClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    xml = client.harvest(verb, metadata_prefix, from_date, until, set_spec)
    click.echo(xml)
