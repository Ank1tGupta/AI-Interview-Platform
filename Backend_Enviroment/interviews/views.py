import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, CandidateInterview, Question
from .serializers import PublicInterviewSerializer
from .services.ai_service import evaluate_answer, generate_interview_questions

logger = logging.getLogger(__name__)


def send_invitation(interview):
    """Email the candidate their interview link. Returns the link.

    A mail failure must not lose the interview that was already created,
    so it is logged rather than raised.
    """
    link = f"{settings.FRONTEND_URL}/interview/{interview.token}"
    try:
        send_mail(
            subject="AI Interview Invitation",
            message=f"Click here to start your interview:\n\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[interview.candidate_email],
        )
    except Exception:
        logger.exception("Failed to send invitation to %s", interview.candidate_email)
        return link, False
    return link, True


class PublicInterviewAccessAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        interview = get_object_or_404(
            CandidateInterview,
            token=token
        )

        if interview.is_completed:
            return Response(
                {"error": "This interview has already been completed"},
                status=400
            )

        serializer = PublicInterviewSerializer(interview)
        return Response(serializer.data)
    
class SubmitAnswerAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        interview = get_object_or_404(
            CandidateInterview,
            token=token
        )

        if interview.is_completed:
            return Response(
                {"error": "This interview has already been completed"},
                status=400
            )

        answer_text = request.data.get("answer_text")
        if not answer_text or not str(answer_text).strip():
            return Response({"error": "answer_text is required"}, status=400)

        question = get_object_or_404(
            Question,
            id=request.data.get("question_id"),
            interview=interview
        )

        try:
            time_taken = request.data.get("time_taken_seconds")
            time_taken = None if time_taken is None else max(0, int(time_taken))
        except (TypeError, ValueError):
            time_taken = None

        # An AI failure must not cost the candidate their answer, so store it
        # unscored and let the recruiter see a missing score.
        try:
            evaluation = evaluate_answer(question.text, answer_text)
        except Exception:
            logger.exception("Evaluation failed for question %s", question.id)
            evaluation = {"score": None, "feedback": None}

        answer, _ = Answer.objects.update_or_create(
            question=question,
            defaults={
                "answer_text": answer_text,
                "time_taken_seconds": time_taken,
                "score": evaluation.get("score"),
                "feedback": evaluation.get("feedback"),
            }
        )

        return Response({
            "message": "Answer submitted",
            "score": answer.score,
            "feedback": answer.feedback
        })


class CompleteInterviewAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        interview = get_object_or_404(
            CandidateInterview,
            token=token
        )

        if interview.is_completed:
            return Response(
                {"error": "This interview has already been completed"},
                status=400
            )

        # Average over scored answers only - unscored ones (AI failures or
        # skipped questions) would otherwise drag the average down.
        scores = [
            a.score for a in Answer.objects.filter(question__interview=interview)
            if a.score is not None
        ]

        interview.overall_score = (
            round(sum(scores) / len(scores), 2) if scores else None
        )
        interview.is_completed = True
        interview.completed_at = timezone.now()
        interview.save()

        return Response({
            "message": "Interview completed",
            "overall_score": interview.overall_score
        })

class RecruiterReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, interview_id):
        try:
            interview = CandidateInterview.objects.get(
                id=interview_id,
                recruiter=request.user
            )
        except CandidateInterview.DoesNotExist:
            return Response({"error": "Interview not found"}, status=404)

        questions_data = []

        for question in interview.questions.select_related("answer"):
            try:
                answer = question.answer  # OneToOne reverse accessor
            except Answer.DoesNotExist:
                answer = None

            questions_data.append({
                "id": question.id,
                "question": question.text,
                "answer": answer.answer_text if answer else None,
                "score": getattr(answer, "score", None),
                "feedback": getattr(answer, "feedback", None),
            })

        return Response({
            "candidate_name": interview.candidate_name,
            "candidate_email": interview.candidate_email,
            "role": interview.role,
            "difficulty": interview.difficulty,
            "overall_score": interview.overall_score,
            "completed_at": interview.completed_at,
            "questions": questions_data
        })

MAX_QUESTIONS = 20
DIFFICULTIES = ("easy", "medium", "hard")


class CreateInterviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        difficulty = request.data.get("difficulty")
        question_count = request.data.get("question_count")
        candidate_email = request.data.get("candidate_email")
        candidate_name = request.data.get("candidate_name")

        if not all([role, difficulty, question_count, candidate_email, candidate_name]):
            return Response({"error": "All fields required"}, status=400)

        try:
            question_count = int(question_count)
        except (TypeError, ValueError):
            return Response({"error": "question_count must be a number"}, status=400)

        if not 1 <= question_count <= MAX_QUESTIONS:
            return Response(
                {"error": f"question_count must be between 1 and {MAX_QUESTIONS}"},
                status=400
            )

        if difficulty not in DIFFICULTIES:
            return Response({"error": "Invalid difficulty"}, status=400)

        # Generate the questions before creating anything, so an AI failure
        # does not leave an interview with no questions in it.
        try:
            questions = generate_interview_questions(
                role, difficulty, count=question_count
            )
        except Exception:
            logger.exception("Question generation failed for role=%s", role)
            return Response(
                {"error": "Could not generate interview questions. Try again."},
                status=503
            )

        if not questions:
            return Response(
                {"error": "Could not generate interview questions. Try again."},
                status=503
            )

        interview = CandidateInterview.objects.create(
            recruiter=request.user,
            role=role,
            difficulty=difficulty,
            question_count=len(questions),
            candidate_email=candidate_email,
            candidate_name=candidate_name
        )

        Question.objects.bulk_create([
            Question(interview=interview, text=q, order=i + 1)
            for i, q in enumerate(questions)
        ])

        interview_link, mailed = send_invitation(interview)

        return Response({
            "message": (
                "Interview created & email sent" if mailed
                else "Interview created, but the invitation email failed to send"
            ),
            "interview_link": interview_link,
        })


class RecruiterInterviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interviews = CandidateInterview.objects.filter(
            recruiter=request.user
        )

        data = []

        for i in interviews:
            data.append({
                "id": i.id,
                "name": i.candidate_name,
                "email": i.candidate_email,
                "role": i.role,
                "difficulty": i.difficulty,
                "status": "Completed" if i.is_completed else "Pending",
                "score": i.overall_score
            })

        return Response(data)

class RecruiterInterviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, interview_id):
        try:
            interview = CandidateInterview.objects.get(
                id=interview_id,
                recruiter=request.user
            )
        except CandidateInterview.DoesNotExist:
            return Response({"error": "Interview not found"}, status=404)

        interview.delete()
        return Response({"message": "Interview deleted"})
