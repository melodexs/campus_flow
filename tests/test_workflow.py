import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_ticket_status


class TestTicketAssignment(unittest.TestCase):

    def setUp(self):
        self.ticket = create_ticket(
            1, "Wi-Fi problem", "Network", "high", 5
        )

    def test_assigns_ticket_to_staff_member(self):
        assign_ticket(self.ticket, "Ada")

        self.assertEqual(self.ticket["assigned_to"], "Ada")

    def test_strips_spaces_from_staff_name(self):
        assign_ticket(self.ticket, "  Ada  ")

        self.assertEqual(self.ticket["assigned_to"], "Ada")

    def test_rejects_empty_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "   ")

    def test_cannot_assign_resolved_ticket(self):
        self.ticket["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "Ada")


class TestTicketWorkflow(unittest.TestCase):

    def setUp(self):
        self.ticket = create_ticket(
            1, "Wi-Fi problem", "Network", "high", 5
        )

    def test_ticket_starts_open(self):
        self.assertEqual(self.ticket["status"], "open")

    def test_cannot_start_unassigned_ticket(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "in_progress")

    def test_assigned_ticket_can_start_work(self):
        assign_ticket(self.ticket, "Ada")

        update_ticket_status(self.ticket, "in_progress")

        self.assertEqual(self.ticket["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.ticket, "Ada")
        update_ticket_status(self.ticket, "in_progress")
        update_ticket_status(self.ticket, "resolved")

        self.assertEqual(self.ticket["status"], "resolved")

    def test_cannot_resolve_ticket_directly_from_open(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.ticket, "Ada")
        update_ticket_status(self.ticket, "in_progress")
        update_ticket_status(self.ticket, "resolved")

        update_ticket_status(self.ticket, "open")

        self.assertEqual(self.ticket["status"], "open")

    def test_rejects_invalid_status(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "pending")


if __name__ == "__main__":
    unittest.main()

