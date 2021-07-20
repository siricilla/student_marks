from django.urls import path
from django.urls.conf import include
from markscal.views import MarksView, TotalMarksView, AvgMarksView

urlpatterns = [
    path("marks", MarksView.as_view()),
    path("marks/<int:id>", MarksView.as_view()),
    path("totalmarks", TotalMarksView.as_view()),
    path("averagemarks", AvgMarksView.as_view()),
]