from django.urls import include, path, re_path
from rest_framework import routers

from books import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet)
router.register(r"authors", views.AuthorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    re_path(r"^upload/(?P<filename>[^/]+)$", views.FileUploadView.as_view()),
]
