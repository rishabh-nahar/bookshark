from django.shortcuts import redirect, render
from  django.contrib import messages    
from backend.models import user_details, listing_books
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random

def home(request):
    return render(request,'pages/home/index.html')

def sell(request):
    if request.method == 'POST':
        book_name = request.POST['book_name']
        book_author = request.POST['book_author']
        book_publisher = request.POST['book_publisher']
        book_year_edition = request.POST['book_year_edition']
        book_selling_price = request.POST['book_selling_price']
        book_description = request.POST['book_description']

        list_book_details = listing_books.objects.create(
            book_name=book_name, 
            book_author=book_author,
            book_publisher=book_publisher,
            book_year_edition=book_year_edition,
            book_selling_price = book_selling_price,
            book_description = book_description,
            book_seller_id = user_details.objects.get(username = request.session.get("username")).unique_id
            )
        list_book_details.save()

    return render(request,'pages/sell/sell.html')

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        validate_userid = user_details.objects.filter(username__exact = username)

        count_users = validate_userid.count()
        for userids in validate_userid:
            user_unique_id = userids.unique_id
            if count_users >= 1:
                request.session['username'] = username
                request.session['user_unique_id'] = user_unique_id
                if password == userids.password:
                    return redirect("/",args={'username':username,'user_unique_id':user_unique_id})
                else:
                    print("Wrong password")

    return render(request,'pages/login/login.html')



def registeration_page(request):
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        gender = request.POST['gender'] 
        mail = request.POST['mail'] 
        phone = request.POST['phone'] 
        username = request.POST['username'] 
        password = request.POST['password'] 
        print(username)

        exists_username = user_details.objects.filter(username = username).count()
        exists_email = user_details.objects.filter(mail = mail).count()

        if exists_username > 0:
            print("username error")
            messages.error(request,"Username Exist")
            
        elif exists_email > 0:
            print("email error")
            messages.error(request,"Email Exist")
        else:
            users = user_details.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender = gender,
                mail = mail,
                phone = phone,
                username = username,
                password = password,
                )
            users.save()
            print("User Created")
            # We will load the html content first
            random_num = random.randint(1000,9999)

            html_content = render_to_string("other/mail_templates/emailtemplate.html", {'name': first_name ,'otp':random_num })

            # html content jo load karenge usme se HTML tags nikal denge
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(  # Initialize a single email message (which can be sent to multiple recipients).
                # subject
                "Please Verify Your Account",
                # content
                text_content,
                # from email
                'findmynotes2002@gmail.com',
                # receipient list
                [mail]
            )

            # attach the html content
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            request.session["new_user"] = username
            request.session["new_user_id"] = users.unique_id
            request.session["new_otp"] = random_num
            return redirect(otp_page)

    return render(request,'pages/register/register.html')

def otp_page(request):
    if request.method == "POST":
        input_otp = request.POST['opt_input']
        if input_otp == str(request.session.get('new_otp')):
            set_active = user_details.objects.get(username = request.session.get("new_user"))
            set_active.is_active = True
            set_active.save()
            messages.success(request,"valid OTP")
            request.session['username'] = request.session.get("new_user")
            request.session['user_unique_id'] = request.session.get("new_user_id")
            return redirect(home)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,"pages/otp_verification/otp_verification.html")

