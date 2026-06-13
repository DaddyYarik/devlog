import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from datetime import date, timedelta

import click

from . import __version__
from . import formatter
from . import storage


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "-V", "--version")
def cli():
    """devlog — daily developer log & standup generator.

    Jot down what you work on throughout the day, then run
    'devlog standup' to get a ready-to-paste standup report.
    """


@cli.command()
@click.argument("message", nargs=-1, required=True)
@click.option(
    "--tag", "-t",
    multiple=True,
    metavar="TAG",
    help="Add a tag. Use 'blocked' to mark blockers.",
)
def add(message, tag):
    """Add a log entry.

    \b
    Examples:
      devlog add fixed login redirect bug
      devlog add -t backend deployed /users endpoint
      devlog add -t blocked waiting on design review
    """
    entry = storage.add_entry(" ".join(message), list(tag))
    formatter.print_added(entry)


@cli.command()
def today():
    """Show today's log entries."""
    formatter.print_day(date.today(), storage.get_by_date(date.today()), label="Today")


@cli.command()
def yesterday():
    """Show yesterday's log entries."""
    d = date.today() - timedelta(days=1)
    formatter.print_day(d, storage.get_by_date(d), label="Yesterday")


@cli.command()
def standup():
    """Print a ready-to-paste standup report.

    Shows yesterday's done items, today's work, and any entries
    tagged with 'blocked' as blockers.
    """
    formatter.print_standup(
        storage.get_by_date(date.today() - timedelta(days=1)),
        storage.get_by_date(date.today()),
    )


@cli.command()
def week():
    """Show this week's entries (Mon–today)."""
    today = date.today()
    start = today - timedelta(days=today.weekday())
    formatter.print_week(start, today, storage.get_range(start, today))


@cli.command("ls")
@click.option(
    "--days", "-d",
    default=7,
    show_default=True,
    help="How many days back to show.",
)
def list_entries(days):
    """List recent log entries."""
    end = date.today()
    start = end - timedelta(days=days - 1)
    formatter.print_recent(storage.get_range(start, end), days)


@cli.command()
@click.argument("entry_id")
def delete(entry_id):
    """Delete an entry by its ID prefix."""
    if storage.delete_entry(entry_id):
        click.echo(f"Deleted entry {entry_id}.")
    else:
        click.echo(f"No entry found with ID '{entry_id}'.", err=True)
        raise SystemExit(1)
