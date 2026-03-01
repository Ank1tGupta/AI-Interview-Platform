from django.db import models
from django.contrib.auth.models import User
import uuid

class InterviewTemplate(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_templates"
    )

    role = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    question_count = models.PositiveIntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['recruiter']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.recruiter.username} - {self.role} ({self.difficulty})"



class CandidateInterview(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_interviews"
    )

    # Interview configuration (no template anymore)
    role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    question_count = models.PositiveIntegerField(default=5)

    candidate_name = models.CharField(max_length=255, default="")
    candidate_email = models.EmailField()

    # Secure public link
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    overall_score = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["recruiter"]),
            models.Index(fields=["is_completed"]),
            models.Index(fields=["started_at"]),
        ]

    def __str__(self):
        # include name if available for easier debugging
        if self.candidate_name:
            return f"{self.candidate_name} <{self.candidate_email}> - {self.role}"
        return f"{self.candidate_email} - {self.role}"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('text', 'Text'),
        ('coding', 'Coding'),
        ('audio', 'Audio'),
    )

    interview = models.ForeignKey(
        CandidateInterview,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='text'
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['interview']),
        ]

    def __str__(self):
        return f"Q{self.order} - {self.interview.candidate_email}"



class Answer(models.Model):
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        related_name='answer'
    )

    answer_text = models.TextField(blank=True)

    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    answered_at = models.DateTimeField(auto_now_add=True)
    time_taken_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['question']),
        ]

class Evaluation(models.Model):
    answer = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        related_name='evaluation'
    )

    score = models.FloatField()
    feedback = models.TextField()
    improvement_tips = models.TextField()
    ai_raw_response = models.JSONField()

    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['score']),
        ]

    def __str__(self):
        return f"Score: {self.score}"