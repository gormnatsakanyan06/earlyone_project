from django.http import JsonResponse ,HttpResponse
from .models import *
from django.shortcuts import render


#QR
import qrcode
from io import BytesIO
import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response


from .qr import create_qr_and_save

@api_view(['POST'])
def create_appointment(request):
    full_name = request.data.get('full_name')
    phone = request.data.get('phone')
    category = request.data.get('category')
    action_id = request.data.get('action_id')
    scheduled_time = request.data.get('scheduled_time')

    model_map = {
        'finance': BankAction,
        'government': GovernmentAction,
        'telecom': TelecomAction,
        'utility': ServiceAction,
    }

    selected_model = model_map.get(category)

    if not selected_model:
        return Response({"error": "Invalid category"}, status=400)

    content_type = ContentType.objects.get_for_model(selected_model)
    appointment = Appointment.objects.create(
        full_name=full_name,
        phone_number=phone,
        category=category,
        content_type=content_type,
        object_id=action_id,
        scheduled_at=scheduled_time
    )

    qr = create_qr_and_save(str(appointment.verification_code))
    appointment.qr_code = qr
    appointment.save()

    return Response({
        "appointment_id": appointment.id,
        "verification_code": str(appointment.verification_code),
        "qr_image": qr.image.url
    })

#QR
#Banks
def banks(request):
    banks = list(Bank.objects.values())
    return JsonResponse(banks, safe=False)


def bank_branches(request):
    branches = list(BankBranch.objects.values())
    return JsonResponse(branches, safe=False)


def bank_actions(request):
    actions = list(BankAction.objects.values())
    return JsonResponse(actions, safe=False)



#services



def service(request):
    service = list(Service.objects.values())
    return JsonResponse(service, safe=False)


def service_branches(request):
    branches = list(ServiceBranch.objects.values())
    return JsonResponse(branches, safe=False)


def service_actions(request):
    actions = list(ServiceAction.objects.values())
    return JsonResponse(actions, safe=False)



#government




def government(request):
    government = list(Government.objects.values())
    return JsonResponse(government, safe=False)


def government_branches(request):
    branches = list(GovernmentBranch.objects.values())
    return JsonResponse(branches, safe=False)


def government_actions(request):
    actions = list(GovernmentAction.objects.values())
    return JsonResponse(actions, safe=False)





#telecom 




def telecom(request):
    telecom = list(Telecom.objects.values())
    return JsonResponse(telecom, safe=False)


def telecom_branches(request):
    branches = list(TelecomBranch.objects.values())
    return JsonResponse(branches, safe=False)


def telecom_actions(request):
    actions = list(TelecomAction.objects.values())
    return JsonResponse(actions, safe=False)




def home(request):
    return HttpResponse("Earlyone server is running 🚀")

# Create your views here.

def appointment(request):
    return render(request, "core/appointment.html")

def finance(request):
    return render(request, 'core/finance.html')


def government(request):
    return render(request, 'core/government.html')

