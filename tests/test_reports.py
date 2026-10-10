import unittest

from campusflow.reports import generate_ticket_report


class TestTicketReports(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {"id": 1, "priority": "critical", "status": "open"},
            {"id": 2, "priority": "high", "status": "in_progress"},
            {"id": 3, "priority": "low", "status": "resolved"},
        ]

    def test_counts_total_tickets(self):
        report = generate_ticket_report(self.tickets)

        self.assertEqual(report["total"], 3)

    def test_counts_tickets_by_status(self):
        report = generate_ticket_report(self.tickets)

        self.assertEqual(
            report["by_status"],
            {
                "open": 1,
                "in_progress": 1,
                "resolved": 1,
            },
        )

    def test_counts_tickets_by_priority(self):
        report = generate_ticket_report(self.tickets)

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 1,
                "medium": 0,
                "low": 1,
            },
        )

    def test_handles_empty_ticket_list(self):
        report = generate_ticket_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(
            report["by_status"],
            {"open": 0, "in_progress": 0, "resolved": 0},
        )

    def test_rejects_non_list_input(self):
        with self.assertRaises(ValueError):
            generate_ticket_report("invalid")

    def test_rejects_invalid_status(self):
        tickets = [
            {"id": 1, "priority": "high", "status": "waiting"}
        ]

        with self.assertRaises(ValueError):
            generate_ticket_report(tickets)

    def test_rejects_invalid_priority(self):
        tickets = [
            {"id": 1, "priority": "urgent", "status": "open"}
        ]

        with self.assertRaises(ValueError):
            generate_ticket_report(tickets)


if __name__ == "__main__":
    unittest.main()