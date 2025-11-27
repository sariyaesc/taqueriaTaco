from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


# Models: Tablas de la base de datos


class Category(models.Model):
	name = models.CharField(max_length=200)
	# Hex color code used for badges (e.g. #3b82f6). Assigned automatically when empty.
	color = models.CharField(max_length=7, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		# Auto-assign a random pastel-ish hex color when none provided
		if not self.color:
			import random
			# Generate a random pastel color by mixing with white
			r = int((random.randint(0, 255) + 255) / 2)
			g = int((random.randint(0, 255) + 255) / 2)
			b = int((random.randint(0, 255) + 255) / 2)
			self.color = '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
		super().save(*args, **kwargs)


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
	description = models.TextField(blank=True)
	image = models.URLField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} (${self.price})"


class Order(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_DONE = 'done'
	STATUS_CHOICES = [
		(STATUS_PENDING, 'pending'),
		(STATUS_DONE, 'done'),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	is_available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order #{self.pk} - {self.user} - {self.status}"

	@property
	def total_price(self):
		items = self.items.all()
		total = sum((item.subtotal for item in items), 0)
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	price_snapshot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

	def save(self, *args, **kwargs):
		# Ensure price snapshot is set from product if not provided
		if self.product and (self.price_snapshot is None):
			self.price_snapshot = self.product.price

		# Calculate subtotal
		if self.price_snapshot is not None:
			self.subtotal = self.price_snapshot * self.quantity

		super().save(*args, **kwargs)

	def __str__(self):
		prod = self.product.name if self.product else 'Deleted product'
		return f"{prod} x {self.quantity} (${self.subtotal or '0.00'})"
