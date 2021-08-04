from django import conf
from django.http.response import HttpResponse, HttpResponseGone, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,reverse
from myapp.models import Contact, Category,Book, user_profile, order
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from paypal.standard.forms import PayPalPaymentsForm 
from django.conf import settings

# Create your views here.
def index(request):
    context = {}
    
    cats = Category.objects.all().order_by("name")

    context["categories"] = cats
    return render(request, "index.html", context)

def contact_view(request):
    context={}
    if request.method=="POST":
        nm = request.POST.get("name")
        em = request.POST.get("email")
        msz = request.POST.get("message")

        obj = Contact(name=nm, email=em, message=msz)
        try:
            obj.save()
            context["status"] = "Dear {} your contact request submitted successfully!".format(nm)
        except:
            context["status"] = "A user with this email already submitted feedback!"

    return render(request, "contact.html",context)

def single_author(request):
    return render(request, "author.html")

def all_books(request):
    con={}
    al_books = Book.objects.all().order_by("name")
    if "q" in request.GET:
        cat_id = request.GET.get("q")
        al_books = Book.objects.filter(category__id=cat_id)

    con["books"] = al_books
    return render(request, "all_books.html",con)

def register(request):
    context={}
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        number = request.POST.get('number')
        
        check = len(User.objects.filter(username=email))
        if check==0:
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()

            profile = user_profile(user=user, contact_number=number)
            profile.save()
            
            context['status'] = 'Account created successfully!'
        else:
            context['error'] = 'A User with this email already exists!'
    return render(request, "register.html", context)

def signIn(request):
    context  = {}
    if request.method=="POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user = authenticate(username=email,password=passw) 
        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect('/admin')
            return HttpResponseRedirect('/dashboard')
        else:
            context['status'] = 'Invalid login details!'
    return render(request, "login.html", context)

def single_book(request,id):
    context={}

    try:
        book = Book.objects.get(id=id)
        context['book'] = book
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            ord = order(user=user, book=book)
            ord.save()
            inv = 'INV10001-{}'.format(ord.id)
            paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':book.discounted_price,
            'item_name':book.name,
            'user_id':request.user.id,
            'invoice':inv,
            'notify_url':'http://{}{}'.format("127.0.0.1:8000",reverse('paypal-ipn')),
            'return_url':'http://{}{}'.format("127.0.0.1:8000",reverse('payment_done')),
            'cancel_url':'http://{}{}'.format("127.0.0.1:8000",reverse('payment_cancel')),
            }
            ord.invoice_id = inv 
            ord.save()
            request.session['order_id'] = ord.id 

            form = PayPalPaymentsForm(initial=paypal_dict)
            context['form'] = form
        return render(request, "single_book.html", context)
    except:
        return HttpResponse("<h1>Not Found</h1>")

def dashboard(request):
    context={}
    my_orders = order.objects.filter(user__username=request.user.username, status=True).order_by('-id')
    context['orders'] = my_orders
    try:
        user_details = user_profile.objects.get(user__username = request.user.username)
        context['profile'] = user_details
    except:
        return HttpResponse("<h1>You are not allowed here!</h1>")
    
    if "update_profile" in request.POST:
        name = request.POST.get("name")
        em = request.POST.get("email")
        nm = request.POST.get("number")
        ad = request.POST.get("address")
        
        #Update details 
        user_details.user.first_name = name
        user_details.user.email = em 
        user_details.user.save()

        user_details.contact_number = nm
        user_details.address = ad
        user_details.save()

        if "profile_pic" in request.FILES:
            pic = request.FILES.get("profile_pic")
            user_details.profile_pic = pic 
            user_details.save()
            
        context['status'] = 'Profile updated successfully!'
    
    if "update_password" in request.POST:
        current_password = request.POST.get("c_password")
        new_password = request.POST.get("n_password")

        login_user = User.objects.get(id=request.user.id)
        check = login_user.check_password(current_password)
        if check==True:
            login_user.set_password(new_password)
            login_user.save()
            context['status'] = 'Password Updated Successfully!'
            login(request, login_user)
        else:
            context['status'] = 'Incorrect Current Password!'

    return render(request,"dashboard.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def payment_done(request):
    pid = request.GET.get('PayerID')
    order_id = request.session.get('order_id')

    order_obj = get_object_or_404(order, id=order_id)
    order_obj.payer_id = pid 
    order_obj.status = True 
    order_obj.save()

    return render(request, 'payment_successfull.html')

def payment_cancel(request):
    order_id = request.session.get('order_id')
    order_obj = get_object_or_404(order, id=order_id)
    order_obj.delete()
    return render(request, 'payment_failed.html')