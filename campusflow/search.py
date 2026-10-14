"""Read-only ticket search and filtering.

Pure functions: no input(), no print(), and the ticket collection is never
modified. Filters combine with logical AND; an empty filter means
"do not filter by that field".
"""

from campusflow.queue import PRIORITY_ORDER
from campusflow.tickets import VALID_CATEGORIES
from campusflow.workflow import VALID_STATUSES

VALID_PRIORITIES = tuple(PRIORITY_ORDER)


def normalise_choice(raw, valid_options):
    """Return the canonical option matching raw (case-insensitive), or None.

    An empty or whitespace-only raw means "no filter" and returns None.
    Raise ValueError if raw is non-empty but not a valid option.
    """
    if raw is None or not str(raw).strip():
        return None

    wanted = str(raw).strip().casefold()

    for option in valid_options:
        if option.casefold() == wanted:
            return option

    raise ValueError(
        "Must be one of: " + ", ".join(valid_options) + " (or blank for any)."
    )


def search_tickets(tickets, title_text="", category=None, status=None,
                   priority=None):
    """Return tickets matching every supplied filter, in original order.

    title_text: case-insensitive substring of the title (blank = any title).
    category, status, priority: exact canonical values, or None for any.
    The input list and its tickets are never modified.
    """
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    needle = (title_text or "").strip().casefold()

    matches = []

    for ticket in tickets:
        if needle and needle not in str(ticket.get("title", "")).casefold():
            continue

        if category is not None and ticket.get("category") != category:
            continue

        if status is not None and ticket.get("status") != status:
            continue

        if priority is not None and ticket.get("priority") != priority:
            continue

        matches.append(ticket)

    return matches


def sort_by_priority(tickets):
    """Return a new list sorted by priority (critical first), then ticket ID.

    Ticket IDs are compared numerically, so 10 sorts after 2.
    """
    return sorted(
        tickets,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket.get("priority"), len(PRIORITY_ORDER)),
            ticket["id"],
        ),
    )


def format_ticket_row(ticket):
    """Return one display line: ID, title, category, priority, status, assignee."""
    return (
        f"#{ticket['id']} | {ticket['title']} | {ticket['category']} | "
        f"{ticket['priority']} | {ticket['status']} | "
        f"{ticket.get('assigned_to') or 'Unassigned'}"
    )
