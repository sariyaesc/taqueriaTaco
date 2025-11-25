
from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	readonly_fields = ('price_snapshot', 'subtotal')
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'is_available', 'created_at', 'total_price')
	list_filter = ('status', 'is_available', 'created_at')
	inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'created_at')
	list_filter = ('category',)
	search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('product', 'order', 'quantity', 'price_snapshot', 'subtotal')
	readonly_fields = ('price_snapshot', 'subtotal')



