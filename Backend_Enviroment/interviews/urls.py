from django.urls import path
from .views import (
    CreateInterviewAPIView,
    CreateInterviewTemplateAPIView,
    CompleteInterviewAPIView,
    SubmitAnswerAPIView,
    RecruiterInterviewListAPIView,
    # add detail view for deletes
    RecruiterInterviewDetailAPIView,
    RecruiterTemplateListAPIView,
    CreateCandidateInterviewAPIView,
    PublicInterviewAccessAPIView,
    TemplateCandidateListAPIView,
    RecruiterReportAPIView
)
urlpatterns = [
    path("templates/<int:template_id>/create-candidate/",CreateCandidateInterviewAPIView.as_view()),
    path("public/interview/<uuid:token>/",PublicInterviewAccessAPIView.as_view()),
    path("public/interview/<uuid:token>/answer/",SubmitAnswerAPIView.as_view()),
    path("public/interview/<uuid:token>/complete/",CompleteInterviewAPIView.as_view()),
    path("recruiter/templates/",RecruiterTemplateListAPIView.as_view()),
    path("recruiter/templates/<int:template_id>/candidates/",TemplateCandidateListAPIView.as_view()),
    path("recruiter/report/<int:interview_id>/",RecruiterReportAPIView.as_view()),
    path("recruiter/templates/create/",CreateInterviewTemplateAPIView.as_view()),
    path("recruiter/create-interview/", CreateInterviewAPIView.as_view()),
    path("recruiter/interviews/", RecruiterInterviewListAPIView.as_view()),
    path("recruiter/interviews/<int:interview_id>/", RecruiterInterviewDetailAPIView.as_view()),
]
