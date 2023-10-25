import datetime
from rest_framework import status, viewsets

from tic_api.permissions import IsStaff,IsStudent
from .models import Ticket
from .serializers import AllTicketSerializer, TicketEmpSerializer, TicketStudentSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework import generics



# View for Registering Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def TokenCreate(sender, instance, created, **kwargs):
        if created:
            token = Token.objects.create(user=instance)
            return token
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     token, created = Token.object.get_or_create(user=serializer.instance)
    #     return Response({
    #             'token': token.key, 
    #             }, 
    #         status=status.HTTP_201_CREATED)
    

    # def list(self, request, *args, **kwargs):
    #     response = {'message': 'You cant create Ticket like that'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


# ================================ Students only =============================================


class StdTicketCreate(generics.ListCreateAPIView):
    ticket = Ticket.objects.all()
    serializer_class = AllTicketSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStudent)
    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(created_by=user.id)
    def post(self, request):
        user = self.request.user
        title = request.data['title']
        content = request.data['content']
        ticket = Ticket.objects.create(created_by=user,ticket_status='Opening',title=title, content=content)
        serializer = TicketStudentSerializer(ticket, many=False)
        json = {
            'message': 'ticket is Created',
            'result': serializer.data
        }
        return Response(json , status=status.HTTP_200_OK)

class StdTicUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStudentSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStudent)
    lookup_field = 'pk'
    def get_queryset(self):
        # ticket = Ticket.objects.get(id=pk)
        user = self.request.user
        return Ticket.objects.filter(created_by=user)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = request.data['is_deleted']
        instance.is_archived = request.data['is_archived']
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            json = {
                'message': 'status not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)


# ==================================== End Students View ==============================================



# ---------------- employee for viewing all Opening tickets

class ViewEmpOpenTask(generics.ListAPIView):
    ticket = Ticket.objects.all()
    serializer_class = AllTicketSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStaff)
    def get_queryset(self):
        # user = self.request.user
        return Ticket.objects.filter(ticket_status='Opening')

# Update any Opening Ticket Tasks 

class EmpUpdateOpenTask(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketEmpSerializer #TicketEmpSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStaff)
    lookup_field = 'pk'
    def get_queryset(self):
        # ticket = Ticket.objects.get(id=pk)
        user = self.request.user
        return Ticket.objects.filter(ticket_status='Opening')
    

    def update(self, request, *args, **kwargs):

        instance = self.get_object()  #  
        if instance.ticket_status == 'Opening':  #  instance.assigned_to is None or
            instance.assigned_to = self.request.user
            instance.accepted_date = datetime.datetime.now()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(status=status.HTTP_200_OK)
            else:
                json = {
                    'message': 'status not provided'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            

# ---------------- employee for viewing all belonging tickets

class ViewEmpSelfTask(generics.ListAPIView):
    ticket = Ticket.objects.all()
    serializer_class = AllTicketSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStaff)
    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(assigned_to=user)
    


# Update Specific Employee References Tasks 

class EmpUpdateSelfTask(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketEmpSerializer #TicketEmpSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsStaff)
    lookup_field = 'pk'
    def get_queryset(self):
        # ticket = Ticket.objects.get(id=pk)
        user = self.request.user
        return Ticket.objects.filter(assigned_to=user)
    

    def update(self, request, *args, **kwargs):

        instance = self.get_object()  #  
        if instance.assigned_to == self.request.user:  #  or instance.ticket_status == 'Opening'
            instance.assigned_to = self.request.user
            instance.accepted_date = datetime.datetime.now()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(status=status.HTTP_200_OK)
            else:
                json = {
                    'message': 'status not provided'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            


# ----------------------------------- emp




#------------------------------end
