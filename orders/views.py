from django.shortcuts import render,redirect,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from shop.models import Category
from django.template.loader import render_to_string
from django.core.mail import send_mail
import weasyprint

# Create your views here.
def order_create(request):
	categories = Category.objects.all().order_by('name')
	cart = Cart(request)
	product_all = []
	
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
			cart.clear()
			# launch asynchoronus task
			order_created.delay(order.id)
			# context = {
			# 'name' : cd['first_name'],'email':cd['email'],'products':product_all,'order_id':order.id}
			
			#send message to vendor
			# subject = 'An order has been Placed by {}, order ID-{}'.format(cd['first_name'],order.id)
			# message = render_to_string('orders/order/vendor_email.txt',context)
			# send_mail(subject, message, 'kavinkarthik025@gmail.com', ('milesstonner@gmail.com',))

			#send message_to user
			# subject = 'Boxit, Thankyou for purchasing.'
			# message = render_to_string('orders/order/user_email.txt',context)
			# send_mail(subject, message, 'kavinkarthik025@gmail.com', [cd['email']])


			# #set the order in session
			# request.session['order_id'] = order.id
			# return redirect(reverse('payment:process'))
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