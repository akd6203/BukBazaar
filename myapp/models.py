from django.db import models
from django.contrib.auth.models import User 

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d")
    description = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=250, unique=True)
    profile = models.ImageField(upload_to="authors/%Y/%m/%d")
    signature = models.ImageField(upload_to="authors/signatures")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    lg=(
        ('English','English'),
        ('Hindi','Hindi'),
        ('Punjabi','Punjabi'),
    )
    name = models.CharField(max_length=250, unique=True)
    cover = models.ImageField(upload_to="books/")
    description = models.TextField()
    language = models.CharField(max_length=40, choices=lg, default='English')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.FloatField()
    discounted_price = models.FloatField()
    pages = models.IntegerField()
    chapters = models.IntegerField()
    readers = models.IntegerField(default=0)
    awards = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.first_name

        
class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=250, blank=True)
    payer_id = models.CharField(max_length=250, blank=True,null=True)
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
    