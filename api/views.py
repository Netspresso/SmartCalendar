from django.shortcuts import render
from .models import Note, Task
from .serializers import NoteSerializer, TaskSerializer, UserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


@api_view(['GET'])
def notes_api_overview(request):

    api_urls = {
        'List': '/list/',
        'Note_details': '/details/<str:pk>/',
        'User_notes_list': '/<username>/notes-list',
        'Create': '<username>/create/',
        'Update': '/update/<str:pk>/',
        'Delete': '/destroy/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def tasks_api_overview(request):

    api_urls = {
        'List': '/list/',
        'Task_details': '/details/<str:pk>/',
        'User_tasks_list': '/<username>/notes-list',
        'Create': '<username>/create/',
        'Update': '/update/<str:pk>/',
        'Delete': '/destroy/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def api_overview(request):

    api_urls = {
        'Note-api': '/notes/',
        'Task-api': '/tasks/',
        'Login': '/login',
        'Logout': '/logout',
        'Logout_tall': '/logoutall',
        'Register': '/register',
    }

    return Response(api_urls)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def notes_list(self, request):
    ''' API endpoint that allows to see all notes '''
    queryset = Note.objects.all()
    serializer_class = NoteSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def note_details(self, request, pk):
    ''' API endpoint that allows to see all notes '''
    queryset = Note.objects.get(id=pk)
    serializer_class = NoteSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def user_notes_list(self, request, username):
    ''' API endpoint that allows to see all user's notes '''
    user = User.objects.get(username=username)
    queryset = Note.objects.filter(owner=user.id).order_by(id)
    serializer = NoteSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def note_create(self, request, username):
    ''' API endpoint that create new note assigned to the user '''
    '''
    {
        "title": <str>,
        "content: <str>
    }
    '''
    user = User.objects.get(username=username)
    queryset = Note(owner=user)
    serializer = NoteSerializer(queryset, data=request.data)

    if serializer.is_valid():
        ''' if data inserted to serializer through the endpoint are valid - serializer saves '''
        serializer.save()

    return Response(serializer.data)  # 201 Request should be shown


@api_view(['PUT'])
def note_update(self, request, pk):
    ''' API endpoint that create new note assigned to the user '''
    '''
    {
        "id": <int>.
        "title": <str>,
        "content: <str>,
        "owner": <str>
    }
    '''
    queryset = Note.objects.get(id=pk)
    serializer = NoteSerializer(queryset, data=request.data)

    if serializer.is_valid():
        ''' if data inserted to serializer through the endpoint are valid - serializer saves '''
        serializer.save()

    return Response(serializer.data)  # 201 Request should be shown


@api_view(['DELETE'])
def note_destroy(self, request, pk=None):
    ''' This view delete Note '''
    note = Note.objects.get(id=pk)
    note.delete()

    return Response("Item succesfully deleted")


@api_view(['GET'])
def tasks_list(self, request):
    ''' API endpoint that allows to see all notes '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def task_details(self, request, pk):
    ''' API endpoint that allows to see all notes '''
    queryset = Task.objects.get(id=pk)
    serializer_class = TaskSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def user_tasks_list(self, request, username):
    ''' API endpoint that allows to see all user's notes '''
    user = User.objects.get(username=username)
    queryset = Task.objects.filter(owner=user.id).order_by(id)
    serializer = TaskSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def task_create(self, request, username):
    ''' API endpoint that create new note assigned to the user '''
    '''
    {
        "task name": <str>,
        "priority_weight": <choices (A, B, C, D, E)>,
        "priority_order": <int> (without repetition)
    }
    '''
    user = User.objects.get(username=username)
    queryset = Task(owner=user)
    serializer = TaskSerializer(queryset, data=request.data)

    if serializer.is_valid():
        ''' if data inserted to serializer through the endpoint are valid - serializer saves '''
        serializer.save()

    return Response(serializer.data)  # 201 Request should be shown


@api_view(['PUT'])
def task_update(self, request, pk):
    ''' API endpoint that create new note assigned to the user '''
    '''
    {
        "id": <int>.
        "task name": <str>,
        "priority_weight": <choices (A, B, C, D, E)>,
        "priority_order": <int> (without repetition),
        "owner": <str>
    }
    '''
    queryset = Task.objects.get(id=pk)
    serializer = TaskSerializer(queryset, data=request.data)

    if serializer.is_valid():
        ''' if data inserted to serializer through the endpoint are valid - serializer saves '''
        serializer.save()

    return Response(serializer.data)  # 201 Request should be shown


@api_view(['DELETE'])
def task_destroy(self, request, pk=None):
    ''' This view delete Note '''
    note = Task.objects.get(id=pk)
    note.delete()

    return Response("Item succesfully deleted")


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user":
            UserSerializer(user, context=self.get_serializer_context()).data,
            "token":
            AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )
    '''
    {
        "username": <str>,
        "password": <str>
    }
    '''
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
