from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bill, Measurement
from .serializers import BillSerializer, MeasurementSerializer


class BillViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for bills — login zaroori hai, aur har user sirf apne
    shop ke bills hi dekh/edit/delete kar sakta hai:
    GET    /api/bills/          -> sirf apne bills ki list
    POST   /api/bills/          -> naya bill (owner apne aap set hota hai)
    GET    /api/bills/{id}/     -> ek bill
    PUT    /api/bills/{id}/     -> update bill
    PATCH  /api/bills/{id}/     -> partial update (e.g. toggle shirt_ready)
    DELETE /api/bills/{id}/     -> delete bill
    """
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Sirf isi login-user (shop) ke bills return honge — doosre shop
        # ka data kabhi nahi dikhega, chahe URL me ID guess kar le.
        return Bill.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='measurement')
    def get_measurement(self, request, pk=None):
        """GET /api/bills/{id}/measurement/ -> is bill ki measurement laao"""
        bill = self.get_object()
        measurement, created = Measurement.objects.get_or_create(bill=bill)
        serializer = MeasurementSerializer(measurement)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'], url_path='measurement/save')
    def save_measurement(self, request, pk=None):
        """PUT /api/bills/{id}/measurement/save/ -> measurement add/edit/save karo"""
        bill = self.get_object()
        measurement, created = Measurement.objects.get_or_create(bill=bill)
        serializer = MeasurementSerializer(measurement, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
