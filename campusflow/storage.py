
import json
from pathlib import Path


def validate_tickets(tickets):
    """Validate that tickets form a list with unique positive integer IDs."""
    if not isinstance(tickets, list):
        raise ValueError("The tickets file must contain a JSON list.")

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        ticket_id = ticket.get("id")

        if (
            not isinstance(ticket_id, int)
            or isinstance(ticket_id, bool)
            or ticket_id < 1
        ):
            raise ValueError("Each ticket must have a positive integer ID.")

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

        seen_ids.add(ticket_id)


def save_tickets(tickets, filename="tickets.json"):
    """Validate and save tickets to a JSON file."""
    validate_tickets(tickets)
    path = Path(filename)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(filename="tickets.json"):
    """Load and validate tickets from a JSON file.

    Return an empty list if the file does not exist.
    Raise a clear error if the JSON is malformed or invalid.
    """
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error

    validate_tickets(tickets)
    return tickets
