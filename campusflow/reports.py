PRIORITIES = ("critical", "high", "medium", "low")
STATUSES = ("open", "in_progress", "resolved")


def generate_ticket_report(tickets):
    """Generate a summary of tickets by status and priority."""

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
    }

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        status = ticket.get("status")
        priority = ticket.get("priority")

        if status not in STATUSES:
            raise ValueError("Each ticket must have a valid status.")

        if priority not in PRIORITIES:
            raise ValueError("Each ticket must have a valid priority.")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report