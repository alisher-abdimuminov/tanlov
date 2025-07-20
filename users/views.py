from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import User, Criteria, Application


@login_required(login_url="login")
def home_view(request: HttpRequest):
    context = {}

    criterias = Criteria.objects.all()

    for criteria in criterias:
        criteria.applications = criteria.applications(user=request.user)

    context["criterias"] = criterias

    if request.method == "POST":
        for file in request.FILES:
            criteria = Criteria.objects.filter(pk=file)
            file = request.FILES.get(file)
            if criteria.exists():
                criteria = criteria.first()
                application = Application.objects.filter(criteria=criteria, author=request.user)
                if application.exists():
                    application = application.first()
                    if application.status == "approved" or application.status == "waiting":
                        continue
                    else:
                        application.file = file
                        application.status = "wating"
                        application.save()
                else:
                    Application.objects.create(
                        criteria=criteria,
                        author=request.user,
                        file=file,
                        status="waiting"
                    )

    return render(request=request, template_name="index.html", context=context)


def login_view(request: HttpRequest):
    # if user is logged in redirect to home page
    if request.user.is_authenticated:
        return redirect("home")
    
    context = {}
    if request.method == "POST":
        phone = request.POST.get("phone", "")
        password = request.POST.get("password", "")

        user = User.objects.filter(phone=phone)

        if not user.exists():
            messages.add_message(request=request, level=messages.constants.ERROR, message="Telefon raqami topilmadi")
            return render(request=request, template_name="login.html", context=context)
        
        user = user.first()

        if not user.check_password(raw_password=password):
            messages.add_message(request=request, level=messages.constants.ERROR, message="Parol mos kelmadi")
            return render(request=request, template_name="login.html", context=context)
        
        login(request=request, user=user)
        messages.add_message(request=request, level=messages.constants.SUCCESS, message="Xush kelibsiz")
        return redirect("home")

    return render(request=request, template_name="login.html", context=context)


def signup_view(request: HttpRequest):
     # if user is logged in redirect to home page
    if request.user.is_authenticated:
        return redirect("home")
    
    context = {}
    if request.method == "POST":
        phone = request.POST.get("phone", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password", "")

        user = User.objects.filter(phone=phone)

        if user.exists():
            messages.add_message(request=request, level=messages.constants.ERROR, message="Telefon raqami allaqachon ro'yxatdan o'tgan")
            return render(request=request, template_name="signup.html", context=context)
        
        user = User.objects.create(
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(raw_password=password)
        user.save()

        return redirect("login")

    return render(request=request, template_name="signup.html", context=context)

