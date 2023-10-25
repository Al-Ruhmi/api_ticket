from rest_framework import serializers, status
from .models import Ticket

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class TicketStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','title','content','created_by','ticket_status','is_archived','is_deleted']

class TicketEmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','assigned_to','ticket_status','accepted_date']


# serializer to get all fields for employees but only Opening status

class AllTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
