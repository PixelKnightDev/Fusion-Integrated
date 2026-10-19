from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from modules.elm.models.leave_types import LeaveType, LeaveBalance
from modules.elm.models.leave_application import LeaveApplication
from modules.elm.api.serializers import LeaveTypeSerializer, LeaveBalanceSerializer, LeaveApplicationSerializer
from modules.elm.services.leave_service import LeaveService
from modules.elm.services.workflow_service import WorkflowService

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

class LeaveBalanceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user_id = self.request.user.id
        return LeaveBalance.objects.filter(user_id=user_id)
    
    serializer_class = LeaveBalanceSerializer
    permission_classes = [IsAuthenticated]

class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = super().retrieve(request, *args, **kwargs)
        return Response(LeaveApplicationSerializer(instance).data)

    def create(self, request, *args, **kwargs):
        data = request.data
        leave_type_code = data.get('leave_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        purpose = data.get('purpose')
        
        validation = LeaveService.validate_application(
            request.user.id, leave_type_code, start_date, end_date, purpose
        )
        
        if not validation['valid']:
            return Response({"error": validation['reason']}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(LeaveApplicationSerializer(self.get_object()).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user_id=request.user.id)

    def update(self, request, *args, **kwargs):
        # Update logic with re-validation
        instance = self.get_object()
        data = request.data
        
        leave_type_code = data.get('leave_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        purpose = data.get('purpose')
        
        validation = LeaveService.validate_application(
            request.user.id, leave_type_code, start_date, end_date, purpose
        )
        
        if not validation['valid']:
            return Response({"error": validation['reason']}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(LeaveApplicationSerializer(instance).data)

    def perform_update(self, serializer):
        serializer.save()

@api_view(['POST'])
def record_decision(request):
    application_id = request.data.get('application_id')
    decision = request.data.get('decision')
    decision_maker_id = request.user.id
    
    application = get_object_or_404(LeaveApplication, id=application_id)
    WorkflowService.process_decision(application, decision, decision_maker_id)
    
    return Response(LeaveApplicationSerializer(application).data)
