import unittest

from campusflow.validation import (
    validate_ticket_details,
    validate_ticket_id,
)


class TestTicketValidation(unittest.TestCase):

    def test_accepts_valid_ticket_details(self):
        result = validate_ticket_details(
            "Wi-Fi issue", "Network", "high", 15
        )
        self.assertIsNone(result)

    def test_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            validate_ticket_details(
                "   ", "Network", "high", 15
            )

    def test_rejects_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_ticket_details(
                "Wi-Fi issue", "Invalid", "high", 15
            )

    def test_rejects_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_ticket_details(
                "Wi-Fi issue", "Network", "urgent", 15
            )

    def test_rejects_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_details(
                "Wi-Fi issue", "Network", "high", 0
            )

    def test_rejects_boolean_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_details(
                "Wi-Fi issue", "Network", "high", True
            )

    def test_accepts_valid_ticket_id(self):
        result = validate_ticket_id(1)
        self.assertIsNone(result)

    def test_rejects_invalid_ticket_id(self):
        with self.assertRaises(ValueError):
            validate_ticket_id(0)


if __name__ == "__main__":
    unittest.main()