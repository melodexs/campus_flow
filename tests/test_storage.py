import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import save_tickets, load_tickets


class TestTicketStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filepath = Path(self.temp_dir.name) / "tickets.json"

        self.tickets = [
            {
                "id": 1,
                "title": "Wi-Fi problem",
                "category": "Network",
                "urgency": "medium",
                "affected_users": 5,
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            }
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_tickets_creates_json_file(self):
        save_tickets(self.tickets, self.filepath)

        self.assertTrue(self.filepath.exists())

    def test_load_tickets_returns_saved_tickets(self):
        save_tickets(self.tickets, self.filepath)

        loaded = load_tickets(self.filepath)

        self.assertEqual(loaded, self.tickets)

    def test_missing_file_returns_empty_list(self):
        loaded = load_tickets(self.filepath)

        self.assertEqual(loaded, [])

    def test_malformed_json_raises_clear_error(self):
        self.filepath.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            load_tickets(self.filepath)

    def test_json_must_contain_a_list(self):
        self.filepath.write_text(
            json.dumps({"id": 1}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "JSON list"):
            load_tickets(self.filepath)

    def test_saves_and_loads_ticket_notes(self):
        self.tickets[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "Checked the router.",
            }
        ]

        save_tickets(self.tickets, self.filepath)

        loaded = load_tickets(self.filepath)

        self.assertEqual(
            loaded[0]["notes"],
            self.tickets[0]["notes"],
        )

    def test_rejects_duplicate_ticket_ids(self):
        duplicate_tickets = [
            self.tickets[0].copy(),
            self.tickets[0].copy(),
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
            save_tickets(duplicate_tickets, self.filepath)

    def test_invalid_save_does_not_overwrite_existing_file(self):
        save_tickets(self.tickets, self.filepath)
        original_content = self.filepath.read_text(encoding="utf-8")

        invalid_tickets = [
            {
                "id": 2,
                "title": "Invalid ticket",
                "category": "Network",
                "urgency": "medium",
                "affected_users": 5,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            }
        ]

        with self.assertRaises(ValueError):
            save_tickets(invalid_tickets, self.filepath)

        updated_content = self.filepath.read_text(encoding="utf-8")

        self.assertEqual(updated_content, original_content)

    def test_rejects_invalid_note_when_loading(self):
        invalid_tickets = [
            {
                **self.tickets[0],
                "notes": [
                    {
                        "note_id": "N001",
                        "author": "",
                        "message": "Checked the router.",
                    }
                ],
            }
        ]

        self.filepath.write_text(
            json.dumps(invalid_tickets),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "author"):
            load_tickets(self.filepath)

    def test_note_id_continuity_after_reload(self):
        from campusflow.notes import add_note

        self.tickets[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "Initial router check.",
            },
            {
                "note_id": "N003",
                "author": "Chidi",
                "message": "Replacement router ordered.",
            },
        ]

        save_tickets(self.tickets, self.filepath)

        loaded_tickets = load_tickets(self.filepath)
        ticket = loaded_tickets[0]

        note = add_note(
            ticket,
            "Ada",
            "Router replacement completed.",
        )

        self.assertEqual(note["note_id"], "N004")
        self.assertEqual(len(ticket["notes"]), 3)


if __name__ == "__main__":
    unittest.main()