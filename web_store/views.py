from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest,HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.core.paginator import Paginator,EmptyPage,InvalidPage #เพจหน้า
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import auth

from web_store.models import Category,Product,Cart,CartItem,Order,OrderItem
from web_store.forms import SignupForm
import stripe




# Create your views here.

def product(request,category_slug = None): # slug = ค่าว่าง
    products = None # ตั้งตัวแปรมาก่อนไม่ให้มีค่าว่าง
    category_page = None #สร้างตัวแปรมา
    if category_slug!= None: #ถ้าตัว แปรไม่เท่ากับ None
         category_page = get_object_or_404(Category,slug=category_slug) #ดึงข้อมูลจาก database โดยใช้ get_object_or_404(คำสั่งดึงจากฐานข้อมูลถ้าไม่มีให้เป็น 404 และอิงจาก model) โดยดึงจาก Model Category และ slug
         products = Product.objects.all().filter(category=category_page,available=True) 
    else:
         products = Product.objects.all().filter(available=True)  #ดึงข้อมูลจาก Productมา แล้ว กรองข้อมูล available
    #ทำหน้าเพจเลือกหน้า
    paginator = Paginator(products,4)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        productPage = paginator.page(page)
    except:
        (EmptyPage,InvalidPage)
        productPage = paginator(paginator.num_pages)

    context = {'products':productPage,'category':category_page}
    return render(request,'web_store/product.html',context) 

def goods(request, category_slug, goods_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=goods_slug) #_ 2 ครั้ง เพราะเป็นการเรียกใช้งาน
    except Product.DoesNotExist: 
        raise Http404("เกิดข้อผิดพลาดโปรดกรุณาเช็คด่วน !!!")  
    context = {'product': product}
    return render(request, 'web_store/goods.html', context)


def list_card(request: HttpRequest):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='signIn')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # สร้างตะกร้าสินค้า
    try:
        cart = Cart.objects.get(cart_id=list_card(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=list_card(request))
        cart.save()
    
    # ซื้อสินค้าครั้งแรก
    try:
        # ซื้อสินค้าซ้ำ
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            # เพิ่มจำนวนสินค้า
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        # ซื้อครั้งแรก
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
    return HttpResponseRedirect(reverse('product'))


def card_detail(request):
    total = 0
    counter = 0
    cart_items = None
    try:
        cart = Cart.objects.get(cart_id=list_card(request)) #ดึงตะกร้าจาก การสร้างตะกร้า
        cart_items = CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลในตะกร้า
        for item in cart_items:
            total+=(item.product.price * item.quantity)
            counter+=(item.quantity)
    except Exception as e:
        pass
    # api stripe
    stripe.api_key = settings.SECRET_KEY
    stripe_total = int(total*100) 
    description = 'Payment online'
    data_key = settings.PUBLIC_KEY
    #การส่งค่าการชำระเงิน
    if request.method == 'POST':
        try: 
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            name = request.POST['stripeBillingName']
            address = request.POST['stripeBillingAddressLine1']
            city = request.POST['stripeBillingAddressCity']
            postcode = request.POST['stripeBillingAddressZip']
            customer = stripe.Customer.create(email=email,source=token)
            charge = stripe.Charge.create(amount=stripe_total,currency='thb',description=description,customer=customer.id)
        #บันทึกข้อมูลสั่งซื้อ
            order = Order.objects.create(
            name = name,
            address = address,
            city = city,
            postcode= postcode,
            total = total,
            email = email,
            token = token,
        )
            order.save()
         #บันทึกรายการสั่งซื้อ
            for item in cart_items:
                oreder_item = OrderItem.objects.create(
                product = item.product.name,
                quantity = item.quantity,
                price = item.product.price,
                order = order,)
                oreder_item.save()
        #ลดจำนวน stock 
                product = Product.objects.get(id=item.product.id)
                product.stock = int(item.product.stock-oreder_item.quantity)
                product.save()
                item.delete()
            return redirect('product')

        except stripe.error.CardError as e:
            return False , e
    return render(request, 'web_store/cart.html',dict(cart_items=cart_items,total=total,counter=counter,data_key=data_key,stripe_total=stripe_total,description=description,))

#ลบสินค้าในตะกร้าต้องโยน id มาด้วยเพื่อเป็นเงื่อนไขนการลบ
def removeCart(request,product_id):
    #ดึงตะกร้ามาใช้
    cart = Cart.objects.get(cart_id=list_card(request))
    #สินค้าที่จะลบ
    product = get_object_or_404(Product,id=product_id)
    cartitem = CartItem.objects.get(product=product,cart=cart)
    #ลบรายการสินค้า ออกจากตะกร้า  โดยลบจากรายการสินค้า Cartitem model
    cartitem.delete()
    return redirect('cart_detail')

def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # บันทึกลง group Customer
            username = form.cleaned_data.get('username')
            # ดึงข้อมูล User จากฐานข้อมูล
            signupUser = User.objects.get(username=username)
            # จัด Group
            customerGroup = Group.objects.get(name='Customer')
            customerGroup.user_set.add(signupUser)
            return HttpResponseRedirect(reverse('signupthk'))
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'web_store/signup.html', context)

def signupTHK(request:HttpRequest):
    return render(request,'web_store/signupthk.html')

def SignIn(request:HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('signup'))

    else:
        pass

    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'web_store/login.html',context)

def SignOut(request):
    logout(request)
    # return redirect('signIn')
    return HttpResponseRedirect(reverse('home'))

def search(request):
    try:
        products = Product.objects.filter(name__contains=request.GET['title'])
        if not products:
            raise Product.DoesNotExist
        context = {'products': products}
        return render(request, 'web_store/product.html', context)
    except Product.DoesNotExist:
        return redirect('empty')

def empty(request):
    return render(request, 'web_store/empty.html')

def OrderHistory(request):
    if request.user.is_authenticated:
        user = auth.get_user(request)
        orders = Order.objects.filter(name=user)
        context={'orders':orders}
    return render(request, 'web_store/orderhistory.html',context)


def ViewsOrder(request,order_id):
    if request.user.is_authenticated:
        user = auth.get_user(request)
        order = Order.objects.get(name=user,id=order_id)
        orderItem = OrderItem.objects.filter(order=order)
        context={'order_detail':orderItem,'order':order}
    return render(request, 'web_store/orderdetail.html',context)
