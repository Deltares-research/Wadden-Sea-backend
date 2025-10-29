"""
CLI commands for Wadden-Sea
"""
import click
from wadden_sea import __version__
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from wadden_sea.api.query import process_query
from wadden_sea.api.types import ENTITY_MAPPING


@click.group()
def cli():
    """Wadden-Sea Command Line Interface"""
    pass


@cli.command()
@click.option('--name', default='World', help='Name to greet')
def hello(name: str):
    """Print hello world message"""
    click.echo(f"Hello {name} from wadden-sea!")


@cli.command()
@click.option('--query', required=True, help='Query to process')
@click.option('--entity', required=True, help='Entity to query (e.g., seal, seagrass)')
def query(query: str, entity: str):
    """Process a RAG query for a specific entity"""
    try:
        # Validate entity
        if entity not in ENTITY_MAPPING:
            available = ', '.join(ENTITY_MAPPING.keys())
            click.echo(f"Error: Unknown entity '{entity}'. Available entities: {available}", err=True)
            return
        
        click.echo(f"Processing query for entity '{entity}': {query}")
        click.echo("...")
        
        # Process query
        result = process_query(query=query, entity=entity)
        
        # Display results
        click.echo("\n" + "="*60)
        click.echo("ANSWER:")
        click.echo("="*60)
        click.echo(result['answer'])
        click.echo("\n" + "="*60)
        click.echo("SOURCES:")
        click.echo("="*60)
        if result['sources']:
            for i, source in enumerate(result['sources'], 1):
                click.echo(f"{i}. {source}")
        else:
            click.echo("No sources found")
        click.echo("="*60)
        
    except Exception as e:
        click.echo(f"Error processing query: {e}", err=True)

@cli.command()
def version():
    """Show version information"""
    click.echo(f"Wadden-Sea CLI {__version__}")


if __name__ == '__main__':
    cli()
