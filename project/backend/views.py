from django.shortcuts import get_object_or_404, redirect, render
from  django.contrib import messages    
from backend.models import book_images, user_details, listing_books
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import FileSystemStorage
import random
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,HttpResponse
from django.db.models import Q

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def home(request):
    user_id = request.session.get("user_unique_id")
    print("user_id-"+str(user_id))
    user_pincode = None
    if user_id is not None:
        user  = user_details.objects.get(pk = user_id)
        user_pincode = user.address_pincode

    book_data = listing_books.objects.filter(
        (Q(buyer_id__isnull = True)),
        (Q(book_seller__address_pincode__exact = user_pincode))
        ).exclude(book_seller_id = user_id)

    show_books = book_images.objects.all()

    search_query = ""
    if search_query is not None:
        search_query = request.GET.get('search_query')
        book_category = request.GET.get('book_category')
        print(search_query)
        if book_category == "All":
            book_category = ""
    else:
        search_query = ""
        print(search_query)

    if search_query != None:
        book_data = listing_books.objects.filter( 
            (Q(book_category__icontains = book_category)),
            ( Q(book_name__icontains = search_query)|Q(book_author__icontains = search_query)|Q(book_publisher__icontains = search_query) ),
            (Q(buyer_id__isnull = True)),
            (Q(book_seller__address_pincode__exact = user_pincode))
            ).exclude(Q(book_seller_id = user_id))


    context = {}
    context['book_data'] = book_data
    context['book_images'] = show_books
    context['search_query'] = search_query
    context['user_id'] = user_id

    return render(request,'pages/home/index.html',context)




def product(request,productid): 

    user_id = request.session.get("user_unique_id")
    book_data = get_object_or_404(listing_books,pk=productid)
    book_image = book_images.objects.filter(book_uid = book_data)

    

    context = {'book_data':book_data,'book_images':book_image ,"user_id":user_id}
    

    if request.method == "POST":
        # Create a Razorpay Order   
        amount = request.POST.get("amount")
        currency = 'INR'
        amount = int(amount) * 100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = str(productid)+ '/paymenthandler/'+ str(amount+123456789)

        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        


    return render(request,'pages/product/Product.html',context)



@csrf_exempt
def paymenthandler(request,amount,productid):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
            

			if result is not None:

				try:
					# capture the payment
					razorpay_client.payment.capture(payment_id, int(amount-123456789))
					print(productid)
					user_id = user_details.objects.get(pk = request.session.get("user_unique_id"))
					print(user_id)
					buyer_update = listing_books.objects.get(pk = productid)
					buyer_update.buyer_id =  user_id
					buyer_update.save()
                    
                        
					# render success page on successful caputre of payment
					return redirect(my_orders)
				except:

					# if there is an error while capturing payment.
					return HttpResponse("fail")
			else:

				# if signature verification fails.
				return HttpResponse("failure")
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()


def my_orders(request):

    user_id = request.session.get("user_unique_id")
    user_details_to_display = user_details.objects.filter(username = request.session.get("username")).first()
    book_data = listing_books.objects.filter(buyer_id = user_id)
    print(book_data)
    show_books = book_images.objects.filter(book_uid_id__in	 = book_data)
    user_id = request.session.get("user_unique_id")
    context = {
        'book_details':book_data,
        'user_detail':user_details_to_display,
        'book_images':show_books,
        'user_id': user_id
        }

    return render(request,'pages/profile/my_orders.html',context)




def profile(request):
    user_id = request.session.get("user_unique_id")
    user_details_to_display = user_details.objects.filter(username = request.session.get("username")).first()
    book_data = listing_books.objects.filter(book_seller_id = request.session.get('user_unique_id'))
    show_books = book_images.objects.filter(book_uid_id__in	 = book_data)
    context = {
        'book_details':book_data,
        'user_detail':user_details_to_display,
        'book_images':show_books,
        'user_id': user_id
        }
    return render(request,'pages/profile/posted_books.html',context)

def edit_profile(request):
    user_id = request.session.get("user_unique_id")
    user_details_to_display = user_details.objects.get(pk = user_id)


    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pincode = request.POST['pincode'] 
        block = request.POST['block'] 
        address_line_1 = request.POST['address_line_1'] 
        address_line_2 = request.POST['address_line_2']  
        district = request.POST['District'] 
        state = request.POST['state'] 
        gender = request.POST['gender'] 
        mail = request.POST['mail'] 
        phone = request.POST['phone'] 
        username = request.POST['username'] 
        password = request.POST['password'] 

        print(username)
        user_details_to_display.first_name=first_name
        user_details_to_display.last_name=last_name
        user_details_to_display.gender = gender
        user_details_to_display.mail = mail
        user_details_to_display.phone = phone
        user_details_to_display.username = username
        user_details_to_display.password = password
        user_details_to_display.address_pincode = pincode
        user_details_to_display.address_line_1 = address_line_1
        user_details_to_display.address_line_2 = address_line_2
        user_details_to_display.block = block
        user_details_to_display.district = district
        user_details_to_display.state = state
        user_details_to_display.save()

        print("User Updated")
        messages.success(request,"Profile Updated")
        # return redirect('profile')


    context = {
        'user_detail':user_details_to_display,
        'user_id': user_id
        }
    return render(request,'pages/profile/edit_profile.html',context)





