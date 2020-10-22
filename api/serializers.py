from rest_framework import serializers
from .models import Note, Task
from django.contrib.auth.models import User


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ('title', "content", 'owner')


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('task_name', 'priority_weight', 'prority_order', 'owner')


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # fields related to table with Notes and with Tasks
    notes = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Note.objects.all())
    tasks = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'notes', 'tasks')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user