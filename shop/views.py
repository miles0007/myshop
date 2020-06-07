from django.shortcuts import render,get_object_or_404,HttpResponse
from shop.models import Category,Product
from cart.forms import CartAddProductForm
from shop.forms import SearchForm
from django.contrib import messages
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def product_list(request,category_slug=None):
	category = None
	categories = Category.objects.all().order_by('name')
	products_list = Product.objects.all().order_by('-created')

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products_list = products_list.filter(category=category)
		# paginator = Paginator(products_list, 6)
	
	paginator = Paginator(products_list, 9)
	page = request.GET.get('page')
	
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	return render(request,
				  'shop/product/list.html',
				  {'category':category,
				   'categories':categories,
				   'products':products})

def product_detail(request,id,slug):
	product = get_object_or_404(Product, id=id,
								slug=slug,available=True)
	# print(product.sliders.img_name)
	categories = Category.objects.all().order_by('name')
	cart_product_form  =CartAddProductForm()
	return render(request,'shop/product/detail.html',
				  {'product':product,
				   'cart_product_form':cart_product_form,
				   'categories':categories})

def nav_list(request,category_slug=None):
	category = None
	categories = Category.objects.all().order_by('name')
	products = Product.objects.filter(available=True)

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	return render(request,
				  'shop/nav.html',
				  {'category':category,
				   'categories':categories,
				   'products':products})

def item_search(request):
	form = SearchForm()
	query = None
	results = []

	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
			search_query = SearchQuery(query)
			results = Product.objects.annotate(search=search_vector,
											   rank=SearchRank(search_vector,search_query)
											   ).filter(rank__gte=0.3).order_by('-rank')
			return render(request,'shop/product/searchlist.html',
												{'form':form,
												'query':query,
												'results':results})
	return HttpResponse('not found')

def q_search(request):
	categories = Category.objects.all().order_by('name')
	if 'query' in request.GET:
		srch = request.GET['query']

		if srch:
			results = Product.objects.filter(Q(name__icontains=srch))
		
		paginator = Paginator(results, 9)
		page = request.GET.get('page')
		
		try:
			results = paginator.page(page)
		except PageNotAnInteger:
			results = paginator.page(1)
		except EmptyPage:
			results = paginator.page(paginator.num_pages)	

		return render(request,'shop/product/searchlist.html',
								{'results':results,'query':srch,'categories':categories})

