import unittest
from expert_rules import expert
from weighted_rules import weighted, explain


def vehicle(buying="med", maint="med", doors="4",
            persons="4", lug_boot="med", safety="high"):
    return {
        "buying": buying,
        "maint": maint,
        "doors": doors,
        "persons": persons,
        "lug_boot": lug_boot,
        "safety": safety
    }


class TestExpertRules(unittest.TestCase):

    def test_low_safety(self):
        self.assertEqual(
            expert(vehicle(safety="low")), "unacc"
        )

    def test_two_passengers(self):
        self.assertEqual(
            expert(vehicle(persons="2")), "unacc"
        )

    def test_medium_safety_small_boot(self):
        self.assertEqual(
            expert(vehicle(safety="med", lug_boot="small")),
            "unacc"
        )

    def test_high_purchase_and_maintenance_cost(self):
        self.assertEqual(
            expert(vehicle(buying="vhigh", maint="vhigh")),
            "unacc"
        )

    def test_very_good_vehicle(self):
        self.assertEqual(
            expert(vehicle(
                buying="low", maint="low",
                persons="more", lug_boot="big"
            )),
            "vgood"
        )

    def test_good_vehicle(self):
        self.assertEqual(expert(vehicle()), "good")

    def test_default_acceptable(self):
        self.assertEqual(
            expert(vehicle(safety="med")), "acc"
        )


class TestWeightedRules(unittest.TestCase):

    def check_score(self, row, expected_score, expected_label):
        label, score, points, reason = explain(row)

        self.assertEqual(score, expected_score)
        self.assertEqual(sum(points.values()), expected_score)
        self.assertEqual(label, expected_label)
        self.assertEqual(weighted(row), expected_label)

    def test_score_8(self):
        self.check_score(
            vehicle(buying="vhigh", maint="vhigh"), 9, "acc"
        )
        self.check_score(
            vehicle(buying="vhigh", maint="vhigh",
                    lug_boot="small"), 8, "unacc"
        )

    def test_score_9(self):
        self.check_score(
            vehicle(buying="vhigh", maint="vhigh"), 9, "acc"
        )

    def test_score_12(self):
        self.check_score(
            vehicle(buying="high"), 12, "acc"
        )

    def test_score_13(self):
        self.check_score(vehicle(), 13, "good")

    def test_score_14(self):
        self.check_score(
            vehicle(buying="low"), 14, "good"
        )

    def test_score_15(self):
        self.check_score(
            vehicle(buying="low", maint="low"), 15, "vgood"
        )

    def test_maximum_score_17(self):
        self.check_score(
            vehicle(buying="low", maint="low",
                    persons="more", lug_boot="big"),
            17, "vgood"
        )

    def test_safety_override(self):
        row = vehicle(
            buying="low", maint="low",
            persons="more", lug_boot="big", safety="low"
        )

        label, score, points, reason = explain(row)

        self.assertEqual(score, 13)
        self.assertEqual(label, "unacc")
        self.assertEqual(reason, "Mandatory rejection")

    def test_passenger_override(self):
        row = vehicle(
            buying="low", maint="low",
            persons="2", lug_boot="big"
        )

        label, score, points, reason = explain(row)

        self.assertEqual(score, 14)
        self.assertEqual(label, "unacc")
        self.assertEqual(reason, "Mandatory rejection")


if __name__ == "__main__":
    unittest.main(verbosity=2)
