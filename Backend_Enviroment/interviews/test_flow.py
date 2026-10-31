from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Answer, CandidateInterview, Question

CREATE_URL = "/api/recruiter/create-interview/"
PAYLOAD = {
    "role": "Backend Developer",
    "difficulty": "easy",
    "question_count": 3,
    "candidate_email": "candidate@example.com",
    "candidate_name": "Candidate",
}


class InterviewFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("recruiter", password="Str0ngPass!99")
        res = self.client.post(
            "/api/auth/login/",
            {"username": "recruiter", "password": "Str0ngPass!99"},
            content_type="application/json",
        )
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {res.json()['access']}"}

    def create_interview(self, questions=("Q1", "Q2", "Q3")):
        with patch(
            "interviews.views.generate_interview_questions",
            return_value=list(questions),
        ):
            res = self.client.post(
                CREATE_URL, PAYLOAD, content_type="application/json", **self.auth
            )
        return res, CandidateInterview.objects.get(candidate_email=PAYLOAD["candidate_email"])

    def test_create_interview_stores_requested_number_of_questions(self):
        res, interview = self.create_interview()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(interview.questions.count(), 3)
        self.assertEqual([q.order for q in interview.questions.all()], [1, 2, 3])

    def test_ai_failure_creates_no_interview(self):
        with patch(
            "interviews.views.generate_interview_questions",
            side_effect=RuntimeError("gemini down"),
        ):
            res = self.client.post(
                CREATE_URL, PAYLOAD, content_type="application/json", **self.auth
            )

        self.assertEqual(res.status_code, 503)
        self.assertFalse(CandidateInterview.objects.exists())

    def test_overall_score_averages_only_scored_answers(self):
        _, interview = self.create_interview()
        questions = list(interview.questions.all())

        # Two scored answers plus one the AI could not score.
        for question, score in zip(questions, [8.0, 6.0, None]):
            Answer.objects.create(
                question=question, answer_text="an answer", score=score
            )

        res = self.client.post(f"/api/public/interview/{interview.token}/complete/")

        self.assertEqual(res.status_code, 200)
        # Averaging over all three answers would have given 4.67.
        self.assertEqual(res.json()["overall_score"], 7.0)

    def test_completed_interview_rejects_further_answers(self):
        _, interview = self.create_interview()
        question = interview.questions.first()
        self.client.post(f"/api/public/interview/{interview.token}/complete/")

        res = self.client.post(
            f"/api/public/interview/{interview.token}/answer/",
            {"question_id": question.id, "answer_text": "late answer"},
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        self.assertFalse(Answer.objects.exists())

    def test_blank_answer_is_rejected(self):
        _, interview = self.create_interview()
        question = interview.questions.first()

        res = self.client.post(
            f"/api/public/interview/{interview.token}/answer/",
            {"question_id": question.id, "answer_text": "   "},
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        self.assertFalse(Answer.objects.exists())

    def test_answer_is_saved_even_when_evaluation_fails(self):
        _, interview = self.create_interview()
        question = interview.questions.first()

        with patch(
            "interviews.views.evaluate_answer", side_effect=RuntimeError("gemini down")
        ):
            res = self.client.post(
                f"/api/public/interview/{interview.token}/answer/",
                {"question_id": question.id, "answer_text": "a real answer"},
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200)
        answer = Answer.objects.get(question=question)
        self.assertEqual(answer.answer_text, "a real answer")
        self.assertIsNone(answer.score)

    def test_report_is_scoped_to_the_owning_recruiter(self):
        _, interview = self.create_interview()
        User.objects.create_user("intruder", password="Str0ngPass!99")
        res = self.client.post(
            "/api/auth/login/",
            {"username": "intruder", "password": "Str0ngPass!99"},
            content_type="application/json",
        )
        intruder = {"HTTP_AUTHORIZATION": f"Bearer {res.json()['access']}"}

        res = self.client.get(
            f"/api/recruiter/report/{interview.id}/", **intruder
        )

        self.assertEqual(res.status_code, 404)

    def test_interview_link_uses_configured_frontend_url(self):
        with self.settings(FRONTEND_URL="https://app.example.com"):
            res, interview = self.create_interview()

        self.assertEqual(
            res.json()["interview_link"],
            f"https://app.example.com/interview/{interview.token}",
        )
