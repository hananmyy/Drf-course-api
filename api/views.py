from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.models import Order, Product
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer)


#class-based views for product API endpoints - generic
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# function-based views for product API endpoints - to return view of all products
""" @api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data) """


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


# to return view of a single product
"""@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)"""


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset() # get the base queryset from the parent class
        return qs.filter(user=self.request.user) # filter the base queryset to only include orders for the authenticated user
  


"""@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related(
        'items__product')  # prefetch related products for each order item by following the FK from item itself thru to the product model
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data) # rest framework's Response object is used to return data in JSON format"""



#drf api view
class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products' : products,
            'count':len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data) # returns html format by default but can be overridden to json by adding the `format` parameter to the request URL, e.g. `?format=json` in the browser or API client
    


# function based view - replaced above with drf api view
"""@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products' : products,
        'count':len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'],
    })
    return Response(serializer.data)"""


