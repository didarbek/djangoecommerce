from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from .forms import UserForm,ProfileForm,CheckoutForm,CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item,Profile,Category,Sex,OrderItem,Order,Address,Payment,Comment
from django.views.generic import ListView,View
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.views.generic import DetailView
from django.http import HttpResponseRedirect,Http404

# Create your views here.

stripe.api_key = "sk_test_LV84oXAHus7lmnQAluhvBNhD007lApVItl"

def is_valid_queryparam(param):
    return param != '' and param is not None

def profile(request):
    return render(request,'profile.html')

class ItemList(ListView):
    model = Item
    paginate_by = 8
    template_name = 'home.html'

class MenItemList(ListView):
    model = Item
    paginate_by = 8
    template_name = 'men_form.html'
    
    def get_queryset(self):
        men_qs  = super().get_queryset()
        return men_qs.filter(sex__name__exact='Men')

class WomenItemList(ListView):
    model = Item
    paginate_by = 8
    template_name = 'women_form.html'
    
    def get_queryset(self):
        women_qs  = super().get_queryset()
        return women_qs.filter(sex__name__exact='Women')

class SaleItemList(ListView):
    model = Item  
    paginate_by = 8
    template_name = 'sale_form.html'

    def get_queryset(self):
        sale_qs  = super().get_queryset()
        return sale_qs.filter(discount_price__isnull=False)

@login_required
@transaction.atomic
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('core:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'account_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def filter(request):
    qs = Item.objects.all()
    categories = Category.objects.all()
    sexes = Sex.objects.all()
    title_contains_query = request.GET.get('title_contains')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    sex = request.GET.get('sex')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    if is_valid_queryparam(price_min):
        qs = qs.filter(price__gte=price_min)

    if is_valid_queryparam(price_max):
        qs = qs.filter(price__lt=price_max)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(category__name=category)

    if is_valid_queryparam(sex) and sex != 'Choose...':
        qs = qs.filter(sex__name=sex)

    return qs

def FilterView(request):
    qs = filter(request)
    context = {
        'queryset': qs,
        'categories': Category.objects.all(),
        'sexes': Sex.objects.all()
    }
    return render(request, "filter_search.html", context)

def product_detail(request,pk):
    template_name = 'product-page.html'
    item = get_object_or_404(Item,pk=pk)
    comments = item.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = item
            new_comment.save()    
            return HttpResponseRedirect(item.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request,template_name,{
        'item':item,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
    })

class SearchResultsView(ListView):
    model = Item
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('title','description')
        object_list = Item.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            }
            return render(self.request,'cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False,
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This product quantity was updated.")
            return redirect("core:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item quantity was updated.")
    return redirect("core:cart")

@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered = False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This product was removed from your cart.")
            return redirect("core:cart")
        else:
            messages.info(request, "This product was not in your cart.")
            return redirect("core:product_detail", pk=pk)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product_detail", pk=pk)

@login_required
def remove_single_item_from_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This product quantity was updated.")
            return redirect("core:cart")
        else:
            messages.info(request, "This product was not in your cart.")
            return redirect("core:product_detail",pk=pk)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product_detail",pk=pk)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
            return render(self.request, "checkout-page.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkoutpage")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkoutpage')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    firstname = form.cleaned_data.get('first_name')
                    lastname = form.cleaned_data.get('last_name')
                    if is_valid_form([shipping_address1,shipping_country,shipping_zip,firstname,lastname]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            first_name=firstname,
                            last_name=lastname
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()
                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:cart")
            
class PaymentView(View):
    def get(self,*args,**kwargs):
        return render(self.request,"payment.html")

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request,"Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.warning(self.request,F"{e.error.message}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            messages.warning(self.request,"Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request,"Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            messages.warning(self.request,"Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            messages.warning(self.request,"Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            messages.warning(self.request,"Something went wrong. Your were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            messages.warning    (self.request,"A serious error occurred. We have been notifed.")
            return redirect("/")

class ShoesView(ListView):
    model = Item
    template_name = 'shoes.html'
    paginate_by = 8

    def get_queryset(self):
        shoes_qs  = super().get_queryset()
        return shoes_qs.filter(category__name='Shoes')

class ClothesView(ListView):
    model = Item
    template_name = 'clothes.html'
    paginate_by = 8

    def get_queryset(self):
        clothes_qs  = super().get_queryset()
        return clothes_qs.filter(category__name='Clothes')

class AccessoriesView(ListView):
    model = Item
    template_name = 'accessories.html'
    paginate_by = 8

    def get_queryset(self):
        accessories_qs  = super().get_queryset()
        return accessories_qs.filter(category__name='Accessories')

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('core:product_detail', pk=comment.item.pk)
