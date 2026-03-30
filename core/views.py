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

def telecom(request):
    return render(request, 'core/telecom.html')  

def utilitie(request):
    return render(request, 'core/utilitie.html')


BANK_DATA = {
    'ameria': {
        'name': 'Ամերիաբանկ',
        'logo': 'ameria.png',
        'branches': [
            {'name': '«Կամար» Մասնաճյուղ', 'address': 'Վ. Սարգսյան 2, Երևան'},
            {'name': '«Սայաթ-Նովա»', 'address': 'Սայաթ-Նովա պողոտա 8, Երևան'},
            {'name': '«Քոչար»', 'address': 'Հ․ Քոչար 21, Երևան'},
            {'name': '«Արշակունյաց»', 'address': 'Արշակունյաց պողոտա 34/3, Երևան'}
        ]
    },
    'ineco': {
        'name': 'Ինեկոբանկ',
        'logo': 'ineco.png',
        'branches': [
            {'name': '«Գլխամասային գրասենյակ»', 'address': 'Թումանյան 17, Երևան'},
            {'name': '«Կոմիտաս»', 'address': 'Կոմիտաս պողոտա 38, Երևան'},
            {'name': '«Նոր Նորք»', 'address': 'Գայի պողոտա 23/6, Երևան'},
            {'name': '«Մալաթիա»', 'address': 'Ռաֆֆու փողոց 39/4, Երևան'}
        ]
    },
    'acba': {
        'name': 'Ակբա բանկ',
        'logo': 'acba.png',
        'branches': [
            {'name': '«Կենտրոն» Մասնաճյուղ', 'address': 'Ամիրյան 1, Երևան'},
            {'name': '«Արարատյան»', 'address': 'Արշակունյաց 1, Երևան'},
            {'name': '«Զեյթուն»', 'address': 'Պ․ Սևակի 8/2, Երևան'},
            {'name': '«Թամանյան»', 'address': 'Ազատության պող․ 24, Երևան'},
        ]
    },
    'evoca': {
        'name': 'Էվոկաբանկ',
        'logo': 'evoca.png',
        'branches': [
            {'name': '«Գլխամասային գրասենյակ»', 'address': 'Հանրապետության 44/2, Երևան'},
            {'name': '«Կասկադ»', 'address': 'Թումանյան 1/3, Երևան'},
            {'name': '«Մալաթիա»', 'address': 'Զորավար Անդրանիկ 40, Երևան'},
            {'name': '«Դավթաշեն»', 'address': 'Դավթաշեն 4-րդ թաղ․ 11/1, Երևան'},
        ]
    }
}

def bank_branches(request, service_slug): 
    data = BANK_DATA.get(service_slug)
    if not data:
        return render(request, '404.html')
        
    context = {
        'branches': data.get('branches'),
        'service_slug': service_slug, # Handing this to the template for the next link
        'name': data.get('name'),
        'logo': data.get('logo'),
    }
    return render(request, 'core/bank_branches.html', context)

def bank_actions(request, service_slug, branch_name):
    data = BANK_DATA.get(service_slug)
    if not data:
        return render(request, '404.html')

    context = {
        'service_slug': service_slug, # Matches URL <str:service_slug>
        'branch_name': branch_name,   # Matches URL <str:branch_name>
        'name': data.get('name'),
        'logo': data.get('logo'),
    }
    return render(request, 'core/bank_actions.html', context)
    


