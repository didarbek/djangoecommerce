from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from .forms import UserForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item,Profile,Category,Sex
from django.views.generic import ListView
from django.db.models import Q, Count

# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None

def product_page(request):
    return render(request,'product-page.html')

def cart(request):
    return render(request,'cart.html')

def profile(request):
    return render(request,'profile.html')

class ItemList(ListView):
    model = Item
    paginate_by = 8
    template_name = 'home.html'

    # def get_context_data(self,**kwargs):
    #     context = super(ItemList,self).get_context_data(**kwargs)
    #     context['slides'] = Carousel.objects.all()
    #     return context

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
    return render(request,template_name,{
        'item':item,
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