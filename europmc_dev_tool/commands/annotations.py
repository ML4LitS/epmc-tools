import click
import json
from ..api.annotations import AnnotationsClient

@click.group()
def annotations():
    """Commands for the Europe PMC Annotations API."""
    pass

@annotations.command('by-id')
@click.argument("article_ids", nargs=-1, required=True)
@click.option("--provider", help="Filter by annotation provider.")
@click.pass_context
def get_by_id(ctx, article_ids, provider):
    """
    Get annotations by article IDs (e.g., PMC:11704132).
    """
    client = AnnotationsClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    data = client.get_by_article_ids(list(article_ids), provider)
    click.echo(json.dumps(data, indent=2))

@annotations.command('by-entity')
@click.argument("entity", required=True)
@click.option("--provider", help="Filter by annotation provider.")
@click.pass_context
def get_by_entity(ctx, entity, provider):
    """
    Find articles that cite a specific entity (e.g., p53).
    """
    client = AnnotationsClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    data = client.get_by_entity(entity, provider)
    click.echo(json.dumps(data, indent=2))

@annotations.command('by-type')
@click.option("--type", "annotation_type", required=True, help="Annotation type (e.g., 'Gene_Proteins', 'Organisms', 'data accession').")
@click.option("--subtype", help="Annotation subtype (e.g., 'database' for data accessions).")
@click.option("--section", help="Article section (e.g., 'Data availability statement').")
@click.option("--provider", help="Filter by annotation provider.")
@click.option("--filter", "filter_val", default=1, type=int, help="Filter annotations (0 or 1).")
@click.option("--page-size", default=4, type=int, help="Number of articles per page (1-8).")
@click.option("--cursor-mark", default="0.0", help="Cursor for pagination.")
@click.pass_context
def get_by_type(ctx, annotation_type, subtype, section, provider, filter_val, page_size, cursor_mark):
    """
    Get annotations of a specific type, with optional filters.
    """
    client = AnnotationsClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    data = client.get_by_section_and_or_type(annotation_type, subtype, section, provider, filter_val, page_size, cursor_mark)
    click.echo(json.dumps(data, indent=2))
