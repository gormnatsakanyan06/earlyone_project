from django.http import JsonResponse ,HttpResponse
from .models import *


#QR
import qrcode
from io import BytesIO
import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response


def generate_qr_base64(data):
    qr = qrcode.make(data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    img_bytes = buffer.getvalue()
    base64_str = base64.b64encode(img_bytes).decode()

    return base64_str



@api_view(['GET', 'POST'])
def create_qr(request):
    data = request.data.get("text") or request.GET.get("text")

    if not data:
        return Response({"error": "No text provided"}, status=400)

    qr_base64 = generate_qr_base64(data)

    return Response({
        "qr_code": qr_base64
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