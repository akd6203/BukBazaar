from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from myapp.models import Contact, Category,Book, user_profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

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
        return render(request, "single_book.html", context)
    except:
        return HttpResponse("<h1>Not Found</h1>")

def dashboard(request):
    context={}
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
    return render(request,"dashboard.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')