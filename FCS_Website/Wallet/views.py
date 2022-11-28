from django.shortcuts import HttpResponse,render
from django.views.generic.list import ListView
YOUR_DOMAIN="http://127.0.0.1:8000/"

# Create your views here.
import stripe
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import *

from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_PRIVATE_KEY
from Wallet.models import Transactions,approve
from django.http import JsonResponse
from Common.helper import *
i




def create_checkout_session (request):
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()
    pk = request.session['transaction']
    ID = request.session["claimID"]

    print(ID)
    if( Transactions.objects.filter(ID=pk).exists()==False):
        attributes = {"title":"Invalid Payment Session",
                        "heading": "Illegal route for payment ",
                    "redirect":"login"}
        return render (request, "Common/Templates/message.html", attributes)
    transID = Transactions.objects.get(ID=pk)
    if(transID==None):
        attributes = {"title":"Invalid Payment Session",
                        "heading": "Illegal route for payment ",
                    "redirect":"login"}
        return render (request, "Common/Templates/message.html", attributes)


    payload = transID.Amount
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],

    line_items=[{
    'price_data': {
     'currency': 'inr',
     'product_data': {
     'name': 'Paying for website',
     },
     'unit_amount':payload*100,

     },
    'quantity': 1,

     }],
    mode='payment',

    metadata = {'transid': pk , 'claimID':ID},
    success_url=YOUR_DOMAIN + "success",
    cancel_url=YOUR_DOMAIN +'failure',
    )

    return JsonResponse({'id': session.id})
def payment(request ):
 pk = request.session['transaction']
 if( Transactions.objects.filter(ID=pk).exists()==False):
        attributes = {"title":"Invalid Payment Session",
                        "heading": "Illegal route for payment ",
                    "redirect":"login"}
        return render (request, "Common/Templates/message.html", attributes)

 trans = Transactions.objects.get(ID=pk)
 if(trans.Success == True):
    attributes = {"title":"Invalid Payment Session",
                        "heading": "Illegal route for payment ",
                    "redirect":"login"}
    return render (request, "Common/Templates/message.html", attributes)

 user = request.session["username"]

 if(trans.Sender.username != user):
     attributes = {"title":"Invalid Payment Session",
                        "heading": "Illegal route for payment ",
                    "redirect":"login"}
     return render (request, "Common/Templates/message.html", attributes)


 return render(request,'Wallet/Templates/checkout.html' )


def success(request):

    attributes = {"title":"Payment Successfull",
                    "heading": "Your payment was successfull",
                    "redirect":"/login"}
    return render (request, "Common/Templates/message.html", attributes)
def failure(request):
    attributes = {"title":"Payment Request Failed",
                    "heading": "Could not process payment due to some invalid entries.",
                    "redirect":"/login"}
    return render (request, "Common/Templates/message.html", attributes)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']
        id = session['metadata']['transid']
        claimID = session['metadata']['claimID']
        approve(claimID)
        transID = Transactions.objects.filter(ID=id)
        transID.update(Success=True)


    return HttpResponse(status=200)

