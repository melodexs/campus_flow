PRIORITIES = ("critical", "high", "medium", "low")
STATUSES = ("open", "in_progress", "resolved")
CATEGORIES = ("Network", "Hardware", "Software", "Other")


def calculate_resolution_percentage(resolved, total):
    """Return resolved / total * 100, rounded to one decimal place.

    An empty dataset (total of 0) reports 0.0 instead of dividing by zero.
    """
    if total <= 0:
        return 0.0

    return round(resolved / total * 100, 1)


def generate_ticket_report(tickets):
    """Generate a summary of tickets by status, priority and category.

    Every ticket is counted once, by its CURRENT status, so reopened tickets
    are never double-counted. The report also includes the unresolved count
    (open + in_progress), the resolved count and the resolution percentage.
    Read-only: the tickets are never modified.
    """

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
        "by_category": {category: 0 for category in CATEGORIES},
    }

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        status = ticket.get("status")
        priority = ticket.get("priority")
        category = ticket.get("category")

        if status not in STATUSES:
            raise ValueError("Each ticket must have a valid status.")

        if priority not in PRIORITIES:
            raise ValueError("Each ticket must have a valid priority.")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

        # Category is only counted when present, so tickets stored before the
        # category field was validated do not crash the report.
        if category in CATEGORIES:
            report["by_category"][category] += 1

    report["unresolved"] = (
        report["by_status"]["open"] + report["by_status"]["in_progress"]
    )
    report["resolved"] = report["by_status"]["resolved"]
    report["resolution_percentage"] = calculate_resolution_percentage(
        report["resolved"], report["total"]
    )

    return report
