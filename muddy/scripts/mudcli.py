import click
from muddy.constants import MUD_MODEL_DEF
from muddy.models import IPVersion, Direction
from muddy.utils import get_sub_ace_name

@click.group()
def cli():
    pass

@cli.command()
@click.option('--mud-version', '-v', required=True, default=1, help=MUD_MODEL_DEF["mud-version"], show_default=True)
@click.option('--mud-url', '-u', required=True, help=MUD_MODEL_DEF["mud-url"])
@click.option('+supported/-supported', required=True, default=True, help=MUD_MODEL_DEF["is-supported"], show_default=True)
@click.option('--cache-validity', default=48, help=MUD_MODEL_DEF["cache-validity"], show_default=True)
@click.option('--systeminfo', help=MUD_MODEL_DEF["systeminfo"])
@click.option('--documentation', help=MUD_MODEL_DEF["documentation"])
@click.option('--mfg-name', help=MUD_MODEL_DEF["mfg-name"])
@click.option('--model-name', help=MUD_MODEL_DEF["model-name"])
@click.option('--firmware-rev', help=MUD_MODEL_DEF["firmware-rev"])
@click.option('--software-rev', help=MUD_MODEL_DEF["software-rev"])
@click.option('--extensions', help=MUD_MODEL_DEF["extensions"])
@click.option('+ipv4/-ipv4', required=True, help="Does this device speak IPv4?")
@click.option('+ipv6/-ipv6', required=True, help="Does this device speak IPv6?")
@click.option('--acldns', type=(str, str, str, str), help="DNS ACL")
def make(mud_version, mud_url, cache_validity, supported, systeminfo,
        mfg_name, documentation, model_name, firmware_rev, software_rev,
        extensions, ipv4, ipv6, acldns):
    click.echo('make mud file')
    click.echo(acldns)
    click.echo(get_sub_ace_name("test", Direction.FROM_DEVICE))