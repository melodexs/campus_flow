VALID_STATUSES = ("open", "in_progress", "resolved")


def assign_ticket(ticket, staff_member):
    """Assign a ticket to a staff member."""

    if not isinstance(ticket, dict):
        raise ValueError("Ticket must be a dictionary.")

    if ticket.get("status") == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")

    if not isinstance(staff_member, str) or not staff_member.strip():
        raise ValueError("Staff member name cannot be empty.")

    ticket["assigned_to"] = staff_member.strip()
    return ticket


def update_ticket_status(ticket, new_status):
    """Update a ticket's status while enforcing workflow rules."""

    if not isinstance(ticket, dict):
        raise ValueError("Ticket must be a dictionary.")

    if new_status not in VALID_STATUSES:
        raise ValueError(
            "Status must be open, in_progress, or resolved."
        )

    current_status = ticket.get("status")

    if current_status not in VALID_STATUSES:
        raise ValueError("Ticket has an invalid current status.")

    if current_status == "resolved" and new_status != "open":
        raise ValueError("Reopen the ticket before changing its status.")

    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Assign the ticket before starting work.")

    if current_status == "open" and new_status == "resolved":
        raise ValueError(
            "A ticket must be in progress before it can be resolved."
        )

    ticket["status"] = new_status
    return ticket

 