from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import User, Application


@login_required(login_url="login")
def home_view(request: HttpRequest):
    context = {}

    # Joriy foydalanuvchiga tegishli arizani olish
    application = Application.objects.filter(author=request.user).first()
    context["application"] = application

    if request.method == "POST":
        # Agar foydalanuvchi allaqachon ariza topshirgan bo'lsa, qayta topshira olmaydi
        if application:
            messages.error(request, "Siz allaqachon ariza topshirgansiz!")
            return redirect("home")

        # Formadan ma'lumotlarni olish
        fio = request.POST.get("fio", "")
        phone = request.POST.get("phone", "")

        # Fayllarni olish
        passport = request.FILES.get("passport")
        diploma = request.FILES.get("diploma")
        certificate = request.FILES.get("certificate")  # Bu ixtiyoriy bo'lishi mumkin

        # Majburiy maydonlar to'ldirilganini tekshirish
        if not (fio and phone and passport and diploma):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring va fayllarni yuklang.")
            return render(request, "index.html", context)

        # Yangi ariza yaratish
        Application.objects.create(
            author=request.user,
            fio=fio,
            phone=phone,
            passport=passport,
            diploma=diploma,
            certificate=certificate
        )

        messages.success(request, "Arizangiz muvaffaqiyatli qabul qilindi!")
        return redirect("home")

    return render(request=request, template_name="index.html", context=context)


def login_view(request: HttpRequest):
    # Agar foydalanuvchi tizimga kirgan bo'lsa, bosh sahifaga yo'naltirish
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        phone = request.POST.get("phone", "")
        password = request.POST.get("password", "")

        user = User.objects.filter(phone=phone)

        if not user.exists():
            messages.error(request, "Telefon raqami topilmadi")
            return render(request=request, template_name="login.html", context=context)

        user = user.first()

        if not user.check_password(raw_password=password):
            messages.error(request, "Parol mos kelmadi")
            return render(request=request, template_name="login.html", context=context)

        login(request=request, user=user)
        messages.success(request, "Xush kelibsiz")
        return redirect("home")

    return render(request=request, template_name="login.html", context=context)


def signup_view(request: HttpRequest):
    # Agar foydalanuvchi tizimga kirgan bo'lsa, bosh sahifaga yo'naltirish
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
            messages.error(request, "Telefon raqami allaqachon ro'yxatdan o'tgan")
            return render(request=request, template_name="signup.html", context=context)

        user = User.objects.create(
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(raw_password=password)
        user.save()

        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz. Tizimga kiring.")
        return redirect("login")

    return render(request=request, template_name="signup.html", context=context)
