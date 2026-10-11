import unittest
from unittest.mock import patch

import main


class TestTicketViewing(unittest.TestCase):
    def setUp(self):
        self.ticket = {
            "id": 4,
            "title": "Wi-Fi problem",
            "category": "Network",
            "urgency": "high",
            "affected_users": 5,
            "priority": "high",
            "status": "open",
            "assigned_to": None,
        }

    @patch("builtins.print")
    @patch("builtins.input", return_value="4")
    def test_views_ticket_by_id(self, _input, printed):
        main.view_ticket([self.ticket])

        output = "\n".join(str(call.args[0]) for call in printed.call_args_list)
        self.assertIn("Ticket ID: 4", output)
        self.assertIn("Title: Wi-Fi problem", output)

    @patch("builtins.print")
    @patch("builtins.input", return_value="99")
    def test_reports_missing_ticket(self, _input, printed):
        main.view_ticket([self.ticket])

        printed.assert_called_with("Ticket not found.")

    @patch("builtins.print")
    @patch("builtins.input", return_value="not-a-number")
    def test_reports_invalid_ticket_id(self, _input, printed):
        main.view_ticket([self.ticket])

        printed.assert_called_with("\nError: Ticket ID must be a number.")


class TestCliExit(unittest.TestCase):
    @patch("main.load_tickets", return_value=[])
    @patch("builtins.print")
    @patch("builtins.input", side_effect=EOFError)
    def test_eof_exits_cleanly(self, _input, printed, _load):
        main.main()

        self.assertIn(unittest.mock.call("\nGoodbye!"), printed.call_args_list)

    @patch("main.load_tickets", return_value=[])
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", EOFError])
    def test_eof_during_action_exits_cleanly(self, _input, printed, _load):
        main.main()

        self.assertIn(unittest.mock.call("\nGoodbye!"), printed.call_args_list)


if __name__ == "__main__":
    unittest.main()