GOVERNMENT_DATA = {
    'ngn': {
        'name': 'Հաշվառման-քննական ստորաբաժանումներ',
        'logo': 'ngn.png',
        'branches': [
            {'name': 'Երևանի ՀՔԲ (Գաջեգործների)', 'address': 'Գաջեգործների փողոց 76, Երևան'},
        ],
        'actions': [
            {'name': 'Տեսական քննություն', 'slug': 'theory', 'icon': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'},
            {'name': 'Գործնական քննություն', 'slug': 'practical', 'icon': 'M13 10V3L4 14h7v7l9-11h-7z'},
            {'name': 'Վկայականի փոխանակում', 'slug': 'exchange', 'icon': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'},
        ]
    },
    'arxiv': {
        'name': 'Հայաստանի ազգային արխիվ',
        'logo': 'arxiv.png',
        'branches': [
            {'name': 'Գլխամասային մասնաշենք', 'address': 'Հրաչյա Քոչար 5, Երևան'},
        ],
        'actions': [
            {'name': 'Դիմումի հանձնում', 'slug': 'submit', 'icon': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4'},
            {'name': 'Դիմումի ստացում', 'slug': 'receive', 'icon': 'M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4'},
        ]
    },
    'kadastr': {
        'name': 'Կադաստրի կոմիտե',
        'logo': 'kadastr.png',
        'branches': [
            {'name': 'Արաբկիր', 'address': 'Կոմիտասի պող․ 35/2'},
            {'name': 'Կենտրոն', 'address': 'Փ․ Բուզանդ 1/3'},
            {'name': 'Շենգավիթ', 'address': 'Մանանդյան 33'},
        ], 
        'actions': [
            {'name': 'Դիմումի հանձնում', 'slug': 'submit', 'icon': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4'},
            {'name': 'Ստանալ փաստաթուղթ', 'slug': 'receive', 'icon': 'M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4'},
        ]
    }
}

def government_branches(request, service_slug):
    data = GOVERNMENT_DATA.get(service_slug.lower())
    if not data:
        return render(request, '404.html')
    context = {
        'name': data['name'],
        'logo': data['logo'],
        'branches': data['branches'],
        'service_slug': service_slug.lower(),
    }
    return render(request, 'core/government_branches.html', context)


def government_actions(request, service_slug, branch_name):
    service = GOVERNMENT_DATA.get(service_slug)
    if not service:
        return render(request, '404.html')
    context = {
        'logo': service['logo'],
        'actions': service['actions'],
        'service_slug': service_slug,
        'branch_name': branch_name,
    }
    return render(request, 'core/government_actions.html', context)



TELECOM_DATA = {
    'team': {
        'name': 'Թիմ Տելեկոմ',
        'logo': 'team.png',
        'branches': [
            {'name': 'Ազատության', 'address': 'Ազատության պող․ 24/1, Երևան'},
            {'name': 'Աբովյան', 'address': 'Աբովյան փող․ 21, Երևան'},
            {'name': 'Մաշտոց', 'address': 'Մաշտոցի պող․ 48, Երևան'},
        ]
    },
    'viva': {
        'name': 'Վիվա',
        'logo': 'viva.png',
        'branches': [
            {'name': 'Ամիրյան', 'address': 'Ամիրյան փող․ 3, Երևան'},
            {'name': 'Հյուսիսային պողոտա', 'address': 'Հյուսիսային պող․ 6/14, Երևան'},
            {'name': 'Կոմիտաս', 'address': 'Կոմիտասի պող․ 28, Երևան'},
        ]
    },
    'ucom': {
        'name': 'Յուքոմ',
        'logo': 'ucom.png',
        'branches': [
            {'name': 'Հյուսիսային պողոտա', 'address': 'Հյուսիսային պող․ 1, Երևան'},
            {'name': 'Սայաթ-Նովա', 'address': 'Սայաթ-Նովա պող․ 19, Երևան'},
            {'name': 'Մալաթիա', 'address': 'Րաֆֆու փող․ 19, Երևան'},
        ]
    }
}


TELECOM_ACTIONS = [
    {'name': 'Դառնալ բաժանորդ', 'slug': 'new-subscriber', 'icon': 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z'},
    {'name': 'Վճարումներ', 'slug': 'payments', 'icon': 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z'},
    {'name': 'Սարքավորումների ձեռքբերում', 'slug': 'devices', 'icon': 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z'},
    {'name': 'Խորհրդատվություն', 'slug': 'support', 'icon': 'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0z'},
]

def telecom_branches(request, service_slug):
    data = TELECOM_DATA.get(service_slug.lower())
    if not data: return render(request, '404.html')
    
    context = {
        'name': data['name'],
        'logo': data['logo'],
        'branches': data['branches'],
        'service_slug': service_slug.lower(),
    }
    return render(request, 'core/telecom_branches.html', context)

def telecom_actions(request, service_slug, branch_name):
    data = TELECOM_DATA.get(service_slug.lower())
    if not data: return render(request, '404.html')

    context = {
        'name': data['name'],
        'logo': data['logo'],
        'actions': TELECOM_ACTIONS,
        'service_slug': service_slug,
        'branch_name': branch_name,
    }
    return render(request, 'core/telecom_actions.html', context)


UTILITY_DATA = {
    'gazprom': {
        'name': 'Գազպրոմ Արմենիա',
        'logo': 'gazprom.png',
        'branches': [
            {'name': 'Երևանի ԳԳՄ', 'address': 'Թբիլիսյան խճուղի 43'},
            {'name': 'Արաբկիրի մասնաճյուղ', 'address': 'Կոմիտաս 49/4'},
        ],
        'actions': [
            {'name': 'Գազի սարքի փոխարինում', 'slug': 'gas-device-replacement', 'icon': 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'},
            {'name': 'Գազի հաշվիչի կապարակնքում', 'slug': 'gas-meter-sealing', 'icon': 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'},
        ]
    },
    'hec': {
        'name': 'ՀԷՑ',
        'logo': 'hec.png',
        'branches': [
            {'name': '«Գեղամա» մասնաճյուղ', 'address': 'Սայաթ-Նովա 12'},
        ],
        'actions': [
            {'name': 'Հաշվիչի փոխարինում / տեղակայում', 'slug': 'meter-replacement', 'icon': 'M13 10V3L4 14h7v7l9-11h-7z'},
            {'name': 'Հզորության փոխարինում', 'slug': 'power-change', 'icon': 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'},
        ]
    },
    'veolia': {
        'name': 'Վեոլիա Ջուր',
        'logo': 'veolia.png',
        'branches': [
            {'name': 'Կենտրոն սպասարկման գրասենյակ', 'address': 'Աբովյան 66'},
        ],
        'actions': [
            {'name': 'Ջրաչափի փոխարինում / տեղադրում', 'slug': 'water-meter-replacement', 'icon': 'M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z'},
            {'name': 'Ավարտական ակտի հաստատում', 'slug': 'final-act', 'icon': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'},
        ]
    }
}

def utility_branches(request, service_slug):
    data = UTILITY_DATA.get(service_slug.lower())
    if not data:
        return render(request, '404.html')
    
    context = {
        'name': data['name'],
        'logo': data['logo'],
        'branches': data['branches'],
        'service_slug': service_slug.lower(),
    }
    return render(request, 'core/utilitie_branches.html', context)

def utility_actions(request, service_slug, branch_name):
    data = UTILITY_DATA.get(service_slug.lower())
    if not data:
        return render(request, '404.html')

    context = {
        'name': data['name'],
        'logo': data['logo'],
        'actions': data['actions'], # Now coming from the same dict
        'service_slug': service_slug,
        'branch_name': branch_name,
    }
    return render(request, 'core/utilitie_actions.html', context)



def datetime_selection(request, service_slug, branch_name, action_slug):
    data = BANK_DATA.get(service_slug) or GOVERNMENT_DATA.get(service_slug) or TELECOM_DATA.get(service_slug) or UTILITY_DATA.get(service_slug)
    if not data:
        return render(request, '404.html')

    context = {
        'name': data.get('name'),
        'logo': data.get('logo'),
        'service_slug': service_slug,
        'branch_name': branch_name,
        'action_slug': action_slug,
    }

    return render(request, 'core/datetime.html', context)
def generate_ticket(request, service_slug, branch_name, action_slug, date, time):
    # Try fetching from Finance first, then Government
    data = BANK_DATA.get(service_slug) or GOVERNMENT_DATA.get(service_slug) or TELECOM_DATA.get(service_slug) or UTILITY_DATA.get(service_slug)
    
    if not data:
        return render(request, '404.html')
    
    context = {
        'name': data.get('name'),    
        'logo': data.get('logo'),    
        'branch_name': branch_name,
        'service': action_slug,           
        'date': date,
        'time': time,
        'ticket_number': "A-102", 
    }
    return render(request, 'core/ticket.html', context)

