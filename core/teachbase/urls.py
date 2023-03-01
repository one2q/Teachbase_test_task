from django.urls import path

from teachbase.views import CoursesListView, CoursesDetailView, CreateUserView
from teachbase.yasg import urlpatterns as doc_urls

urlpatterns = [
    path("courses/", CoursesListView.as_view()),
    path("courses/<int:pk>/", CoursesDetailView.as_view()),
    path("users/", CreateUserView.as_view()),
]

urlpatterns += doc_urls
