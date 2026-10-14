import unittest

from campusflow.notes import add_note
from campusflow.tickets import create_ticket


class TestTicketNotes(unittest.TestCase):

    def setUp(self):
        self.ticket = create_ticket(
            1, "Wi-Fi problem", "Network", "high", 5
        )

    def test_adds_note_with_correct_fields(self):
        note = add_note(
            self.ticket,
            "Ada",
            "Checked the router.",
        )

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Checked the router.")
        self.assertEqual(len(self.ticket["notes"]), 1)

    def test_strips_author_and_message(self):
        note = add_note(
            self.ticket,
            "  Ada  ",
            "  Checked the router.  ",
        )

        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Checked the router.")

    def test_note_ids_increase(self):
        first = add_note(self.ticket, "Ada", "First note.")
        second = add_note(self.ticket, "Ben", "Second note.")

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_rejects_empty_author_without_changing_ticket(self):
        original_ticket = self.ticket.copy()
        original_notes = self.ticket["notes"].copy()

        with self.assertRaises(ValueError):
            add_note(self.ticket, "   ", "Checked the router.")

        self.assertEqual(self.ticket, original_ticket)
        self.assertEqual(self.ticket["notes"], original_notes)

    def test_rejects_short_message_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Ada", "No")

        self.assertEqual(self.ticket, original_ticket)

    def test_rejects_long_message_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Ada", "x" * 301)

        self.assertEqual(self.ticket, original_ticket)

    def test_rejects_note_on_resolved_ticket(self):
        self.ticket["status"] = "resolved"
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Ada", "Checked the router.")

        self.assertEqual(self.ticket, original_ticket)

    def test_note_id_does_not_duplicate_existing_id(self):
        self.ticket["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "First note.",
            },
            {
                "note_id": "N003",
                "author": "Ben",
                "message": "Third note.",
            },
        ]

        note = add_note(self.ticket, "Chidi", "Fourth note.")

        self.assertEqual(note["note_id"], "N004")

    def test_rejects_duplicate_existing_note_ids_without_changing_ticket(self):
        self.ticket["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "First note.",
            },
            {
                "note_id": "N001",
                "author": "Ben",
                "message": "Another note.",
            },
        ]

        original_ticket = {
            **self.ticket,
            "notes": [note.copy() for note in self.ticket["notes"]],
        }

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Chidi", "A new note.")

        self.assertEqual(self.ticket, original_ticket)

if __name__ == "__main__":
    unittest.main()