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

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def home(request):


    user_id = request.session.get("user_unique_id")
    show_books = book_images.objects.all()
    book_data = listing_books.objects.filter(buyer_id__isnull = True).exclude(book_seller_id = user_id)


    currency = 'INR'
    amount = 20000

    context = {}
    
	# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # def Merge(dict1, dict2):
    #     res = {**dict1, **dict2}
    #     return res
    # we need to pass these details to frontend.
    # context1 = {'book_data':book_data,'book_images':show_books,"user_id":user_id}

    
    context['book_images'] = show_books
    context['user_id'] = user_id

    search_query = request.GET.get('search_query')
    search_category = request.POST.get("search_category")

    if search_query != None:
        
        book_data = listing_books.objects.filter(book_name__icontains = search_query)


    context['book_data'] = book_data

    return render(request,'pages/home/index.html',context)




def product(request,productid): 
    book_data = get_object_or_404(listing_books,pk=productid)
    book_image = book_images.objects.filter(book_uid = book_data)
    user_id = request.session.get("user_unique_id")

    

    context = {'book_data':book_data,'book_images':book_image ,"user_id":user_id}
    
    currency = 'INR'

    if request.method == "POST":
        # Create a Razorpay Order   
        amount = request.POST.get("amount")
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
					# capture the payemt
					razorpay_client.payment.capture(payment_id, int(amount-123456789))
					print(productid)
					user_id = user_details.objects.get(pk = request.session.get("user_unique_id"))
					print(user_id)
					buyer_update = listing_books.objects.get(pk = productid)
					buyer_update.buyer_id =  user_id
					buyer_update.save()
                    
                        
					# render success page on successful caputre of payment
					return redirect(home)
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




def profile(request):
    user_details_to_display = user_details.objects.filter(username = request.session.get("username")).first()
    book_data = listing_books.objects.filter(book_seller_id = request.session.get('user_unique_id'))
    show_books = book_images.objects.filter(book_uid_id__in	 = book_data)
    user_id = request.session.get("user_unique_id")
    context = {
        'book_details':book_data,
        'user_detail':user_details_to_display,
        'book_images':show_books,
        'user_id': user_id
        }
    return render(request,'pages/profile/ProfilePage.html',context)
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
    context  = {'user_id': user_id}
    return render(request,'pages/sell/listbook.html',context)

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
        pincode = request.POST['pincode'] 
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
                )
            users.save()

            print("User Created")
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

def about(request):
    user_id = request.session.get("user_unique_id")
    context = {'user_id': user_id}
    return render(request,"other/about/about.html",context)

def logout(request):
    request.session.flush()
    return redirect(loginpage)