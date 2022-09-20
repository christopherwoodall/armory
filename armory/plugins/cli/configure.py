import click

@click.group()
def cli():
    """Armory CLI"""


@cli.group()
def run():
    """Run"""

@create.command()
def no_docker():
    click.echo('no docker')

@create.command()
def check():
    click.echo('check')


@cli.group()
def configure():
    """Configure Armory"""

@drop.command()
def use_defaults():
    click.echo('use defaults')

@drop.command()
@click.option('--foo')
def bar(foo):
    click.echo(f"bar called with {foo}")

