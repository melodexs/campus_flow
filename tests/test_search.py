import copy
import unittest

from campusflow.search import (
    format_ticket_row,
    normalise_choice,
    search_tickets,
    sort_by_priority,
)


def make_ticket(ticket_id, title, category, priority, status, assigned_to=None):
    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": "high",
        "affected_users": 5,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestSearchTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket(1, "Wifi down in library", "Network", "critical", "open"),
            make_ticket(2, "WIFI slow in lab", "Network", "medium", "resolved"),
            make_ticket(3, "Broken projector", "Hardware", "low", "open"),
            make_ticket(4, "Wifi password reset", "Software", "high", "open"),
        ]

    def ids(self, results):
        return [ticket["id"] for ticket in results]

    def test_title_search_ignores_case(self):
        results = search_tickets(self.tickets, "wIfI")

        self.assertEqual(self.ids(results), [1, 2, 4])

    def test_title_search_matches_substring(self):
        results = search_tickets(self.tickets, "project")

        self.assertEqual(self.ids(results), [3])

    def test_hyphenated_and_plain_spellings_are_different_substrings(self):
        """No fuzzy matching: 'wi-fi' does not match 'wifi'."""
        tickets = [make_ticket(1, "Wi-Fi down", "Network", "high", "open")]

        self.assertEqual(len(search_tickets(tickets, "WI-FI")), 1)
        self.assertEqual(search_tickets(tickets, "wifi"), [])

    def test_combined_filters_use_and(self):
        results = search_tickets(
            self.tickets, "wifi", category="Network", status="open"
        )

        self.assertEqual(self.ids(results), [1])

    def test_all_three_filters_plus_title_must_all_match(self):
        results = search_tickets(
            self.tickets,
            "wifi",
            category="Network",
            status="open",
            priority="critical",
        )

        self.assertEqual(self.ids(results), [1])

        results = search_tickets(
            self.tickets,
            "wifi",
            category="Network",
            status="open",
            priority="low",
        )

        self.assertEqual(results, [])

    def test_empty_filters_mean_no_filtering(self):
        results = search_tickets(self.tickets, "", None, None, None)

        self.assertEqual(self.ids(results), [1, 2, 3, 4])

    def test_status_filter_alone(self):
        results = search_tickets(self.tickets, status="resolved")

        self.assertEqual(self.ids(results), [2])

    def test_search_does_not_modify_tickets(self):
        before = copy.deepcopy(self.tickets)

        search_tickets(self.tickets, "wifi", category="Network", status="open")
        sort_by_priority(self.tickets)

        self.assertEqual(self.tickets, before)

    def test_search_returns_new_list_not_the_original(self):
        results = search_tickets(self.tickets, "")

        self.assertIsNot(results, self.tickets)

    def test_search_rejects_non_list_input(self):
        with self.assertRaises(ValueError):
            search_tickets("not a list", "wifi")


class TestSortAndFormat(unittest.TestCase):
    def test_sort_by_priority_then_numeric_id(self):
        tickets = [
            make_ticket(10, "A", "Other", "high", "open"),
            make_ticket(2, "B", "Other", "high", "open"),
            make_ticket(7, "C", "Other", "critical", "open"),
            make_ticket(1, "D", "Other", "low", "open"),
        ]

        ordered = [ticket["id"] for ticket in sort_by_priority(tickets)]

        # Numeric tie-break: 2 comes before 10 (text sorting would not).
        self.assertEqual(ordered, [7, 2, 10, 1])

    def test_row_shows_all_required_fields(self):
        ticket = make_ticket(5, "Lab PC", "Hardware", "high", "open", "Ada")

        row = format_ticket_row(ticket)

        for expected in ("5", "Lab PC", "Hardware", "high", "open", "Ada"):
            self.assertIn(expected, row)

    def test_row_shows_unassigned(self):
        ticket = make_ticket(5, "Lab PC", "Hardware", "high", "open")

        self.assertIn("Unassigned", format_ticket_row(ticket))


class TestNormaliseChoice(unittest.TestCase):
    OPTIONS = ("Network", "Hardware", "Software", "Other")

    def test_blank_means_no_filter(self):
        self.assertIsNone(normalise_choice("", self.OPTIONS))
        self.assertIsNone(normalise_choice("   ", self.OPTIONS))
        self.assertIsNone(normalise_choice(None, self.OPTIONS))

    def test_returns_canonical_value_for_any_casing(self):
        self.assertEqual(normalise_choice("nEtWoRk", self.OPTIONS), "Network")

    def test_invalid_option_raises(self):
        with self.assertRaises(ValueError):
            normalise_choice("printers", self.OPTIONS)


if __name__ == "__main__":
    unittest.main()
