import os
import json
import unittest

from app.pipeline import NavigatorPipeline


CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "corpus")


def assert_schema(testcase: unittest.TestCase, response):
    testcase.assertEqual(set(response.keys()), {"summary", "relevant_sections", "limitations", "confidence"})
    testcase.assertIsInstance(response["summary"], str)
    testcase.assertIsInstance(response["limitations"], list)
    testcase.assertIn(response["confidence"], {"very_low", "low", "medium", "high"})
    for item in response["relevant_sections"]:
        testcase.assertEqual(set(item.keys()), {"title", "why_relevant"})
        testcase.assertIsInstance(item["title"], str)
        testcase.assertIsInstance(item["why_relevant"], str)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = NavigatorPipeline(CORPUS_DIR)

    def test_refusal(self):
        res = self.pipeline.run("Is this lawful?")
        assert_schema(self, res)
        self.assertEqual(res["confidence"], "very_low")
        self.assertEqual(res["relevant_sections"], [])
        self.assertIn("Cannot provide legal advice", res["summary"])

    def test_refusal_lawful_under_gdpr(self):
        res = self.pipeline.run("Is our planned tracking feature lawful under GDPR/UK GDPR?")
        assert_schema(self, res)
        self.assertEqual(res["confidence"], "very_low")
        self.assertEqual(res["relevant_sections"], [])

    def test_refusal_action_recommendation(self):
        res = self.pipeline.run("What should we do to comply with ICO guidance for consent banners / legitimate interests?")
        assert_schema(self, res)
        self.assertEqual(res["confidence"], "very_low")
        self.assertEqual(res["relevant_sections"], [])

    def test_refusal_step_by_step_compliance_plan(self):
        res = self.pipeline.run("Give me a step-by-step plan to become compliant with the ICO on lawful basis and privacy notices.")
        assert_schema(self, res)
        self.assertEqual(res["confidence"], "very_low")
        self.assertEqual(res["relevant_sections"], [])

    def test_not_refused_lawful_basis_guidance_question(self):
        res = self.pipeline.run(
            "What does the guidance say about choosing and documenting a lawful basis before processing personal data?"
        )
        assert_schema(self, res)
        self.assertNotEqual(res["confidence"], "very_low")
        self.assertGreaterEqual(len(res["relevant_sections"]), 1)

    def test_confidence_high_or_medium_when_multiple_sections(self):
        res = self.pipeline.run("What does ICO say about documenting lawful basis and transparency?")
        assert_schema(self, res)
        self.assertGreaterEqual(len(res["relevant_sections"]), 1)
        self.assertIn(res["confidence"], {"high", "medium"})

    def test_confidence_low_on_weak_retrieval(self):
        res = self.pipeline.run("space rockets telemetry data")
        assert_schema(self, res)
        self.assertIn(res["confidence"], {"low", "very_low"})

    def test_out_of_corpus_question_degrades_confidence(self):
        res = self.pipeline.run("What does ICO guidance say about international data transfers and SCCs?")
        assert_schema(self, res)
        self.assertIn(res["confidence"], {"low", "very_low"})

    def test_output_json_serializable(self):
        res = self.pipeline.run("How should we record processing activities?")
        assert_schema(self, res)
        json.dumps(res)  # should not raise


if __name__ == "__main__":
    unittest.main()
