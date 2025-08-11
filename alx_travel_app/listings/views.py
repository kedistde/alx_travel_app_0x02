import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
class InitiatePaymentView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        booking_reference = request.data.get("booking_reference")

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": request.data.get("email"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "tx_ref": booking_reference,
            "callback_url": "http://yourdomain.com/api/verify-payment/"
        }

        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        data = response.json()

      

        if response.status_code == 200 and data.get("status") == "success":
            transaction_id = data["data"]["tx_ref"]
            Payment.objects.create(
                booking_reference=booking_reference,
                transaction_id=transaction_id,
                amount=amount,
                status="Pending"
            )
            return Response({"checkout_url": data["data"]["checkout_url"]})
        return Response({"error": "Payment initiation failed"}, status=400)

       class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{tx_ref}", headers=headers)
        data = response.json()

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if data.get("status") == "success" and data["data"]["status"] == "success":
            payment.status = "Completed"
            payment.save()
            return Response({"message": "Payment completed"})
        else:
            payment.status = "Failed"
            payment.save()
            return Response({"message": "Payment failed"}, status=400) 
