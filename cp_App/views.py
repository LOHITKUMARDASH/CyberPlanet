from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login,logout
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.utils.html import escape
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def sanitizedata(data):
    return escape(data)

def login(request):
    return render(request, "login.html")

def login_view(request):
    if request.method == "POST":
        e_mail = request.POST.get('email')
        pwd = request.POST.get('password')
        user = authenticate(request, email=e_mail, password=pwd)
        if user is not None:
            if user.role == 'ADMIN':
                auth_login(request, user)
                return redirect('index')
            elif user.role == 'STAFF':
                auth_login(request, user)
                return redirect('assign')
            else:
                return render(request, "login.html")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required
def index(request):
    context = {}
    context["currentPage"] = "index"
    context["customer"] = customer.objects.all()
    context["users"] = NewUser.objects.exclude(user_name__in=["super", "Lohit"])
    try:
        if request.method == "POST":
            c_name = sanitizedata(request.POST.get('name'))
            email = sanitizedata(request.POST.get('email'))
            mobile = sanitizedata(request.POST.get('mobile'))
            t_asset = sanitizedata(request.POST.get('t_asset'))
            address = sanitizedata(request.POST.get('address'))
            assign_to = sanitizedata(request.POST.get('assign_to'))
            warranty = sanitizedata(request.POST.get('warranty'))
            problem = sanitizedata(request.POST.get('problem'))
            received_date = sanitizedata(request.POST.get('received_date'))
            estimated_date = sanitizedata(request.POST.get('estimated_date'))
            if request.FILES and request.FILES.get('image'):
                prof_pic = request.FILES['image']
                fs = FileSystemStorage()
                file = fs.save(prof_pic.name, prof_pic)
                fileurl = fs.url(file)
                customer(name=c_name, mobile=mobile, email=email, assets_type=t_asset,
                         assign=assign_to, warranty=warranty, problem=problem, received_date=received_date, estimated_date=estimated_date,
                         address=address, status="Assign", referance_image=fileurl).save()
            else:
                customer(name=c_name, mobile=mobile, email=email, assets_type=t_asset,
                         assign=assign_to, warranty=warranty, problem=problem, received_date=received_date,
                         estimated_date=estimated_date,
                         address=address, status="Assign").save()
    except Exception as e:
        print(e)
    return render(request, "index.html", context)

@login_required
def edit_customer(request):
    context = {}
    context["currentPage"] = "index"
    context["customer"] = customer.objects.all()
    try:
        if request.method == "POST":
            ids = sanitizedata(request.POST.get('edit_id'))
            c_name = sanitizedata(request.POST.get('edit_name'))
            email = sanitizedata(request.POST.get('edit_email'))
            mobile = sanitizedata(request.POST.get('edit_mobile'))
            t_asset = sanitizedata(request.POST.get('edit_t_asset'))
            assign_to = sanitizedata(request.POST.get('edit_assign_to'))
            warranty = sanitizedata(request.POST.get('edit_warranty'))
            problem = sanitizedata(request.POST.get('edit_problem'))
            received_date = sanitizedata(request.POST.get('edit_received_date'))
            estimated_date = sanitizedata(request.POST.get('edit_estimated_date'))
            status = sanitizedata(request.POST.get('edit_status'))
            customer.objects.filter(id=ids).update(name=c_name, mobile=mobile, email=email, assets_type=t_asset,
                     assign=assign_to, warranty=warranty, problem=problem, received_date=received_date,
                     estimated_date=estimated_date,
                     status=status)
    except Exception as e:
        print(e)
    return render(request, "index.html", context)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

@login_required
def assign(request):
    context = {}
    context["currentPage"] = "assign"
    context["customer"] = customer.objects.all()
    return render(request, "assign.html", context)

@login_required
def edit_assign(request):
    context = {}
    context["currentPage"] = "assign"
    context["customer"] = customer.objects.all()
    try:
        if request.method == "POST":
            ids = sanitizedata(request.POST.get('edit_id'))
            problem = sanitizedata(request.POST.get('edit_problem'))
            spare = sanitizedata(request.POST.get('Spare'))
            estimate_cost = sanitizedata(request.POST.get('estimate_cost'))
            status = sanitizedata(request.POST.get('edit_status'))
            customer.objects.filter(id=ids).update(problem=problem,spare=spare,estimated_cost=estimate_cost, status=status)

            subject = "Estimated Report"
            username = customer.objects.get(id=ids).name
            recipient_list = [customer.objects.get(id=ids).email]
            estimated_completion_date = customer.objects.get(id=ids).estimated_date
            assets = customer.objects.get(id=ids).assets_type
            cc_list = ['lohitkumardash1996@gmail.com','cyberplanet.bpd@gmail.com']

            message = (
                    f"Dear {username},\n\n"
                    f"We would like to inform you about the status of your {assets} repair:\n\n"
                    f"Problem Description: {problem}\n"
                    f"Estimated Cost: {estimate_cost}\-\n"
                    f"Spare Parts Consume: {spare}\n"
                    f"Estimated Completion Date: {estimated_completion_date}\n\n"
                    f"Please feel free to contact us if you have any further questions.\n\n"
                    f"Best regards,\n"
                    f"CYBER PLANTE \n"
                    f"Your Laptop Repair Service Team"
                )
            if customer.objects.get(id=ids).mail_status != "1":
                print("sent")
                email = EmailMessage(subject, message, "CYBER PLANTE" + "<" + settings.EMAIL_HOST_USER + ">", recipient_list, cc=cc_list)
                email.send(fail_silently=False)
                customer.objects.filter(id=ids).update(mail_status= 1)


    except Exception as e:
        print(e)
    return render(request, "assign.html", context)

@login_required
def add_user(request):
    context = {}
    context["currentPage"] = "add_user"
    users_to_exclude = ["super@gmail.com", "admin@gmail.com"]
    context["user_data"] = NewUser.objects.exclude(email__in=users_to_exclude)
    if request.method == "POST":
        try:
            name = sanitizedata(request.POST.get('name'))
            mobile = sanitizedata(request.POST.get('mobile'))
            email = sanitizedata(request.POST.get('email'))
            password = "cp@123"
            user = NewUser(user_name=name, email=email, first_name=name,
                           mobile=mobile, is_active=True, role='STAFF')
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
    return render(request, "add_user.html", context)

@login_required
def edit_user(request):
    context = {}
    context["currentPage"] = "add_user"
    users_to_exclude = ["super@gmail.com", "admin@gmail.com"]
    context["user_data"] = NewUser.objects.exclude(email__in=users_to_exclude)
    if request.method == "POST":
        try:
            ids = sanitizedata(request.POST.get('edit_id'))
            name = sanitizedata(request.POST.get('edit_name'))
            mobile = sanitizedata(request.POST.get('edit_mobile'))
            email = sanitizedata(request.POST.get('edit_email'))
            user = NewUser.objects.filter(id=ids).update(user_name=name, email=email, first_name=name,mobile=mobile)
        except Exception as e:
            print(e)
    return render(request, "add_user.html", context)