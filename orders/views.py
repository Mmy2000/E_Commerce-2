from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages


# Create your views here.
def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('/')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        if cart_item.product.discount:
            total += (cart_item.product.discount * cart_item.quantity)
            quantity += cart_item.quantity
        else:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_orderd=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            }
            return render(request, 'orders/payments.html', context)
        else:
          messages.error(request, 'Pls, Add your Delivery info')
          return redirect(reverse('carts:checkout'))  
    else:
        return redirect(reverse('carts:checkout'))

# def payments(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user, is_orderd=False, order_number=body['orderID'])

#     # Store transaction details inside Payment model
#     payment = Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         payment_paid = order.order_total,
#         status = body['status'],
#     )
#     payment.save()

#     order.payment = payment
#     order.is_orderd = True
#     order.save()

#     # Move the cart items to Order Product table
#     cart_items = CartItem.objects.filter(user=request.user)

#     for item in cart_items:
#         orderproduct = OrderProduct()
#         orderproduct.order_id = order.id
#         orderproduct.payment = payment
#         orderproduct.user_id = request.user.id
#         orderproduct.product_id = item.product_id
#         orderproduct.quantity = item.quantity
#         if item.product.discount:
#             orderproduct.product_price = item.product.discount
#         else:
#             orderproduct.product_price = item.product.price
#         orderproduct.ordered = True
#         orderproduct.save()

#         cart_item = CartItem.objects.get(id=item.id)
#         product_variation = cart_item.variations.all()
#         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#         orderproduct.variations.set(product_variation)
#         orderproduct.save()


#         # Reduce the quantity of the sold products
#         product = Product.objects.get(id=item.product_id)
#         product.stock -= item.quantity
#         product.save()

#     # Clear cart
#     CartItem.objects.filter(user=request.user).delete()

#    # Send order recieved email to customer
#     mail_subject = 'Thank you for your order!'
#     message = render_to_string('orders/order_recieved_email.html', {
#         'user': request.user,
#         'order': order,
#     })
#     to_email = request.user.email
#     send_email = EmailMessage(mail_subject, message, to=[to_email])
#     send_email.send()

#     # Send order number and transaction id back to sendData method via JsonResponse
#     data = {
#         'order_number': order.order_number,
#         'transID': payment.payment_id,
#         'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
#     }
#     return JsonResponse(data)

# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')

#     try:
#         order = Order.objects.get(order_number=order_number, is_orderd=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order.order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
#         return render(request, 'orders/order_complete.html', context)
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect(reverse('settings:home'))


def payments(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        order = get_object_or_404(Order, user=request.user, is_orderd=False, order_number=body['orderID'])

        # Retrieve the payment intent to confirm the payment details
        intent = stripe.PaymentIntent.retrieve(body['paymentIntentId'])

        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id=intent.id,
            payment_method=intent.payment_method_types[0],
            payment_paid=intent.amount_received / 100,  # Stripe amounts are in cents
            status=intent.status,
        )
        payment.save()

        # Update the order with payment and mark it as ordered
        order.payment = payment
        order.is_orderd = True
        order.save()

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.discount if item.product.discount else item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Assign product variations to order product
            product_variation = item.variations.all()
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # Send order number and transaction id back to sendData method via JsonResponse
        data = {
            'order_number': order.order_number,
            'payment_id': payment.payment_id,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_orderd=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect(reverse('settings:home'))
    
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('orderID')

            # Assuming you fetch the order from the database
            order = Order.objects.get(order_number=order_id)

            intent = stripe.PaymentIntent.create(
                amount=int(order.order_total * 100),  # Stripe expects the amount in cents
                currency='usd',
                metadata={'order_id': order.id}
            )

            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'total': order.order_total,
        'tax': order.tax,
        'grand_total': order.order_total + order.tax,
        'cart_items': order.orderproduct_set.all()
    }
    return render(request, 'payment.html', context)