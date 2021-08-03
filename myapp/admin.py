from django.contrib import admin
from myapp.models import Contact, Category, Author, Book, user_profile, order

admin.site.site_header="Kindle | Admin"

class ContactAdmin(admin.ModelAdmin):
    # fields=['name']
    list_filter = ["name","added_on"]
    list_editable=["name"]
    list_display = ["id","name","email","added_on", "updated_on"]
    search_fields = ["name","email"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on', 'updated_on']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','name','category','language','discounted_price','pages','added_on', 'updated_on']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on', 'updated_on']

class orderAdmin(admin.ModelAdmin):
    list_display = ['id','status','ordered_on']


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(user_profile)
admin.site.register(order,orderAdmin)
