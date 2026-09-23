from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import FileObjectSerializer
from .models import FileObject

class FileUploadView(APIView):
    # This parser is crucial for handling actual file uploads (multipart/form-data)
    parser_classes = (MultiPartParser, FormParser)
    
    # Ensure only logged-in users can upload files
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Pass the request context so the serializer knows who the user is
        serializer = FileObjectSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)