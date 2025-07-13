import click
import json
from ..api.articles import ArticlesClient

@click.group()
def articles():
    """Commands for the Europe PMC Articles API."""
    pass

@articles.command()
@click.argument("query")
@click.option("--page", default=1)
@click.option("--page-size", default=25)
@click.option("--core/--lite", default=True)
@click.pass_context
def search(ctx, query, page, page_size, core):
    """Search articles by query."""
    client = ArticlesClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    result_type = "core" if core else "lite"
    data = client.search(query, page, page_size, result_type)
    click.echo(json.dumps(data, indent=2))

@articles.command()
@click.argument("article_id")
@click.option("--core/--lite", default=True)
@click.pass_context
def get(ctx, article_id, core):
    """Get metadata for an article."""
    client = ArticlesClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    result_type = "core" if core else "lite"
    
    # Determine the source from the article_id
    source = "PMC" if "PMC" in article_id.upper() else "MED"
    
    data = client.get_article(source, article_id, result_type=result_type)
    click.echo(json.dumps(data, indent=2))

@articles.command()
@click.argument("source")
@click.argument("article_id")
@click.option("--page", default=1)
@click.option("--page-size", default=25)
@click.pass_context
def references(ctx, source, article_id, page, page_size):
    """Get references for an article."""
    client = ArticlesClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    if source.upper() == "PMC":
        article_id = f"PMC{article_id}"
    data = client.get_references(source, article_id, page, page_size)
    click.echo(json.dumps(data, indent=2))

@articles.command()
@click.argument("article_id")
@click.pass_context
def fulltext(ctx, article_id):
    """Download full-text XML for an open-access article."""
    client = ArticlesClient(email=ctx.obj.get("email"), tool=ctx.obj.get("tool"))
    xml = client.get_fulltext_xml(article_id)
    click.echo(xml)
