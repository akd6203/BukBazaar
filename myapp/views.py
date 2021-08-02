from django.http.response import HttpResponse
from django.shortcuts import render
from myapp.models import Contact, Category,Book, user_profile
from django.contrib.auth.models import User

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
    return render(request, "login.html")

def single_book(request,id):
    context={}
    try:
        book = Book.objects.get(id=id)
        context['book'] = book
        return render(request, "single_book.html", context)
    except:
        return HttpResponse("<h1>Not Found</h1>")