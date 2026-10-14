VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_URGENCIES = ("low", "medium", "high")
VALID_STATUSES = ("open", "in_progress", "resolved")
VALID_PRIORITIES = ("critical", "high", "medium", "low")


def validate_ticket_details(title, category, urgency, affected_users):
    """Validate the details supplied when creating a ticket."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    if category not in VALID_CATEGORIES:
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    if urgency not in VALID_URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
        or affected_users < 1
    ):
        raise ValueError(
            "Affected users must be a positive whole number."
        )


def validate_ticket_id(ticket_id):
    """Ensure a ticket ID is a positive integer."""

    if (
        not isinstance(ticket_id, int)
        or isinstance(ticket_id, bool)
        or ticket_id < 1
    ):
        raise ValueError("Ticket ID must be a positive integer.")