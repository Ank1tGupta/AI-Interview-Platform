from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .services.ai_service import generate_interview_questions
from .services.ai_service import evaluate_answer
from .models import Evaluation
from django.utils import timezone
from .serializers import InterviewReportSerializer
from django.core.mail import send_mail

from .models import InterviewTemplate, CandidateInterview


from .models import Question, Answer
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    PublicInterviewSerializer,
)

import re

def extract_score(ai_text):
    """
    Extracts score out of 10 from AI response.
    Example match: 'Score: 7/10'
    """
    match = re.search(r'(\d+(\.\d+)?)/10', ai_text)
    if match:
        return float(match.group(1))
    return 0.0


class CreateCandidateInterviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, template_id):
        template = get_object_or_404(
            InterviewTemplate,
            id=template_id,
            recruiter=request.user
        )

        candidate_email = request.data.get("candidate_email")

        if not candidate_email:
            return Response(
                {"error": "candidate_email is required"},
                status=400
            )

        candidate = CandidateInterview.objects.create(
            template=template,
            candidate_email=candidate_email
        )


        interview_link = f"http://localhost:5173/interview/{candidate.token}"

        send_mail(
            subject="AI Interview Invitation",
            message=f"Click here to start your interview:\n\n{interview_link}",
            from_email="noreply@aiinterview.com",
            recipient_list=[candidate_email],
        )

        return Response({
            "message": "Candidate interview created",
            "interview_link": interview_link
        })
    
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

        question_id = request.data.get("question_id")
        answer_text = request.data.get("answer_text")
        time_taken = request.data.get("time_taken_seconds")

        question = get_object_or_404(
            Question,
            id=question_id,
            interview=interview
        )

        # 🧠 AI Evaluation
        try:
            evaluation = evaluate_answer(
                question.text,
                answer_text
            )
        except Exception as exc:  # catch JSON errors or API failures
            print("Evaluation error:", exc)
            evaluation = {"score": None, "feedback": None}

        # store whatever we got (may be None) - avoids blowing up later
        answer, created = Answer.objects.update_or_create(
            question=question,
            defaults={
                "answer_text": answer_text,
                "time_taken_seconds": time_taken,
                "score": evaluation.get("score"),
                "feedback": evaluation.get("feedback"),
            }
        )
        print("Saved Score:", answer.score)
        print("Saved Feedback:", answer.feedback)
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

        answers = Answer.objects.filter(
            question__interview=interview
        )

        total_score = sum(a.score for a in answers if a.score is not None)
        count = answers.count()

        interview.overall_score = (
            total_score / count if count > 0 else 0
        )
        interview.is_completed = True
        interview.completed_at = timezone.now()
        interview.save()

        return Response({
            "message": "Interview completed",
            "overall_score": interview.overall_score
        })

class RecruiterTemplateListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        templates = InterviewTemplate.objects.filter(
            recruiter=request.user
        )

        data = []

        for template in templates:
            data.append({
                "id": template.id,
                "role": template.role,
                "difficulty": template.difficulty,
                "question_count": template.question_count
            })

        return Response(data)
    
class TemplateCandidateListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, template_id):
        template = get_object_or_404(
            InterviewTemplate,
            id=template_id,
            recruiter=request.user
        )

        candidates = template.candidateinterview_set.all()

        data = []

        for c in candidates:
            data.append({
                "id": c.id,
                "email": c.candidate_email,
                "is_completed": c.is_completed,
                "overall_score": c.overall_score,
                "token": str(c.token)
            })

        return Response(data)

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

        for question in interview.questions.all():
            try:
                answer = question.answer  # ✅ correct for OneToOne
            except Answer.DoesNotExist:
                answer = None

            questions_data.append({
                "question": question.text,
                "answer": answer.answer_text if answer else None,
                "score": getattr(answer, "score", None),
                "feedback": getattr(answer, "feedback", None),
            })

        return Response({
            "candidate_email": interview.candidate_email,
            "role": interview.role,
            "difficulty": interview.difficulty,
            "overall_score": interview.overall_score,
            "completed_at": interview.completed_at,
            "questions": questions_data
        })

class CreateInterviewTemplateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        difficulty = request.data.get("difficulty")
        question_count = request.data.get("question_count", 5)

        if not role or not difficulty:
            return Response(
                {"error": "role and difficulty are required"},
                status=400
            )

        template = InterviewTemplate.objects.create(
            recruiter=request.user,
            role=role,
            difficulty=difficulty,
            question_count=question_count
        )

        return Response({
            "id": template.id,
            "role": template.role,
            "difficulty": template.difficulty,
            "question_count": template.question_count
        })

class CreateInterviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        difficulty = request.data.get("difficulty")
        question_count = request.data.get("question_count")
        candidate_email = request.data.get("candidate_email")

        if not all([role, difficulty, question_count, candidate_email]):
            return Response({"error": "All fields required"}, status=400)

        interview = CandidateInterview.objects.create(
            recruiter=request.user,
            role=role,
            difficulty=difficulty,
            question_count=question_count,
            candidate_email=candidate_email
        )

        # Generate AI questions
        questions = generate_interview_questions(role, difficulty)

        for i, q in enumerate(questions[:int(question_count)]):
            Question.objects.create(
                interview=interview,
                text=q,
                order=i+1
            )

        # Send email
        interview_link = f"http://localhost:5173/interview/{interview.token}"

        send_mail(
            subject="AI Interview Invitation",
            message=f"Click here to start your interview:\n\n{interview_link}",
            from_email="noreply@aiinterview.com",
            recipient_list=[candidate_email],
        )

        return Response({"message": "Interview created & email sent"})
    
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
                "email": i.candidate_email,
                "role": i.role,
                "difficulty": i.difficulty,
                "status": "Completed" if i.is_completed else "Pending",
                "score": i.overall_score
            })

        return Response(data)