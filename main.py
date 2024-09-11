import click
import urllib.parse

from app.SiteManager import SiteManager

site_manager = SiteManager()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-n",
    "--name",
    metavar="SITE_NAME",
    prompt="Enter your site's name",
    help="Enter your site's name",
)
def new(name):
    """Create a new site"""
    site_name = site_manager.create_site(name)
    click.echo(f"Site created: {site_name}.")


@cli.command()
def integrate_site():
    """Defines SSH details for an existing site"""
    sites = site_manager.get_site_names()
    for index, site in enumerate(sites):
        click.echo(f"{index+1}. {site}")

    click.echo("Which site would you like to integrate")
    option = click.prompt("Enter your choice", type=int)

    if option > len(sites) or option < 1:
        click.echo(f"Invalid option {option}. Please try again")
        return

    site = site_manager.get_site(sites[option - 1])

    user = click.prompt("Enter SSH username")
    domain = click.prompt("Enter your domain")
    password = click.prompt("Enter your password")

    site.set_ssh_details(user, domain, password)


@cli.command()
def remove():
    """Remove an existing site"""
    sites = site_manager.get_site_names()
    for index, site in enumerate(sites):
        click.echo(f"{index+1}. {site}")

    click.echo("Which site would you like to remove")
    option = click.prompt("Enter your choice", type=int)

    if option > len(sites) or option < 1:
        click.echo(f"Invalid option {option}. Please try again")
        return

    site = site_manager.get_site(sites[option - 1])
    site.remove()


@cli.command()
def list():
    """List all sites"""
    sites = site_manager.get_site_names()
    for index, site in enumerate(sites):
        click.echo(f"{index+1}. {site}")


@cli.command()
def import_site():
    """Download site from remote server"""
    sites = site_manager.get_site_names()
    for index, site in enumerate(sites):
        click.echo(f"{index+1}. {site}")

    click.echo("Which site details would you like to download")
    option = click.prompt("Enter your choice", type=int)

    site = site_manager.get_site(sites[option - 1])
    site.download()


@cli.command()
def export_site():
    """Upload site from remote server"""
    sites = site_manager.get_site_names()
    for index, site in enumerate(sites):
        click.echo(f"{index+1}. {site}")

    click.echo("Which site details would you like to upload to remote server")
    option = click.prompt("Enter your choice", type=int)

    site = site_manager.get_site(sites[option - 1])
    site.upload()


@click.command()
@click.option(
    "-n", "--name", prompt="Enter your site's name", help="The name of the site."
)
@click.option(
    "-u",
    "--url",
    prompt="Enter your site's URL",
    help="The URL of the site.",
    default="https://example.com",
)
@click.option(
    "-s",
    "--sync",
    type=click.Choice(["y", "n"]),
    default="n",
    prompt="Would you like to synchronousize site to your web server?",
    help="Synchronousize site to your web server.",
)
def generate_site(name, url, sync):
    """Simple program that greets NAME."""
    click.echo(
        f"Your site's name is {name}. Your site's URL is {url}."
        + f" You've chosen synchronization: {sync}."
    )


if __name__ == "__main__":
    cli()


# Provide your site's name
# Enter your site's URL
# Would you like to synchronousize site to your web server? (Y/N)


# Validate URL
def validate_url(ctx, param, value):
    """
    Validate a URL.

    :param ctx: Click context
    :param param: Click parameter
    :param value: URL value
    :return: Validated URL value
    """
    try:
        # Parse the URL
        parsed_url = urllib.parse.urlparse(value)

        # Check if the URL has a scheme (e.g. http, https)
        if not parsed_url.scheme:
            raise click.BadParameter("Invalid URL: missing scheme")

        # Check if the URL has a netloc (e.g. domain, IP address)
        if not parsed_url.netloc:
            raise click.BadParameter("Invalid URL: missing netloc")

        # Check if the URL has a path
        if not parsed_url.path:
            raise click.BadParameter("Invalid URL: missing path")

        # Return the validated URL value
        return value

    except ValueError as e:
        # Raise a Click BadParameter exception if the URL is invalid
        raise click.BadParameter(f"Invalid URL: {e}")
