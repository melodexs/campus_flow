def add_note(ticket, author, message):
    """Add a validated note to an open or in-progress ticket."""

    # Validate the ticket before making any changes.
    if not isinstance(ticket, dict):
        raise ValueError("Ticket must be a dictionary.")

    if ticket.get("status") not in ("open", "in_progress"):
        raise ValueError("Notes can only be added to active tickets.")

    # Validate the author.
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    # Validate and normalize the message.
    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError(
            "Note message must contain between 5 and 300 characters."
        )

    # Validate existing notes before adding another one.
    notes = ticket.get("notes")

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be a list.")

    existing_ids = set()

    for existing_note in notes:
        if not isinstance(existing_note, dict):
            raise ValueError("Each note must be a dictionary.")

        note_id = existing_note.get("note_id")

        if (
            not isinstance(note_id, str)
            or not note_id.startswith("N")
            or not note_id[1:].isdigit()
            or int(note_id[1:]) < 1
        ):
            raise ValueError("Each note must have a valid note ID.")

        if note_id in existing_ids:
            raise ValueError(f"Duplicate note ID found: {note_id}")

        existing_ids.add(note_id)

        existing_author = existing_note.get("author")
        existing_message = existing_note.get("message")

        if not isinstance(existing_author, str) or not existing_author.strip():
            raise ValueError("Each note must have a valid author.")

        if (
            not isinstance(existing_message, str)
            or not 5 <= len(existing_message.strip()) <= 300
        ):
            raise ValueError("Each note must have a valid message.")

    # Generate the next ID only after validation succeeds.
    highest_id = max(
        (int(note_id[1:]) for note_id in existing_ids),
        default=0,
    )
    next_id = highest_id + 1
    new_note_id = f"N{next_id:03d}"

    note = {
        "note_id": new_note_id,
        "author": author.strip(),
        "message": message,
    }

    # This is the first mutation of the ticket.
    notes.append(note)

    return note