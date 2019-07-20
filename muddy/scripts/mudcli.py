import click
from muddy.constants import MUD_MODEL_DEF

@click.group()
def cli():
    pass

@cli.command()
@click.option('--version', default=1, help=MUD_MODEL_DEF["mud-version"], show_default=True)
@click.option('--mud-url', help=MUD_MODEL_DEF["mud-url"])
@click.option('--cache-validity', default=48, help=MUD_MODEL_DEF["cache-validity"], show_default=True)
@click.option('--is-supported/--is-not-supported', default=True, help=MUD_MODEL_DEF["is-supported"], show_default=True)
def make(version, mud_url, cache_validity, is_supported):
    click.echo('make mud file')