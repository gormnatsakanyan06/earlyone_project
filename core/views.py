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
    provider = get_object_or_404(
        Provider,
        slug=provider_slug,
        category__slug=category_slug
    )

    branch = get_object_or_404(
        Branch,
        slug=branch_slug,
        provider=provider
    )

    actions = provider.actions.all()

    return render(request, 'core/unified/action_list.html', {
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

# from .qr import create_qr_and_save

# @api_view(['POST'])
# def create_appointment(request):
#     full_name = request.data.get('full_name')
#     phone = request.data.get('phone')
#     category = request.data.get('category')
#     action_id = request.data.get('action_id')
#     scheduled_time = request.data.get('scheduled_time')

#     model_map = {
#         'finance': BankAction,
#         'government': GovernmentAction,
#         'telecom': TelecomAction,
#         'utility': ServiceAction,
#     }

#     selected_model = model_map.get(category)

#     if not selected_model:
#         return Response({"error": "Invalid category"}, status=400)

#     content_type = ContentType.objects.get_for_model(selected_model)
#     appointment = Appointment.objects.create(
#         full_name=full_name,
#         phone_number=phone,
#         category=category,
#         content_type=content_type,
#         object_id=action_id,
#         scheduled_at=scheduled_time
#     )

#     qr = create_qr_and_save(str(appointment.verification_code))
#     appointment.qr_code = qr
#     appointment.save()

#     return Response({
#         "appointment_id": appointment.id,
#         "verification_code": str(appointment.verification_code),
#         "qr_image": qr.image.url
#     })





