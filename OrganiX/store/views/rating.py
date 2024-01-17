from store.models.reviewrating import ReviewRating
from store.models.orders import Order
from django.shortcuts import render, redirect
def submit_review(request, order_id, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        print(order_id, product_id)
        if ReviewRating.objects.filter(user = request.user, product__id = product_id, order__id = order_id):
            review = ReviewRating.objects.get(user = request.user, product__id = product_id, order__id = order_id)
            review.subject = request.POST.get('subject')
            review.rating = request.POST.get('rating')
            review.review = request.POST.get('review')
            review.save()
            return redirect(url)
        else:
            review = ReviewRating()
            review.subject = request.POST.get('subject')
            review.rating = request.POST.get('rating')
            review.review = request.POST.get('review')
            review.product_id = product_id
            review.user_id = request.user.id
            review.order_id = order_id
            review.save()
            return redirect(url)