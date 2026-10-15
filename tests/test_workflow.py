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

    def test_rejects_empty_staff_name_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "   ")

        self.assertEqual(self.ticket, original_ticket)

    def test_cannot_assign_resolved_ticket_without_changing_ticket(self):
        self.ticket["status"] = "resolved"
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "Ada")

        self.assertEqual(self.ticket, original_ticket)

    def test_rejects_non_string_staff_name_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, 123)

        self.assertEqual(self.ticket, original_ticket)

class TestTicketWorkflow(unittest.TestCase):

    def setUp(self):
        self.ticket = create_ticket(
            1, "Wi-Fi problem", "Network", "high", 5
        )

    def test_ticket_starts_open(self):
        self.assertEqual(self.ticket["status"], "open")

    def test_cannot_start_unassigned_ticket_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "in_progress")

        self.assertEqual(self.ticket, original_ticket)

    def test_assigned_ticket_can_start_work(self):
        assign_ticket(self.ticket, "Ada")

        update_ticket_status(self.ticket, "in_progress")

        self.assertEqual(self.ticket["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.ticket, "Ada")
        update_ticket_status(self.ticket, "in_progress")
        update_ticket_status(self.ticket, "resolved")

        self.assertEqual(self.ticket["status"], "resolved")

    def test_cannot_resolve_ticket_directly_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "resolved")

        self.assertEqual(self.ticket, original_ticket)

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.ticket, "Ada")
        update_ticket_status(self.ticket, "in_progress")
        update_ticket_status(self.ticket, "resolved")

        update_ticket_status(self.ticket, "open")

        self.assertEqual(self.ticket["status"], "open")

    def test_rejects_invalid_status_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "pending")

        self.assertEqual(self.ticket, original_ticket)

    def test_rejects_non_string_status_without_changing_ticket(self):
        original_ticket = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, None)

        self.assertEqual(self.ticket, original_ticket)

if __name__ == "__main__":
    unittest.main()
