from rest_framework import serializers
from clinic.models import DoctorDB, AppointmentDb

class Doctor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDB
        fields = "__all__"
        read_only_fields = ["id", ]

class Appointment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDb
        fields = "__all__"
        read_only_fields = ["id", ]

    def validate(self, validated_data):
        ph = validated_data.get("phone")
        a_date = validated_data.get("appointment_date")

        if AppointmentDb.objects.filter(phone = ph, appointment_date= a_date).exists():
            raise serializers.ValidationError("Already Booked!")
        
        else:
            return validated_data