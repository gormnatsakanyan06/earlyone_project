from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files import File
from io import BytesIO
import qrcode
import uuid

from .models import Appointment
def create_qr_and_save(verif_code):
    # check if already exists
    if Appointment.objects.filter(verif_code=verif_code).exists():
        return Appointment.objects.get(verif_code=verif_code)

    qr = qrcode.make(verif_code)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    

    file_name = f"{uuid.uuid4()}.png"
    file = File(buffer, name=file_name)

    qr_instance = Appointment.objects.create(
        verif_code=verif_code,
        image=file
    )

    return qr_instance





@api_view(['POST'])
def create_qr(request):

    verif_code = request.data.get("verif_code")


    if not verif_code:
        return Response({"error": "No verif_code provided"}, status=400)

    qr = create_qr_and_save(verif_code)

    return Response({
        "id": qr.id,
        "verif_code": qr.verif_code,
        "image_url": qr.image.url
    })



@api_view(['GET'])
def download_qr(request, qr_id):
    try:
        qr = Appointment.objects.get(id=qr_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    response = HttpResponse(qr.image.open(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr_{qr_id}.png"'

    return response


