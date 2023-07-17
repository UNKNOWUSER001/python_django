from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True) #ชื่อประเภทสินค้า(ห้ามชื่อซ้ำกัน)
    slug = models.SlugField(max_length=255,unique=True) #ตั้งชื่อเล่นให้ข้อมูล จัดหมวดหมู่(ผูกข้อมูลกับ url)


    def __str__(self): # แปลงข้อมูล model ที่สร้างแปลงเป็น string 
        return self.name 
    
    class Meta :
        ordering = ('name',) #เรียงลำดับชื่อ
        verbose_name = 'หมวดหมู่สินค้า'
        verbose_name_plural = 'ข้อมูลประเภทสินค้า'
    
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])
    
class Product(models.Model):
    name = models.CharField(max_length=255,unique=True) 
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2) #เป็นทศนิยม  และทศนิยม 2 ตำแหน่ง
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product',blank=True) 
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True) #วันเวลา ปัจจุบันที่กดบันทึกสินค้า 
    update = models.DateField(auto_now=True)  # หลังจาก
    
    def __str__(self):
        return self.name
    
    class Meta :
        ordering = ('name',) #เรียงลำดับชื่อ
        verbose_name = 'สินค้า'
        verbose_name_plural = 'ข้อมูลสินค้า'
    
    def get_url(self):
        return reverse('stockdetail',args=[self.category.slug, self.slug]) #reverse คือการดึง name url มาใช้ โดยดึง category.slug ออกมา
    

class Cart(models.Model): #ตะกร้าสินค้า
    cart_id = models.CharField(max_length=255,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id

    class Meta:
        db_table = 'cart'
        ordering = ('date_added',) 
        verbose_name = 'ตะกร้าสินค้า'
        verbose_name_plural = 'ข้อมูลตะกร้าสินค้า'

class CartItem(models.Model): #สินค้าในตะกร้า 
    product = models.ForeignKey(Product,on_delete=models.CASCADE) #สินค้า
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE) #ตะกร้า
    quantity = models.IntegerField() #คำนวณราคา
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
        verbose_name = 'รายการสินค้าในตระกร้า'
        verbose_name_plural = 'ข้อมูลรายการสินค้าในตระกร้า'

    def product_total(self): #การคำนวณผลรวมสินค้าแต่ละรายการ
        return self.product.price * self.quantity


    def __str__(self):
        return str(self.cart)
    
    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    name = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=255,blank=True)
    postcode = models.CharField(max_length=255,blank=True)
    total = models.DecimalField(max_digits=10,decimal_places=2) #คำนวณราคา
    email = models.EmailField(max_length=255,blank=True)
    token = models.CharField(max_length=255,blank=True)
    create = models.DateTimeField(auto_now_add=True) #วันเวลา ปัจจุบันที่กดบันทึกสินค้า 
    update = models.DateField(auto_now=True)  # หลังจาก
    
     

    class Meta:
         db_table = 'Order'
         ordering = ('id',) 
         verbose_name_plural = 'ประวัติผู้ซื้อ'
    def __str__(self):
        return str(self.id)
        
class OrderItem(models.Model):
    product  =  models.CharField(max_length=255) 
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True) #วันเวลา ปัจจุบันที่กดบันทึกสินค้า 
    update = models.DateField(auto_now=True)  # หลังจาก
    
    class Meta:
        db_table = 'OrderItem'
        ordering = ('order',)
        verbose_name_plural = 'ประวัติการซื้อสินค้า'
    def product_total(self): #การคำนวณผลรวมสินค้าแต่ละรายการ    จำนวน * กับ ราคา
        return self.quantity * self.price
    
    def __str__(self):
        return self.product

        
        
        
