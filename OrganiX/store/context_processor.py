from store.models.carts import Cart


def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(account=request.user)
        
        # Đếm số lượng mặt hàng trong giỏ
        if cart:
            count = cart.count()
        else:
            count = 0
    else:
        count = 0

    return {
        'cart_item_count': count
    }