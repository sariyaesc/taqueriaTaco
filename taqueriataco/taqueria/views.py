from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import Product, Order, OrderItem
from .cart import Cart


def home(request):
	products = Product.objects.all().order_by('-created_at')
	return render(request, 'home.html', {'products': products})


def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		# Add Bootstrap classes/placeholders to form fields so floating labels work
		for name in ('username', 'password1', 'password2'):
			if name in form.fields:
				w = form.fields[name].widget
				w.attrs.setdefault('class', '')
				if 'form-control' not in w.attrs['class']:
					w.attrs['class'] = (w.attrs['class'] + ' form-control').strip()
				w.attrs.setdefault('placeholder', name.replace('password', 'Password').capitalize())
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('profile')
	else:
		form = UserCreationForm()
		for name in ('username', 'password1', 'password2'):
			if name in form.fields:
				w = form.fields[name].widget
				w.attrs.setdefault('class', '')
				if 'form-control' not in w.attrs['class']:
					w.attrs['class'] = (w.attrs['class'] + ' form-control').strip()
				w.attrs.setdefault('placeholder', name.replace('password', 'Password').capitalize())
	return render(request, 'register.html', {'form': form})


def signin_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		# Ensure rendered inputs have Bootstrap classes/placeholders for the floating labels
		for name in ('username', 'password'):
			if name in form.fields:
				w = form.fields[name].widget
				w.attrs.setdefault('class', '')
				# append form-control (avoid duplicate)
				if 'form-control' not in w.attrs['class']:
					w.attrs['class'] = (w.attrs['class'] + ' form-control').strip()
				# ensure a placeholder is present for Bootstrap floating labels
				w.attrs.setdefault('placeholder', name.capitalize())
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			# support next parameter from GET or POST (form on /profile/ posts next)
			next_url = request.POST.get('next') or request.GET.get('next') or reverse('home')
			return redirect(next_url)
	else:
		form = AuthenticationForm()
		# Add Bootstrap classes/placeholders for unauthenticated GET form
		for name in ('username', 'password'):
			if name in form.fields:
				w = form.fields[name].widget
				w.attrs.setdefault('class', '')
				if 'form-control' not in w.attrs['class']:
					w.attrs['class'] = (w.attrs['class'] + ' form-control').strip()
				w.attrs.setdefault('placeholder', name.capitalize())
	return render(request, 'signin.html', {'form': form})


def profile_view(request):
	"""Profile page: shows different content depending on authentication.

	- If the user is authenticated: show welcome and order history.
	- If not: show a sign-in form and links to register.
	"""
	if not request.user.is_authenticated:
		# Redirect unauthenticated users to the signin page with a `next` param
		signin_url = reverse('signin')
		return redirect(f"{signin_url}?next={request.path}")

	orders = request.user.orders.all().order_by('-created_at')
	return render(request, 'profile.html', {'orders': orders})


def logout_view(request):
	logout(request)
	return redirect('home')


def cart_view(request):
	cart = Cart(request)
	return render(request, 'cart.html', {'cart': cart})


def success_view(request):
	return render(request, 'success.html')


def cart_add(request):
	if request.method == 'POST':
		pid = request.POST.get('product_id')
		qty = int(request.POST.get('quantity', 1))
		product = get_object_or_404(Product, pk=pid)
		cart = Cart(request)
		cart.add(product, quantity=qty)
		return JsonResponse({'ok': True, 'cart_count': len(cart), 'cart_total': str(cart.get_total_price())})
	return JsonResponse({'ok': False}, status=400)


def cart_update(request):
	if request.method == 'POST':
		pid = request.POST.get('product_id')
		qty = int(request.POST.get('quantity', 1))
		product = get_object_or_404(Product, pk=pid)
		cart = Cart(request)
		cart.add(product, quantity=qty, update_quantity=True)
		return JsonResponse({'ok': True, 'cart_count': len(cart), 'cart_total': str(cart.get_total_price())})
	return JsonResponse({'ok': False}, status=400)


def cart_remove(request):
	if request.method == 'POST':
		pid = request.POST.get('product_id')
		product = get_object_or_404(Product, pk=pid)
		cart = Cart(request)
		cart.remove(product)
		return JsonResponse({'ok': True, 'cart_count': len(cart), 'cart_total': str(cart.get_total_price())})
	return JsonResponse({'ok': False}, status=400)


@login_required
def checkout(request):
	cart = Cart(request)
	if len(cart) == 0:
		return redirect('cart')

	# Create order and order items
	order = Order.objects.create(user=request.user)
	for item in cart:
		OrderItem.objects.create(
			order=order,
			product=item['product'],
			quantity=item['quantity'],
			price_snapshot=item['price'],
			subtotal=item['subtotal'],
		)

	cart.clear()
	return redirect('success')
