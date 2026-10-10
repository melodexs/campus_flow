import unittest

from campusflow.queue import get_work_queue


class TestWorkQueue(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {"id": 5, "priority": "low", "status": "open"},
            {"id": 3, "priority": "critical", "status": "open"},
            {"id": 2, "priority": "high", "status": "in_progress"},
            {"id": 1, "priority": "critical", "status": "open"},
            {"id": 4, "priority": "high", "status": "resolved"},
        ]

    def test_sorts_by_priority(self):
        queue = get_work_queue(self.tickets)

        priorities = [ticket["priority"] for ticket in queue]

        self.assertEqual(
            priorities,
            ["critical", "critical", "high", "low"],
        )

    def test_sorts_same_priority_by_ticket_id(self):
        queue = get_work_queue(self.tickets)

        critical_ids = [
            ticket["id"]
            for ticket in queue
            if ticket["priority"] == "critical"
        ]

        self.assertEqual(critical_ids, [1, 3])

    def test_excludes_resolved_tickets(self):
        queue = get_work_queue(self.tickets)

        ticket_ids = [ticket["id"] for ticket in queue]

        self.assertNotIn(4, ticket_ids)

    def test_includes_open_and_in_progress_tickets(self):
        queue = get_work_queue(self.tickets)

        ticket_ids = [ticket["id"] for ticket in queue]

        self.assertEqual(ticket_ids, [1, 3, 2, 5])

    def test_does_not_modify_original_list(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        get_work_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )

    def test_rejects_non_list_input(self):
        with self.assertRaises(ValueError):
            get_work_queue("not a list")

    def test_rejects_invalid_priority(self):
        tickets = [
            {"id": 1, "priority": "urgent", "status": "open"}
        ]

        with self.assertRaises(ValueError):
            get_work_queue(tickets)

    def test_rejects_invalid_ticket_id(self):
        tickets = [
            {"id": 0, "priority": "high", "status": "open"}
        ]

        with self.assertRaises(ValueError):
            get_work_queue(tickets)


if __name__ == "__main__":
    unittest.main()