from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.product,name='product'),
    path('category/<slug:category_slug>',views.product, name='product_by_category'),
    path('goods/<slug:category_slug>/<slug:goods_slug>',views.goods, name='stockdetail'),
    path('cart/add/<int:product_id>/', views.add_cart, name="addCart"),
    path('cartdetail/',views.card_detail,name="cart_detail"),
    path('cart/remove/<int:product_id>', views.removeCart, name="remove"),
    path('account/create',views.signup, name='signup'),
    path('account/thk',views.signupTHK,name='signupthk'),
    path('account/login',views.SignIn,name='signIn'),
    path('account/logout',views.SignOut,name='SignOut'),
    path('search/',views.search,name = 'search'),
    path('empty/',views.empty,name='empty'),
    path('Orderhistory/',views.OrderHistory,name='orderhistory'),
    path('order/<int:order_id>',views.ViewsOrder,name='orderdetail'),
    
    

    
    
     #นำ slug มาใช้เป็น path

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

# urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
 