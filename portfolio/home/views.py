from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import ContactMessage

# Create your views here.

def home(request):
    # return render(request, 'home.html')
    return HttpResponse("Hello, World!")

def homepage(request):
    # return HttpResponse("Welcome to the homepage!")
    content = {
        'title': 'My Website - Kaushal Karn',
        'message': 'Welcome to the Landing Page!',
    }
    return render(request, 'home/landing_page.html', content)

def about(request):
    return render(request, 'home/about_page.html')

def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not (name and email and message):
            messages.error(request, 'All fields are required. Please fill in the form completely.')
            return render(request, 'home/contact_page.html')

        # 1. Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # 2. Send notification email to site owner
        subject = f'[Portfolio] New message from {name}'
        body = (
            f'You received a new contact form submission.\n\n'
            f'Name:    {name}\n'
            f'Email:   {email}\n'
            f'Message:\n{message}\n\n'
            f'---\nSent via the portfolio contact form.'
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.RECIPIENT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, f"Thank you, {name}! Your message has been sent. I'll get back to you soon. ✉️")
        except Exception as exc:
            # Message still saved to DB; notify user of email issue
            messages.warning(
                request,
                'Your message was received and saved, but there was a problem sending the email notification. '
                'I will still see it — thank you!'
            )

        return redirect('contact')

    return render(request, 'home/contact_page.html')

def blog(request):
    return render(request, 'home/blog_page.html')

def experience(request):
    return render(request, 'home/experience.html')

def certification(request):
    return render(request, 'home/certification.html')
