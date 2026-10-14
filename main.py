from campusflow.queue import get_work_queue
from campusflow.reports import generate_ticket_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import calculate_priority, create_ticket, VALID_CATEGORIES
from campusflow.workflow import assign_ticket, update_ticket_status, VALID_STATUSES


DATA_FILE = "tickets.json"
CANCEL_WORD = "back"


class CancelledInput(Exception):
    """Raised when the user types the cancel word at a prompt."""


def ask(prompt, parse):
    """Ask a question until parse() accepts the answer.

    parse is a function that takes the raw input string, raises ValueError
    with a clear message for bad answers, and returns the cleaned value.
    EOFError and KeyboardInterrupt are not caught here; main() handles them.
    """
    while True:
        raw = input(f"{prompt} (or '{CANCEL_WORD}' to cancel): ")

        if raw.strip().lower() == CANCEL_WORD:
            raise CancelledInput()

        try:
            return parse(raw)
        except ValueError as error:
            print(f"Invalid input: {error} Please try again.")


def parse_title(raw):
    """Validate a ticket title."""
    title = raw.strip()

    if not title:
        raise ValueError("Ticket title cannot be empty.")

    return title


def parse_category(raw):
    """Validate a category against the library's accepted categories."""
    category = raw.strip().title()

    if category not in VALID_CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    return category


def parse_urgency(raw):
    """Validate urgency by reusing the library's own rule."""
    urgency = raw.strip().lower()

    calculate_priority(urgency, 1)

    return urgency


def parse_affected_users(raw):
    """Validate the affected-users count by reusing the library's rules."""
    try:
        affected_users = int(raw.strip())
    except ValueError:
        raise ValueError("Affected users must be a whole number.")

    calculate_priority("low", affected_users)

    return affected_users


def parse_staff_name(raw):
    """Validate a staff member's name."""
    staff_member = raw.strip()

    if not staff_member:
        raise ValueError("Staff member name cannot be empty.")

    return staff_member


def parse_status(raw):
    """Validate a status against the library's accepted statuses."""
    status = raw.strip().lower()

    if status not in VALID_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")

    return status


def make_ticket_id_parser(tickets):
    """Build a parser that accepts a whole number matching a real ticket."""
    def parse(raw):
        try:
            ticket_id = int(raw.strip())
        except ValueError:
            raise ValueError("Ticket ID must be a number.")

        if find_ticket(tickets, ticket_id) is None:
            raise ValueError("Ticket not found.")

        return ticket_id

    return parse


def display_ticket(ticket):
    """Display a ticket's details."""
    print(f"\nTicket ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")


def list_tickets(tickets):
    """Display all tickets."""
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in sorted(tickets, key=lambda item: item["id"]):
        display_ticket(ticket)


def view_ticket(tickets):
    """Display one ticket by ID."""
    ticket_id = ask("Ticket ID", make_ticket_id_parser(tickets))
    ticket = find_ticket(tickets, ticket_id)
    display_ticket(ticket)


def create_new_ticket(tickets):
    """Collect ticket details and create a ticket."""
    title = ask("Ticket title", parse_title)
    category = ask("Category", parse_category)
    urgency = ask("Urgency", parse_urgency)
    affected_users = ask("Number of affected users", parse_affected_users)

    try:
        ticket_id = max(
            (ticket["id"] for ticket in tickets),
            default=0,
        ) + 1

        ticket = create_ticket(
            ticket_id,
            title,
            category,
            urgency,
            affected_users,
        )

        tickets.append(ticket)
        save_tickets(tickets, DATA_FILE)

        print(f"\nTicket #{ticket_id} created successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def show_work_queue(tickets):
    """Display unresolved tickets in priority order."""
    try:
        queue = get_work_queue(tickets)

        if not queue:
            print("\nThe work queue is empty.")
            return

        print("\n--- Work Queue ---")

        for ticket in queue:
            print(
                f"#{ticket['id']} | "
                f"{ticket['priority'].upper()} | "
                f"{ticket['status']} | "
                f"{ticket['title']}"
            )

    except ValueError as error:
        print(f"\nError: {error}")


def assign_existing_ticket(tickets):
    """Assign a ticket to a staff member."""
    ticket_id = ask("Ticket ID", make_ticket_id_parser(tickets))
    ticket = find_ticket(tickets, ticket_id)
    staff_member = ask("Staff member's name", parse_staff_name)

    try:
        assign_ticket(ticket, staff_member)
        save_tickets(tickets, DATA_FILE)

        print(f"Ticket #{ticket_id} assigned successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def change_ticket_status(tickets):
    """Update the status of an existing ticket."""
    ticket_id = ask("Ticket ID", make_ticket_id_parser(tickets))
    ticket = find_ticket(tickets, ticket_id)
    new_status = ask("New status", parse_status)

    try:
        update_ticket_status(ticket, new_status)
        save_tickets(tickets, DATA_FILE)

        print(f"Ticket #{ticket_id} status updated successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def find_ticket(tickets, ticket_id):
    """Find a ticket by its numeric ID."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    return None


def show_report(tickets):
    """Display ticket counts by status and priority."""
    try:
        report = generate_ticket_report(tickets)

        print("\n--- Ticket Report ---")
        print(f"Total tickets: {report['total']}")

        print("\nBy status:")
        for status, count in report["by_status"].items():
            print(f"  {status}: {count}")

        print("\nBy priority:")
        for priority, count in report["by_priority"].items():
            print(f"  {priority}: {count}")

    except ValueError as error:
        print(f"\nError: {error}")


def display_menu():
    """Display the main menu."""
    print("\n====== CampusFlow Ticket Manager ======")
    print("1. Create ticket")
    print("2. List all tickets")
    print("3. View ticket by ID")
    print("4. View work queue")
    print("5. Assign ticket")
    print("6. Update ticket status")
    print("7. View reports")
    print("0. Exit")


def main():
    """Run the CampusFlow command-line application."""
    try:
        tickets = load_tickets(DATA_FILE)
    except ValueError as error:
        print(f"Unable to load tickets: {error}")
        return

    print(f"Loaded {len(tickets)} ticket(s).")

    while True:
        try:
            display_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                create_new_ticket(tickets)
            elif choice == "2":
                list_tickets(tickets)
            elif choice == "3":
                view_ticket(tickets)
            elif choice == "4":
                show_work_queue(tickets)
            elif choice == "5":
                assign_existing_ticket(tickets)
            elif choice == "6":
                change_ticket_status(tickets)
            elif choice == "7":
                show_report(tickets)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 0–7.")
        except CancelledInput:
            print("\nCancelled. Returning to the main menu.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
