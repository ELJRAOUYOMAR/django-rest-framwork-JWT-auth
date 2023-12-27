from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import viewsets  
from rest_framework import permissions
from rest_framework import renderers

from app.models import Snippet
from .serializers import SnippetSerializer

@api_view(['GET',])
def snippet_list(request):
    try:
        snippet_list = Snippet.objects.all()
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet_list, many=True)
        return Response(serializer.data)
    

@api_view(['GET',])
def detail_snippet(request, id):
    try:
        snippet = Snippet.objects.get(pk=id)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)


#using viewsets

class SnippetViweSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsOwnerOrReadOnly]

    @action(detail=True, methods=['GET'])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        # Implement your 'highlight' logic here
        return Response(data={'message': 'Implement your highlight logic here'}, status=status.HTTP_200_OK)
