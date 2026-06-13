from collections import defaultdict
from datetime import timedelta, datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console(legacy_windows=False)


def _time(ts):
    try:
        return datetime.fromisoformat(ts).strftime("%H:%M")
    except Exception:
        return "     "


def _tags(tags):
    if not tags:
        return ""
    return "  " + " ".join(f"[cyan]#{t}[/cyan]" for t in tags)


def print_added(entry):
    console.print(
        f"[green]✓[/green]  [dim]{entry['id']}[/dim]  {entry['message']}{_tags(entry['tags'])}"
    )


def _day_content(entries):
    if not entries:
        return "[dim]No entries[/dim]"
    return "\n".join(
        f"  [dim]{_time(e['timestamp'])}[/dim]  {e['message']}{_tags(e['tags'])}  [dim]{e['id']}[/dim]"
        for e in entries
    )


def print_day(d, entries, label=""):
    heading = f"{label} — {d.strftime('%A, %b %d')}" if label else d.strftime("%A, %b %d")
    console.print(Panel(_day_content(entries), title=heading, border_style="blue"))


def print_standup(yesterday_entries, today_entries):
    sections = []

    sections.append("[bold]✅  Done (yesterday)[/bold]")
    if yesterday_entries:
        sections += [f"   • {e['message']}" for e in yesterday_entries]
    else:
        sections.append("   [dim](no entries)[/dim]")

    sections.append("")
    sections.append("[bold]🔨  Doing (today)[/bold]")
    if today_entries:
        sections += [f"   • {e['message']}" for e in today_entries]
    else:
        sections.append("   [dim](no entries yet — add some with: devlog add ...)[/dim]")

    sections.append("")
    sections.append("[bold]🚧  Blockers[/bold]")
    blockers = [e for e in today_entries if "blocked" in e.get("tags", [])]
    if blockers:
        sections += [f"   • {e['message']}" for e in blockers]
    else:
        sections.append("   • None")

    console.print(
        Panel(
            "\n".join(sections),
            title="[bold green]Standup Report[/bold green]",
            border_style="green",
        )
    )


def print_week(start, end, entries):
    by_date = defaultdict(list)
    for e in entries:
        by_date[e["date"]].append(e)

    rows = []
    d = start
    while d <= end:
        day_entries = by_date.get(d.isoformat(), [])
        label = "Today" if d == end else d.strftime("%a")
        day_str = str(d.day)
        if day_entries:
            bullets = "\n".join(f"  • {e['message']}" for e in day_entries)
            rows.append(f"[bold]{label} {day_str}[/bold]\n{bullets}")
        else:
            rows.append(f"[dim]{label} {day_str}[/dim]\n  [dim]—[/dim]")
        d += timedelta(days=1)

    console.print(
        Panel("\n\n".join(rows), title="[bold]This Week[/bold]", border_style="magenta")
    )


def print_recent(entries, days):
    if not entries:
        console.print(f"[dim]No entries in the last {days} day(s).[/dim]")
        return

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    table.add_column("Date", style="dim", width=11)
    table.add_column("Time", style="dim", width=5)
    table.add_column("Message")
    table.add_column("Tags", style="cyan")
    table.add_column("ID", style="dim", width=8)

    for e in entries:
        table.add_row(
            e["date"],
            _time(e["timestamp"]),
            e["message"],
            " ".join(f"#{t}" for t in e.get("tags", [])),
            e["id"],
        )

    console.print(table)
