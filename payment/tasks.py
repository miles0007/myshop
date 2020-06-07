from io import BytesIO
from celery import task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import weasyprint


@task
def payment_completed(order_id):
	'''
	Task to send an email when order is
	succesfully Placed.
	'''
	order = Order.objects.get(id=order_id)

	# mail Format
	subject = f'My shop - EE Invoice no. {order.id}'
	message = 'Please Find attached invoice for your recent Purchase.'
	email = EmailMessage(subject,
						 message,
						 'kavinkarthik025@gmail.com',
						 [order.email])

	# generate PDF
	html = render_to_string('orders/order/pdf.html',
                            {'order': order})
	out = BytesIO()
	stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')]

	# attach PDF File
	email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
	# send email 
	email.send()