from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDB, AppointmentDb
from clinic.serializers import Doctor_Serializer, Appointment_Serializer
from datetime import time, timedelta, datetime
from rest_framework import serializers


# Create your views here.
class DoctorListCreateView(APIView):
    def get(self, request):
        qs = DoctorDB.objects.all()
        serializer_instance = Doctor_Serializer(qs, many= True)
        return Response(data=serializer_instance.data)

    def post(self, request):
        form_data = request.data
        serializer_instance = Doctor_Serializer(data= form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data= {"message": "doctor details added!"})
        else:
            return Response(data= serializer_instance.errors)

class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(DoctorDB, id = pk)
        s_instance = Doctor_Serializer(qs)
        return Response(data= s_instance.data)

    def put(self, request, pk):
        form_data = request.data
        dr_obj = get_object_or_404(DoctorDB, id=pk)
        s_instance = Doctor_Serializer(data= form_data, instance= dr_obj)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= {"message": "doctor details updated!"})
        else:
            return Response(data= s_instance.errors)

    def delete(self, request, pk):
        dr_obj = get_object_or_404(DoctorDB, id = pk)
        dr_obj.delete()
        return Response(data= {"message": "doctor details deleted!"})


class AppointmentListCreateView(APIView):
    def get(self, request):
        qs = AppointmentDb.objects.all()
        s_instance = Appointment_Serializer(qs, many=True)
        return Response(data= s_instance.data)

    def post(self, request):
        form_data = request.data
        s_instance = Appointment_Serializer(data= form_data)
        if s_instance.is_valid():
            appointment_date = s_instance.validated_data.get("appointment_date")
            doctor_id = s_instance.validated_data.get("doctor_id")

            last_appointment = AppointmentDb.objects.filter(
                appointment_date = appointment_date,
                doctor_id = doctor_id
            ).order_by("-token_number").first()

            if last_appointment is None:
                form_data["token_number"] = 1
                form_data["appointment_time"] = time(10, 0)
            else:
                form_data["token_number"] = last_appointment.token_num ber + 1
                current_time = datetime.combine(appointment_date, last_appointment.appointment_time)
                next_time = current_time + timedelta(minutes= 15)

                # lunch break
                if next_time.time() == time(12, 30):
                    next_time = datetime.combine(appointment_date, time(13, 30))

                # slot complete
                if next_time.time() == time(17, 0):
                    raise serializers.ValidationError("No slots available today..")

                form_data["appointment_time"] = next_time

            qs = AppointmentDb.objects.create(**form_data)
            s_instance = Appointment_Serializer(qs)
            return Response(data={
                "Status" : "Booked Successfully",
                "Token Number" : form_data["token_number"],
                "Appointment Time" : form_data["appointment_time"]
            })
            
        else:
            return Response(data= s_instance.errors)

