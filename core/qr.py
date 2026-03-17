from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files import File
from io import BytesIO
import qrcode
import uuid

from .models import QRCode
def create_qr_and_save(text):
    # check if already exists
    if QRCode.objects.filter(text=text).exists():
        return QRCode.objects.get(text=text)

    qr = qrcode.make(text)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    

    file_name = f"{uuid.uuid4()}.png"
    file = File(buffer, name=file_name)

    qr_instance = QRCode.objects.create(
        text=text,
        image=file
    )

    return qr_instance





@api_view(['POST'])
def create_qr(request):
    text = request.data.get("text")

    if not text:
        return Response({"error": "No text provided"}, status=400)

    qr = create_qr_and_save(text)

    return Response({
        "id": qr.id,
        "text": qr.text,
        "image_url": qr.image.url
    })



@api_view(['GET'])
def download_qr(request, qr_id):
    try:
        qr = QRCode.objects.get(id=qr_id)
    except QRCode.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    response = HttpResponse(qr.image.open(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr_{qr_id}.png"'

    return response