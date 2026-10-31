from django.test import SimpleTestCase

from .services.ai_service import parse_evaluation


class ParseEvaluationTests(SimpleTestCase):
    def test_parses_plain_json(self):
        result = parse_evaluation('{"score": 7, "feedback": "Good"}')
        self.assertEqual(result, {"score": 7.0, "feedback": "Good"})

    def test_strips_markdown_fences_and_surrounding_prose(self):
        raw = 'Here you go:\n```json\n{"score": 8.5, "feedback": "Solid"}\n```'
        self.assertEqual(parse_evaluation(raw)["score"], 8.5)

    def test_clamps_out_of_range_score(self):
        self.assertEqual(parse_evaluation('{"score": 42}')["score"], 10.0)
        self.assertEqual(parse_evaluation('{"score": -3}')["score"], 0.0)

    def test_returns_empty_result_for_unparseable_text(self):
        for raw in ["", "I cannot evaluate this.", "{not json}"]:
            self.assertEqual(
                parse_evaluation(raw), {"score": None, "feedback": None}
            )

    def test_non_numeric_score_becomes_none(self):
        result = parse_evaluation('{"score": "excellent", "feedback": "ok"}')
        self.assertEqual(result, {"score": None, "feedback": "ok"})
