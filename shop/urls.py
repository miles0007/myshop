from django.urls import path
# from django.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  url

app_name = 'shop'

urlpatterns = [
		# path('search/',views.item_search,name='search'),
		path('search/',views.q_search,name='search'),
		path('',views.product_list,name='product_list'),
		path('<slug:category_slug>/',views.product_list,
				name='product_list_by_category'),
		path('<int:id>/<slug:slug>/',views.product_detail,
				name='product_detail'),

]
urlpatterns +=static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)