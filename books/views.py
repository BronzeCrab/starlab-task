from openpyxl import load_workbook
from rest_framework import permissions, viewsets, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer

from io import BytesIO


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ("title", "date_published", "genre")


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ("name",)


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data["upload_file"]
        wb = load_workbook(filename=BytesIO(file_obj.read()))
        print("successful readin of xlsx")
        print(wb)
        return Response(status=204)
