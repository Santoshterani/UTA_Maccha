from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Customer, Item
from .models import Restaurant
from .models import Cart,Order
from django.db.models import Count, Avg
from django.utils import timezone
import uuid
import razorpay
from django.conf import settings 

# Create your views here.
def index(request):
    return render(request, "index.html")

def open_signin(request):
    # return HttpResponse("Sign In")
    return render(request, "signin.html")

def open_signup(request):
    return render(request, "signup.html")

def signup(request):
    # return HttpResponse("Received")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username = username)
            return HttpResponse("Duplicates username not allowed")
        except:
        #Creating customer table object
            Customer.objects.create(username = username,
                                password = password,
                                email = email,
                                mobile = mobile,
                                address = address)
        
        return render(request, "signin.html")
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Customer.objects.get(username=username, password=password)
            
            if username == "admin":
                return render(request, "admin_home.html")
            else:
                restaurant = Restaurant.objects.all()
                return render(request, 'customer_home.html', {"restaurant": restaurant, "username": username})
        
        except Customer.DoesNotExist:
            return render(request, "fail.html")
    
    # If request is GET, just show signin page
    return render(request, "signin.html")

    
# Opens Add Restaurant Page
def open_add_restaurant(request):
    return render(request, "add_restaurant.html")

# Adds Restaurant
def add_restaurant(request):
    #return HttpResponse("Working")
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name, picture=picture, cuisine=cuisine, rating=rating)

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurant.html', {"restaurants": restaurants})

    return HttpResponse("Invalid request")

# Show Restaurants
def open_show_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'show_restaurant.html', {"restaurants": restaurants})

# Opens Update Restaurant Page
def open_update_restaurant(request, restaurant_id):
    #return HttpResponse("Working")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurant.html', {"restaurants": restaurants})
    
# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        restaurant.delete()
        return redirect("open_show_restaurant")  # make sure this view exists!
    
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'update_menu.html', 
{"itemList": itemList, "restaurant": restaurant})


def update_menu(request,restaurant_id ):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        
        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return render(request, 'admin_home.html')
    
#To view Menu
def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'customer_menu.html', 
                {"itemList": itemList, "restaurant": restaurant,"username": username})  


#veiw reports
def view_reports(request):
    # High-level stats
    total_restaurants = Restaurant.objects.count()
    total_items = Item.objects.count()

    # Avg rating across all restaurants
    avg_rating = Restaurant.objects.aggregate(Avg("rating"))["rating__avg"]

    # Items count grouped by restaurant
    restaurants_with_item_counts = Restaurant.objects.annotate(item_count=Count("items"))

    context = {
        "total_restaurants": total_restaurants,
        "total_items": total_items,
        "avg_rating": round(avg_rating, 2) if avg_rating else "N/A",
        "restaurants_with_item_counts": restaurants_with_item_counts,
    }
    return render(request, "admin_reports.html", context)


def manage_orders(request, restaurant_id):
    """
    Admin view to list all orders for a specific restaurant
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Assuming your Order model has a ForeignKey to Restaurant
    orders = Order.objects.filter(restaurant=restaurant).order_by('-created_at')  # newest first

    return render(request, 'manage_orders.html', {
        "restaurant": restaurant,
        "orders": orders
    })










#user side 
def add_to_cart(request, item_id, username):
    item = Item.objects.get(id=item_id)
    customer = Customer.objects.get(username=username)

    cart, created = Cart.objects.get_or_create(customer=customer)
    cart.items.add(item)

    # Redirect to cart page
    return redirect('show_cart', username=username)

def show_cart(request, username):
    customer = Customer.objects.get(username=username)
    cart = Cart.objects.filter(customer=customer).first()

    if cart:
        items = cart.items.all()
        total_price = cart.total_price()
    else:
        items = []
        total_price = 0

    return render(request, "cart.html", {
        "cart_items": items,     # ✅ what template should use
        "total_price": total_price,
        "username": username,
    })

def remove_from_cart(request, item_id, username):
    # Get customer
    customer = get_object_or_404(Customer, username=username)

    # Get cart for this customer
    cart = Cart.objects.filter(customer=customer).first()

    if cart:
        # Get the item
        item = get_object_or_404(Item, id=item_id)

        # Remove item from cart
        cart.items.remove(item)

    # Redirect back to cart page
    return redirect("show_cart", username=username)

def customer_home(request, username):
    restaurant = Restaurant.objects.all()
    return render(request, 'customer_home.html', {"restaurant": restaurant, "username": username})


# Checkout View

def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })


# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Generate order ID and time
    order_id = str(uuid.uuid4())[:8].upper()   # short unique ID
    order_time = timezone.now().strftime("%d %B %Y, %I:%M %p")

    # Clear cart
    if cart:
        cart.items.clear()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'order_id': order_id,
        'order_time': order_time,
    })