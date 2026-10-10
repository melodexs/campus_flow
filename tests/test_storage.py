
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
                "urgency": "high",
                "affected_users": 5,
                "priority": "high",
                "status": "open",
                "assigned_to": None,
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
        self.filepath.write_text("{invalid json", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            load_tickets(self.filepath)

    def test_json_must_contain_a_list(self):
        self.filepath.write_text(
            json.dumps({"id": 1}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "JSON list"):
            load_tickets(self.filepath)


if __name__ == "__main__":
    unittest.main()
