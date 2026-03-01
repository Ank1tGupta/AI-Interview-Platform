from rest_framework import serializers
from .models import Question, Answer, Evaluation, CandidateInterview

class PublicQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "order"]

class PublicInterviewSerializer(serializers.ModelSerializer):
    questions = PublicQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateInterview
        fields = [
            "id",
            "role",
            "difficulty",
            "candidate_name",
            "candidate_email",
            "is_completed",
            "questions"
        ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'question_type',
            'order',
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'answer_text',
            'time_taken_seconds',
            'answered_at',
            'score',
            'feedback',
        ]


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ["score", "feedback", "improvement_tips"]


class AnswerReportSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ["answer_text", "evaluation"]


class QuestionReportSerializer(serializers.ModelSerializer):
    answer = AnswerReportSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "order", "answer"]

class InterviewReportSerializer(serializers.ModelSerializer):
    questions = QuestionReportSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateInterview
        fields = [
            "id",
            "candidate_name",
            "candidate_email",
            "overall_score",
            "is_completed",
            "questions"
        ]