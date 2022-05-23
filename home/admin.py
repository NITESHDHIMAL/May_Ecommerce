from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Brand,BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product,ProductAdmin)


class OrderItemTubleinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleinline]
    list_display = ('firstname','phone','email','payment_id','paid','date')
    search_fields = ['firstname','email','payment_id']

admin.site.register(Order,OrderAdmin)


admin.site.register(Price)
admin.site.register(Color)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(Hero)
admin.site.register(Banner)

admin.site.register(OrderItem)
























