from decimal import Decimal
from django.conf import settings
from taqueria.models import Product


class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity

        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        prod_map = {str(p.id): p for p in products}

        for pid, item in self.cart.items():
            product = prod_map.get(pid)
            if not product:
                continue
            price = Decimal(item['price'])
            quantity = item['quantity']
            subtotal = price * quantity
            yield {
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
            }

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.__iter__():
            total += item['subtotal']
        return total

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
