from django.urls import path

from .views import (
    CompleteInterviewAPIView,
    CreateInterviewAPIView,
    PublicInterviewAccessAPIView,
    RecruiterInterviewDetailAPIView,
    RecruiterInterviewListAPIView,
    RecruiterReportAPIView,
    SubmitAnswerAPIView,
)

urlpatterns = [
    path("public/interview/<uuid:token>/", PublicInterviewAccessAPIView.as_view()),
    path("public/interview/<uuid:token>/answer/", SubmitAnswerAPIView.as_view()),
    path("public/interview/<uuid:token>/complete/", CompleteInterviewAPIView.as_view()),
    path("recruiter/report/<int:interview_id>/", RecruiterReportAPIView.as_view()),
    path("recruiter/create-interview/", CreateInterviewAPIView.as_view()),
    path("recruiter/interviews/", RecruiterInterviewListAPIView.as_view()),
    path("recruiter/interviews/<int:interview_id>/", RecruiterInterviewDetailAPIView.as_view()),
]
