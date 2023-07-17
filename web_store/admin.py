from django.contrib import admin
from web_store.models import Category,Product,Cart,CartItem,Order,OrderItem
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','create','update']
    list_editable = ['price','stock']
    list_per_page = 2

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','total','token','email','create','update']
    list_per_page = 2
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','price','create','update']
    



admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)