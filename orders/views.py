from django.shortcuts import render,redirect,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.recommender import Recommender
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from shop.models import Category,Product
from django.template.loader import render_to_string
from django.core.mail import send_mail
import weasyprint

# Create your views here.
def order_create(request):
	categories = Category.objects.all().order_by('name')
	cart = Cart(request)
	product_all = []
	new = []
	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,
								  product=item['product'],
								  price=item['price'],
								  quantity=item['quantity'])
				product_all.append(item['product'])
			for i in (product_all):
				ele = str(i)
				new.append(ele)	# the elements are appended as a string value
			
			r  = Recommender()	# recommendation for produts in items
			parse_list = []
			for product_to_buy in product_all:
				# get elements in the cart and and get the product model 
				item = Product.objects.get(name=product_to_buy)
				parse_list.append(item)
			r.products_bought(parse_list)
			string = '\n'.join(new)
			print(string)
			cart.clear()
			# launch asynchoronus task
			order_created.delay(order.id,do=string)
			return render(request,'orders/order/created.html',
						{'order':order})

	else:
		form = OrderCreateForm()
	return render(request,'orders/order/create.html',
							{'cart':cart,'form':form,'categories':categories})

@staff_member_required
def admin_order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'admin/orders/order/detail.html',
								{'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response