from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from knox import views as knox_views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
# router.register(r'notes', NoteViewSet, basename='notes')
urlpatterns = [
    path('', api_overview, name='api-overwiew'),
    path('notes/', notes_api_overview, name='notes-api-overwiew'),
    path('notes/list/', notes_list, name='notes-list'),
    path('notes/details/<str:pk>/', note_details, name='note-details'),
    path('notes/<username>/notes-list/',
         user_notes_list,
         name='user_notes-list'),
    path('notes/<username>/create/', note_create, name='note-create'),
    path('notes/update/<str:pk>/', note_update, name='note-update'),
    path('notes/destroy/<str:pk>/', note_destroy, name='note-destroy'),
    path('', api_overview, name='api-overwiew'),
    path('tasks/', tasks_api_overview, name='tasks-api-overwiew'),
    path('tasks/list/', tasks_list, name='list'),
    path('tasks/details/<str:pk>/', task_details, name='details'),
    path('tasks/<username>/notes-list/', user_tasks_list, name='tasks-list'),
    path('tasks/<username>/create/', task_create, name='create'),
    path('tasks/update/<str:pk>/', task_update, name='update'),
    path('tasks/destroy/<str:pk>/', task_destroy, name='destroy'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
urlpatterns += router.urls