from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from users.models import Profile

User = get_user_model()


def seller_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user, role=Profile.Role.SELLER)

    # Annotate product_count on the profile queryset (requires seller FK on Product, added in D1/C1)
    try:
        from products.models import Product
        product_count = Product.objects.filter(seller=user, is_active=True).count()
    except Exception:
        product_count = 0

    context = {
        "username": user.username,
        "bio": profile.bio,
        "product_count": product_count,
    }
    return render(request, "users/seller_profile.html", context)
