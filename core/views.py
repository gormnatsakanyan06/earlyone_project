from django.http import JsonResponse ,HttpResponse
from .models import *

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