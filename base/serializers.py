from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from decimal import Decimal
from .models import *

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields =  ['id','image']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('Invalide query')
        return value
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id = product_id,**validated_data)
    
#custom serializers----------------------------------->
class SimpleProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many = True,read_only= True)
    class Meta:
        model = Product
        fields = ['id','title','price','images']

class CatagorySerializer(ModelSerializer):
    feature_product = serializers.StringRelatedField()
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Catagory
        fields = ["id", "title", "feature_product", "product_count"]
        read_only_fields = ["product_count"]

    


class CatagoryProductSerializer(serializers.ModelSerializer):
    products = SimpleProductSerializer(many=True, read_only=True,source="product_set")

    class Meta:
        model = Catagory
        fields = ["id", "title", "products"]

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields =  ['id','image']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('Invalide query')
        return value
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id = product_id,**validated_data)



class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many = True,read_only= True)
    class Meta:
        model = Product
        fields = ["id","title","slug","inventory","price","price_with_tax","description","catagory","images"]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)



class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','date','like','customer','product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Like.objects.create(product_id = product_id,**validated_data)





#custom serializers----------------------------------->
class AddCartItemSerializer(ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('Invalide query')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item =  CartItem.objects.get(cart_id = cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id = cart_id,
                product_id=product_id,
                quantity = quantity)
        return self.instance


    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

#custom serializers----------------------------------->
class UpdateCartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']



class CartItemSerializer(ModelSerializer):
    product = SimpleProductSerializer()
    product_total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price
    
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','product_total_price']



class CartSerializer(ModelSerializer):
    cartitem_set = CartItemSerializer(read_only = True,many =True)
    id = serializers.UUIDField(read_only = True)
    
    cartitem_total_price = serializers.SerializerMethodField(method_name='get_cartitem_total_price')

    def get_cartitem_total_price(self,cart:Cart):
        total_price = []
        for items in cart.cartitem_set.all():
            total_price.append(items.quantity * items.product.price)
        return sum(total_price)

    class Meta:
        model= Cart
        fields = ['id','cartitem_set','cartitem_total_price']



class CustomerSerializer(ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','date_of_birth']
    


class OrderItemsSerializer(ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity']



class OrderSerializer(ModelSerializer):
    items = OrderItemsSerializer(many =True,read_only = True)
    total_price = serializers.SerializerMethodField(method_name='get_ordeitem_total_price')

    def get_ordeitem_total_price(self,order:Order):
        total_price = []
        for items in order.items.all():
            total_price.append(items.quantity * items.product.price)
        return sum(total_price)



    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items','total_price']
        