def sell(request):
    user_id = request.session.get("user_unique_id")
    if request.method == 'POST':
        book_name = request.POST['book_name']
        book_category = request.POST['book_category']
        book_author = request.POST['book_author']
        book_publisher = request.POST['book_publisher']
        book_year_edition = request.POST['book_year_edition']
        book_mrp  = request.POST['book_mrp']
        book_selling_price = request.POST['book_selling_price']
        book_description = request.POST['book_description']


        list_book_details = listing_books.objects.create(
            book_name=book_name, 
            book_author=book_author,
            book_category=book_category,
            book_publisher=book_publisher,
            book_year_edition=book_year_edition,
            book_selling_price = book_selling_price,
            book_description = book_description,
            book_mrp = book_mrp,
            book_seller_id = user_details.objects.get(username = request.session.get("username")).unique_id
            )
        list_book_details.save()



        images = request.FILES.getlist('image_file')

        # file_type = request.POST['image_type']
        for image in images:
            print(image.name)
            fs = FileSystemStorage(location= 'books/'+str(request.session.get("user_unique_id"))+"/"+str(list_book_details.pk))
            fs.save(image.name,image)
            file_details = book_images.objects.create(
                path = str(str(request.session.get("user_unique_id")))+"/"+ str(list_book_details.pk)+"/"+image.name,
                book_uid = listing_books.objects.get(pk = list_book_details.pk)
                )
            file_details.save()
            return redirect(profile)
    context  = {'user_id': user_id}
    return render(request,'pages/sell/listbook.html',context)

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:

            validate_userid = user_details.objects.get( Q(username__exact = username))
            user_password = validate_userid.password
            print(user_password)

            user_unique_id = validate_userid.unique_id
            print(user_unique_id)

            first_name = validate_userid.first_name
            print(first_name)

            mail = validate_userid.mail
            print(mail)

            if user_password == password:
                check_active = validate_userid.is_active
                print("is_active status: "+ str(check_active))

                if check_active == 1:
                    request.session['username'] = username
                    request.session['user_unique_id'] = user_unique_id
                    return redirect(profile)
                else:
                    print(send_mail(request,first_name, username , user_unique_id,mail))
                    return redirect(otp_page)
            else:
                messages.error(request,"Invalid password")
                print("Invalid password")

        except:
            messages.error(request,"Invalid username or password")
            print("Invalid username or password")


    return render(request,'pages/login/login.html')

def clear_mssge():
    for msg in messages:
        del msg

def registeration_page(request):
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        pincode = request.POST['pincode'] 
        block = request.POST['block'] 
        address_line_1 = request.POST['address_line_1'] 
        address_line_2 = request.POST['address_line_2']  
        district = request.POST['District'] 
        state = request.POST['state'] 


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
                address_pincode = pincode,
                address_line_1 = address_line_1,
                address_line_2 = address_line_2,
                block = block,
                district = district,
                state = state,
                )
            users.save()

            print("User Created")
            send_mail(request,first_name, username , users.pk,mail)

            return redirect(otp_page)

    return render(request,'pages/register/register.html')


def send_mail(request,first_name,username,user_unique_id,mail_id):
    # We will load the html content first
            random_num = random.randint(1000,9999)

            html_content = render_to_string("other/mail_templates/mail_temp.html", {'name': first_name ,'otp':random_num })

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
                [mail_id]
            )

            # attach the html content
            mail.attach_alternative(html_content, "text/html")
            mail.send()

            request.session["new_user"] = username
            request.session["new_user_id"] = user_unique_id
            request.session["new_otp"] = random_num
            print("mail sent")

            return "Mail Sent"


def otp_page(request):
    user = user_details.objects.get(username = request.session.get("new_user"))

    request.session['username'] = request.session.get("new_user")
    request.session['user_unique_id'] = request.session.get("new_user_id")

    username = request.session['username']
    user_unique_id = request.session['user_unique_id']
    user = user_details.objects.get( Q(username__exact = username))
    

    first_name = user.first_name
    print(first_name)

    mail = user.mail
    print(mail)

    context = {
            "first_name":first_name,
            "username":username,
            "user_id":user_unique_id,
            "mail_id":mail,
            "request":request
        }
    if request.method == "POST":
        
        input_otp = request.POST['otp_input']
    


        if input_otp == str(request.session.get('new_otp')):
            user.is_active = True
            user.save()
            messages.success(request,"valid OTP")
          

            return redirect(home)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,"pages/otp_verification/otp_verification.html",context)

def about(request):
    user_id = request.session.get("user_unique_id")
    context = {'user_id': user_id}
    return render(request,"other/about/about.html",context)



def logout(request):
    request.session.flush()
    return redirect(loginpage)