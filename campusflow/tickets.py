
def calculate_priority(urgency, affected_users):
    """Calculate a ticket's priority from urgency and affected users."""

    if urgency not in ("low", "medium", "high"):
        raise ValueError("Urgency must be low, medium, or high.")

    if not isinstance(affected_users, int) or isinstance(affected_users, bool):
        raise ValueError("Affected users must be a whole number.")

    if affected_users < 1:
        raise ValueError("Affected users must be at least 1.")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")


def create_ticket(ticket_id, title, category, urgency, affected_users):
    """Validate the details and create a new helpdesk ticket."""

    if not isinstance(ticket_id, int) or isinstance(ticket_id, bool) or ticket_id < 1:
        raise ValueError("Ticket ID must be a positive integer.")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    if category not in VALID_CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    priority = calculate_priority(urgency, affected_users)

    return {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
