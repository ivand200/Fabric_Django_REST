from rest_framework.serializers import ModelSerializer
from .models import User, Survey

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name"]

class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = ["user", "question", "answer", "created_at", "ended_at"]
