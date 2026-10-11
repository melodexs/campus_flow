# CampusFlow

CampusFlow is a Python command-line campus IT helpdesk ticket manager. It lets
you create and review tickets, assign staff, update ticket status, view a
priority-sorted work queue, and generate status and priority reports. Tickets
are stored in `tickets.json` in the current working directory.

## Requirements

- Python 3.8 or later

CampusFlow uses only the Python standard library; no package installation is
needed.

## Run

From the project directory, run:

```sh
python3 main.py
```

Choose an option from the menu. To create a ticket, enter its title, one of the
listed categories, urgency (`low`, `medium`, or `high`), and the number of
affected users. The application calculates priority and saves the ticket. Use
the ticket ID to view a ticket, assign it to a staff member, or change its
status. A ticket must be assigned before it can move to `in_progress`; resolve
it from that status. Reopen a resolved ticket by setting its status to `open`
before making further changes.

## Run tests

Run the automated unit tests from the project directory:

```sh
python3 -m unittest discover -s tests -v
```
