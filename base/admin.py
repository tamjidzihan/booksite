from django.contrib import admin,messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from . import models

# Register your models here.

@admin.register(models.Catagory)
class CaragoryAdmin(admin.ModelAdmin):
    list_display = ['title','product_count','feature_product']
    autocomplete_fields = ['feature_product']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self,catagory):
        url = (
            reverse('admin:base_product_changelist') 
            + '?'
            +urlencode({
                'catagory__id': str(catagory.id)
            })
            )
        return format_html('<a href ="{}" >{}</a>',url,catagory.product_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count = Count('product'))

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['catagory']
    list_display = ['title','price','inventory','catagory','inventory_status']
    list_editable = ['price','inventory']
    list_filter = ['catagory','last_update']
    list_select_related = ['catagory']
    search_fields = ['title__istartswith']
    list_per_page = 50

    def catagory(self,prodect):
        return prodect.catagory.title

    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    

    actions = ['clear_inventory']
    @admin.action(description='Clear Inventory(On selected product)')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products inventory were successfully Deleted',
            messages.SUCCESS
        )

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=['id','product','image']
    autocomplete_fields = ['product']
    list_per_page = 50

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','phone','address','orders']
    list_select_related = ['address']
    ordering = ['user__first_name','user__last_name']
    autocomplete_fields = ['user']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    list_per_page = 50

    @admin.display(ordering='order_count')
    def orders(self,customer):
        url = (
            reverse('admin:base_order_changelist')
            +'?'
            +urlencode({
                'customer_id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>',url,customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count = Count('order'))




@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','placed_at','payment_status','order_item']
    autocomplete_fields = ['customer']
    list_editable = ['payment_status']
    list_per_page = 50

    def order_item(self,order):
        return reverse('admin:base_orderitem_changelist')


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','quantity','product_price','total_price']
    
    def product_price(self,orderitem):
        return orderitem.product.price
    
    def total_price(self,orderitem):
        return (orderitem.product.price * orderitem.quantity)

   


@admin.register(models.Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['customer','street','city','country']
    autocomplete_fields = ['customer']



@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','customer','product','like']
    autocomplete_fields = ['product','customer']




@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']



@admin.register(models.CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ['id','cart','product','quantity']
    autocomplete_fields = ['product']