from rest_framework import generics, permissions
from taqueria.models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Creating orders requires authentication; listing allowed for admins
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
