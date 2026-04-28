from django.http import JsonResponse ,HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
#QR
import qrcode
from io import BytesIO
import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404
from .models import Category, Provider, Branch, Action
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


from .qr import create_qr_and_save   # or wherever you saved it

def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    providers = category.providers.all()
    return render(request, 'core/unified/category_detail.html', {
        'category': category,
        'providers': providers,
    })

def branch_list_view(request, category_slug, provider_slug):
    provider = get_object_or_404(
        Provider,
        slug=provider_slug,
        category__slug=category_slug  # 🔥 important filter
    )
    branches = provider.branches.all()

    return render(request, 'core/unified/branch_list.html', {
        'provider': provider,
        'branches': branches
    })

def action_list_view(request, category_slug, provider_slug, branch_slug):
    category = get_object_or_404(Category, slug=category_slug)

    provider = get_object_or_404(
        Provider,
        slug=provider_slug,
        category=category
    )

    branch = get_object_or_404(
        Branch,
        slug=branch_slug,
        provider=provider
    )

    actions = provider.actions.all()

    return render(request, 'core/unified/action_list.html', {
        'category': category,   # 🔥 ADD THIS
        'provider': provider,
        'branch': branch,
        'actions': actions
    })

@login_required # This redirects them to login if they aren't authenticated
def appointment_landing_view(request):
    categories = Category.objects.all()
    return render(request, 'core/unified/appointment.html', {
        'categories': categories
    })


# def datetime_view(request):
#     return render(request, 'core/unified/datetime.html')

@csrf_exempt  # for now (later we can secure it)
@api_view(['POST'])
def create_appointment(request):
    data = request.data

    try:
        category = Category.objects.get(slug=data['category'])
        provider = Provider.objects.get(slug=data['provider'], category=category)
        branch = Branch.objects.get(slug=data['branch'], provider=provider)
        action = Action.objects.get(id=data['action'], provider=provider)

        scheduled_at = datetime.strptime(
            f"{data['date']} {data['time']}",
            "%Y-%m-%d %H:%M"
        )

        content_type = ContentType.objects.get_for_model(Action)

        appointment = Appointment.objects.create(
            full_name=request.user.username if request.user.is_authenticated else "Guest",
            phone_number="N/A",
            category=category,
            branch=branch,
            content_type=content_type,
            object_id=action.id,
            scheduled_at=scheduled_at
        )

        return Response({
            "success": True,
            "appointment_id": appointment.id
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=400)
    
def ticket_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'core/unified/ticket.html', {
        'appointment': appointment
    })

import base64
import json

def decode_hash(hash_value):
    padded = hash_value + "=="
    decoded = base64.urlsafe_b64decode(padded)
    return json.loads(decoded)




def datetime_view(request, category_slug, provider_slug, branch_slug, hash):
    data = decode_hash(hash)

    category = Category.objects.get(slug=category_slug)

    provider = Provider.objects.get(
        slug=provider_slug,
        category=category
    )

    branch = Branch.objects.get(
        slug=branch_slug,
        provider=provider   # 🔥 THIS FIXES DUPLICATES
    )

    return render(request, "core/unified/datetime.html", {
        "data": data,
        "category": category,
        "provider": provider,
        "branch": branch,
    })

#QR
#QR
#QR


@csrf_exempt
@api_view(['POST'])
def create_appointment(request):
    data = request.data

    try:
        category = Category.objects.get(slug=data['category'])
        provider = Provider.objects.get(slug=data['provider'], category=category)
        branch = Branch.objects.get(slug=data['branch'], provider=provider)
        action = Action.objects.get(id=data['action'], provider=provider)

        scheduled_at = datetime.strptime(
            f"{data['date']} {data['time']}",
            "%Y-%m-%d %H:%M"
        )

        content_type = ContentType.objects.get_for_model(Action)

        appointment = Appointment.objects.create(
            full_name=request.user.username if request.user.is_authenticated else "Guest",
            phone_number="N/A",
            category=category,
            branch=branch,
            content_type=content_type,
            object_id=action.id,
            scheduled_at=scheduled_at
        )

        # ✅ CREATE QR HERE
        qr_text = str(appointment.verification_code)

        qr = create_qr_and_save(qr_text)

        appointment.qr_code = qr
        appointment.save()

        return Response({
            "success": True,
            "appointment_id": appointment.id
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=400)


