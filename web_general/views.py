from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,InvalidPage #เพจหน้า
from web_store.models import Category,Product




# Create your views here.

def home(request,category_slug = None): # slug = ค่าว่าง
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

