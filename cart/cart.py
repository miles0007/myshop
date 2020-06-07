from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
	# Initilaize the Cart
	def __init__(self,request):
		# getting the current session
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
	# save an empty cart in session
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, quantity=1, override_quantity=False):
		# add product to cart and update
		product_id = str(product.id)
		# print(product_id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity' : 0,
									'price' : str(product.price)}
			print(product.price)
		if override_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		self.session.modified = True

	def remove(self, product):
		# remove product from cart
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		# iterating items  and get product from database
		product_id = self.cart.keys()
		products = Product.objects.filter(id__in=product_id)
		'''
			Not to Change the orignal cart
			So Cart is Copied to iter in loop
		'''
		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item
			
	
	def __len__(self):
		# total quantities in cart
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		# total price of products in cart
		return sum(Decimal(item['price'])*(item['quantity']) for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save()
