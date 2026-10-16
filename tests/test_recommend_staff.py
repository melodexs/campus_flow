
import unittest

from campusflow.recommend_staff import recommend_staff


class TestRecommendStaff(unittest.TestCase):

    def test_recommends_network_staff(self):
        self.assertEqual(
            recommend_staff("Network"),
            ["Mr. Kingsley", "Mr. Godswill"],
        )

    def test_recommends_hardware_staff(self):
        self.assertEqual(
            recommend_staff("Hardware"),
            ["Mr. Ayuba", "Mr. Gabriel"],
        )

    def test_recommends_software_staff(self):
        self.assertEqual(
            recommend_staff("Software"),
            ["Mr. Kingsley", "Mr. Emmanuel"],
        )

    def test_recommends_other_staff(self):
        self.assertEqual(
            recommend_staff("Other"),
            ["Mr. Onche"],
        )

    def test_rejects_invalid_category(self):
        with self.assertRaises(ValueError):
            recommend_staff("Electricity")


if __name__ == "__main__":
    unittest.main()
