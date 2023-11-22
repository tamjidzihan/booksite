from django.db.models.aggregates import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet,ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from .paginations import *
from .filters import *
from .models import *
from .serializers import *


class ProducViewset(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['id','price','last_update']
    search_fields = ['title']
    

    def get_serializer_context(self):
        return {"request": self.request}
    
    def destroy(self, request, *args, **kwargs):
         if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({"error": f"Product can not be deleted.Because Product is on orderitem."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
         return super().destroy(request, *args, **kwargs)
    
class ProducImageViewset(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get','post','patch','delete']

    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs['product_pk']).select_related('product')
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

class CatagoryViewset(ModelViewSet):
    queryset = Catagory.objects.annotate(product_count=Count("product")).all()
    serializer_class = CatagorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(catagory_id = kwargs['pk']):
            return Response({"error": f"Catagory can not be deleted.Because it has Some product on it."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CatagoryProductViewSet(ReadOnlyModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagoryProductSerializer
    # filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ['id']
    # ordering_fields = ['title']

    def get_queryset(self):
        catagory_id = self.kwargs.get('catagory_id')
        if catagory_id:
            return Product.objects.filter(catagory_id=catagory_id)
        return Catagory.objects.all()


class LikeViewset(ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(product_id = self.kwargs['product_pk'])


    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


class CartViewset(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = CartSerializer


class CartItemViewset(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}


class CustomerViwset(CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     GenericViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        if request.method == 'PUT':
            serializer = CustomerSerializer(customer,data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewset(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer

class OrderItemViewset(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    serializer_class = OrderItemsSerializer
    def get_queryset(self):
        return OrderItem.objects.filter(order_id = self.kwargs['order_pk']).select_related('product')

    def get_serializer_context(self):
        return {'order_id':self.kwargs['order_pk']}

