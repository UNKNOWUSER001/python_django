from web_store.models import Category,Cart,CartItem
from web_store.views import list_card


def Menu(request):
    menu = Category.objects.all()
    return dict(menu=menu)

#คำนวณจำนวนสินค้า
def counter(request):
    item_count = 0

    if 'admin' in request.path: #ถ้าเป็น admin จะ path
        return {}
    else:
        try:
            #query cart 
            cart=Cart.objects.filter(cart_id=list_card(request))
            #query cartitem
            cart_item=CartItem.objects.all().filter(cart=cart[:1])

            for item in cart_item:
                item_count+=item.quantity
        except Cart.DoesNotExist:
            item_count=0
    return dict(item_count=item_count)