import click
from muddy.constants import MUD_MODEL_DEF

@click.group()
def cli():
    pass

@cli.command()
@click.option('--mud-version', '-v', required=True, default=1, help=MUD_MODEL_DEF["mud-version"], show_default=True)
@click.option('--mud-url', '-u', required=True, help=MUD_MODEL_DEF["mud-url"])
@click.option('--is-supported', '-s', required=True, type=click.BOOL, default=True, help=MUD_MODEL_DEF["is-supported"], show_default=True)
@click.option('--cache-validity', default=48, help=MUD_MODEL_DEF["cache-validity"], show_default=True)
@click.option('--systeminfo', help=MUD_MODEL_DEF["systeminfo"])
@click.option('--documentation', help=MUD_MODEL_DEF["documentation"])
@click.option('--mfg-name', help=MUD_MODEL_DEF["mfg-name"])
@click.option('--model-name', help=MUD_MODEL_DEF["model-name"])
@click.option('--firmware-rev', help=MUD_MODEL_DEF["firmware-rev"])
@click.option('--software-rev', help=MUD_MODEL_DEF["software-rev"])
@click.option('--extensions', help=MUD_MODEL_DEF["extensions"])
def make(mud_version, mud_url, cache_validity, is_supported, systeminfo,
        mfg_name, documentation, model_name, firmware_rev, software_rev,
        extensions):
    click.echo('make mud file')