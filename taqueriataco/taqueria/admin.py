
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
	list_display = ('name', 'color_display', 'created_at')
	readonly_fields = ('color_display',)

	def color_display(self, obj):
		if obj.color:
			return format_html('<div style="width:48px;height:20px;background:{0};border-radius:4px;"></div>', obj.color)
		return ''
	color_display.short_description = 'Color'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('product', 'order', 'quantity', 'price_snapshot', 'subtotal')
	readonly_fields = ('price_snapshot', 'subtotal')



