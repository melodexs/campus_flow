# CampusFlow

CampusFlow is a command-line campus IT helpdesk ticket manager written in
Python. Campus staff record technical support requests — Wi-Fi outages,
faulty laptops, broken dev environments — as tickets. The application
prioritises them automatically, assigns responsibility, tracks each ticket
from open to resolved, and saves everything to a JSON file so nothing is
lost between runs.

## Requirements

- Python 3.8 or later
- Standard library only — no package installation needed

## Run

From the project directory:

```sh
python3 main.py
```

The application loads existing tickets from `tickets.json` in the current
working directory (a missing file starts a fresh, empty collection) and
offers this menu:

1. Create ticket
2. List all tickets
3. View ticket by ID
4. View work queue
5. Assign ticket
6. Update ticket status
7. View reports
0. Exit

## How tickets work

**Creating:** enter a title, a category (`Network`, `Hardware`, `Software`,
`Other`), an urgency (`low`, `medium`, `high`) and the number of affected
users. The priority is calculated automatically and the ticket gets the next
available integer ID. Each answer is validated before the ticket is created,
and the collection is saved to disk immediately.

**Priority** is calculated from urgency and reach, first match wins:

| Rule | Priority |
|---|---|
| high urgency AND at least 10 affected users | critical |
| high urgency OR at least 10 affected users | high |
| medium urgency OR at least 3 affected users | medium |
| anything else | low |

**Status flow:** `open` → `in_progress` → `resolved`. A ticket must be
assigned to a staff member before it can move to `in_progress`, and it must be
in progress before it can be resolved. A resolved ticket has to be reopened
(status `open`) before anything else can change on it. Workflow-rule
violations print an error and return you to the menu.

**Work queue:** shows unresolved tickets (open and in progress) sorted by
priority, then by ticket ID.

**Reports:** counts of tickets by status and by priority.

## Where data lives

Tickets are saved to `tickets.json` in the working directory. The file is
created and maintained by the application and is not tracked by git. It is
validated on load: malformed files or duplicate/invalid ticket IDs stop the
application with a clear message rather than corrupting data.

## Run tests

```sh
python3 -m unittest discover -s tests -v
```

## Known limitations

- Single-user tool; there is no authentication or multi-user locking.
- Tickets are held in memory and rewritten to disk on each change; it is not
  designed for very large collections.
- The report and queue views validate every ticket on each call, so a
  hand-edited `tickets.json` with an invalid field is rejected rather than
  partially displayed.

## Team and Contributions

- **Partner A — ticket creation, validation and priority engine:**
  Okoh Destiny (melodexs). PR: [PLACEHOLDER — link to Partner A's PR]
- **Partner B — workflow, work queue, reports and storage:**
  Michael Oogwu (dab00gieman). PR: [PLACEHOLDER — link to Partner B's PR]

Each partner keeps their own entries in `docs/ai-learning-log.md`.
