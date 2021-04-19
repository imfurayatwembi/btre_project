from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
# from django.contrib.auth import is_authenticated

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id 
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have arleady made an enquiry for this listing')
                return redirect('/listings/'+listing_id)
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone = phone, user_id=user_id)
        contact.save()
        send_mail(
        'Propety Listing enquiry',
        'There has been an enquiry for '+ listing +'.Sign into the main admin pannel for more info',
        'gentilpacifique123@gmail.com',
        [realtor_email, 'gentilpacifique@gmail.com'],
        fail_silently=False
        )
    
    messages.success(request, 'Your request has been submitted, a realtor will have back to you')
    return redirect('/listings/'+listing_id)
    #  Send email
   
   