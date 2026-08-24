from rest_framework import serializers
from .models import Bill, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = [
            'id', 'bill',
            'shirt_length', 'shirt_chest', 'shirt_stomach',
            'shirt_sleeve', 'shirt_shoulder', 'shirt_collar',
            'pant_length', 'pant_waist', 'pant_thigh',
            'pant_bottom', 'pant_hip', 'pant_seat_langot',
            'notes', 'updated_at',
        ]
        read_only_fields = ['id', 'bill', 'updated_at']


class BillSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    has_measurement = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = [
            'id', 'bill_no', 'name', 'phone',
            'cloth_price', 'stitching_price', 'total',
            'shirt_ready', 'pant_ready',
            'has_measurement',
            'created_at', 'updated_at','note',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        # 'owner' field yahan jaan-boojh kar shamil nahi hai — wo login wale
        # user se automatically set hota hai (views.py me), client ise nahi bhej sakta.

    def get_has_measurement(self, obj):
        return hasattr(obj, 'measurement')
