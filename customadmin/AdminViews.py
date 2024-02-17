from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from accounts.models import *
from orders.models import Order, Payment
from store.models import *
from category.models import Category
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

@login_required(login_url='admin_login')
def admin_home(request):

    orders_count = Order.objects.all().count()
    completed_orders = Order.objects.filter(status='Completed')
    confimed_orders = Order.objects.filter(status='Confirmed')
    delivered_orders = Order.objects.filter(status='Delivered')
    

    context ={
        'user': request.user,
        'orders_count':orders_count,
        'completed_orders':completed_orders,
        'confimed_orders':confimed_orders,
        'delivered_orders':delivered_orders,

    }

    return render(request,'customadmin/admin_home.html', context)
#============================Categories =======================================================================

class CategoriesListView(ListView):
    model = Category
    template_name = "customadmin/categories/category_list.html"
    context_object_name = "categories"

class CategoriesCreate(SuccessMessageMixin, CreateView):
    model = Category
    success_message = "New category added!"
    fields = "__all__"
    template_name = "customadmin/categories/category_create.html"


class CategoriesUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    success_message = " Category updated!"
    fields = "__all__"
    template_name = "customadmin/categories/category_update.html"

@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(SuccessMessageMixin,DeleteView):
    model = Category
    template_name = 'customadmin/categories/category_delete.html'  
    success_message = " User {{category.cat_name}} deleted!"
    success_url = reverse_lazy('category_list') 

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('pk')
        return Category.objects.get(pk=category_slug)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User Account'
        return context
    
    def get_success_message(self, cleaned_data):
        return f"Category deleteded successfully."
#====================================Users=================================================================================
class UsersListView(ListView):
    model = Account
    template_name = "customadmin/user_list.html"
    context_object_name = "users"

@method_decorator(login_required, name='dispatch')
class UserCreateView(SuccessMessageMixin, CreateView):
    model = Account
    template_name = "customadmin/user_create.html"
    fields = ['first_name','last_name','username','email','password','is_admin','is_active','is_merchant','is_staff','is_blocked']
    success_message = "New user added!"
    success_url = reverse_lazy('users_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        # Customize the success message based on the form data
        # You can access form.cleaned_data to retrieve form input values
        return f"User {cleaned_data['username']} created successfully."

@method_decorator(login_required, name='dispatch')    
class UserUpdate(SuccessMessageMixin, UpdateView):
    model = Account
    template_name = "customadmin/user_update.html"
    fields = ['first_name','last_name','username','email','password','is_admin','is_active','is_merchant','is_staff','is_blocked']
    success_message = "New user added!"
    success_url = reverse_lazy('users_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"User {cleaned_data['username']} updated successfully."

@method_decorator(login_required, name='dispatch')
class UserDeleteView(SuccessMessageMixin,DeleteView):
    model = Account
    template_name = 'customadmin/user_delete.html'  
    success_message = " User {{user.ussername}} deleted!"
    success_url = reverse_lazy('users_list') 

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return Account.objects.get(pk=user_id)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User Account'
        return context
    
    def get_success_message(self, cleaned_data):
        return f"User deleteded successfully."

#============================================Products=======================================================================
class ProductListView(ListView):
    model = Product
    template_name = "customadmin/products/product_list.html"
    context_object_name = "products"

@method_decorator(login_required, name='dispatch')
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = "customadmin/products/add_product.html"
    fields = '__all__'
    success_message = "New product added!"
    success_url = reverse_lazy('products_list') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.all().order_by('cat_name')
        #form.fields['merchant'].queryset = Account.objects.filter(is_merchant=True)
        return form

    def form_valid(self, form):
        # Handle the creation of associated ProductImages
        images = self.request.FILES.getlist('images')
        for image in images:
            product_image = ProductImages(images=image, product=self.object)
            product_image.save()

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Product {cleaned_data['product_name']} created successfully."

@method_decorator(login_required, name='dispatch')
class ProductUpdate(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = "customadmin/products/product_update.html"
    fields = '__all__'
    success_message = "The Product added!"
    success_url = reverse_lazy('products_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"Product: {cleaned_data['product_name']} updated successfully."
    
@method_decorator(login_required, name='dispatch')
class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'customadmin/products/product_delete.html'
    success_message = "Product {{ product.product_name }} deleted successfully!"
    success_url = reverse_lazy('products_list')

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        return Product.objects.get(pk=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Product'
        return context
#========================Product Images=============================================================================
class ProductImagesListView(ListView):
    template_name = "customadmin/products/product_images.html"
    context_object_name = "images"

    def get_queryset(self):
        # Get the product ID from the URL parameter or from the view's kwargs
        product_id = self.kwargs.get('product_id')  # Assuming the URL pattern includes 'product_id'
        # Fetch the queryset of ProductImages filtered by the product ID
        queryset = ProductImages.objects.filter(product_id=product_id)
        return queryset
    

@method_decorator(login_required, name='dispatch')
class ProductImagesCreateView(SuccessMessageMixin, CreateView):
    model = ProductImages
    template_name = "customadmin/products/add_product_images.html"
    fields = '__all__'
    success_message = "New Images added!"
    success_url = reverse_lazy('products_list') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['payment'].queryset = Payment.objects.all().order_by('cat_name')
        #form.fields['merchant'].queryset = Account.objects.filter(is_merchant=True)
        return form

    def form_valid(self, form):
        # Handle the creation of associated ProductImages
        images = self.request.FILES.getlist('images')
        for image in images:
            product_image = ProductImages(images=image, product=self.object)
            product_image.save()

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Product {cleaned_data['product_name']} created successfully."


#========================Variations=============================================================================
class VariationtListView(ListView):
    model = Variation
    template_name = "customadmin/products/variation_list.html"
    context_object_name = "variations"

@method_decorator(login_required, name='dispatch')
class VariationCreateView(SuccessMessageMixin, CreateView):
    model = Variation
    template_name = "customadmin/products/add_variations.html"
    fields = '__all__'
    success_message = "New variations added!"
    success_url = reverse_lazy('variations_list') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['product'].queryset = Product.objects.all().order_by('product_name')
        return form

    #def form_valid(self, form):
    #    # Handle the creation of associated ProductImages
    #    images = self.request.FILES.getlist('images')
    #    for image in images:
    #        product_image = ProductImages(images=image, product=self.object)
    #        product_image.save()

    #    return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Variattion created successfully."

@method_decorator(login_required, name='dispatch')
class VariationUpdate(SuccessMessageMixin, UpdateView):
    model = Variation
    template_name = "customadmin/products/variation_update.html"
    fields = '__all__'
    success_message = "The Variation updated!"
    success_url = reverse_lazy('variations_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"Variation updated successfully."


@method_decorator(login_required, name='dispatch')
class VariationDeleteView(SuccessMessageMixin, DeleteView):
    model = Variation
    template_name = 'customadmin/products/variation_delete.html'
    success_message = "Variation  deleted successfully!"
    success_url = reverse_lazy('variations_list')

    def get_object(self, queryset=None):
        variation_id = self.kwargs.get('pk')
        try:
            variation = Variation.objects.get(pk=variation_id)
        except Variation.DoesNotExist:
            raise Http404("Variation does not exist")
        return variation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Variation'
        return context

#============================================Order Management=======================================================================
class OrderListView(ListView):
    model = Order
    template_name = "customadmin/orders/order_list.html"
    context_object_name = "orders"



@method_decorator(login_required, name='dispatch')
class OrderUpdate(SuccessMessageMixin, UpdateView):
    model = Order
    template_name = "customadmin/orders/order_update.html"
    fields = '__all__'
    success_message = "The order status updated!"
    success_url = reverse_lazy('orders_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce

    def get_success_message(self, cleaned_data):
        order_number = cleaned_data.get('order_number')  # Assuming 'order_number' is a field of the form
        name = cleaned_data.get('full_name')  # Assuming 'name' is a field of the form
        return f"Order: {name}-{order_number} updated successfully."


#============================================ Paymment =======================================================================
class PaymentListView(ListView):
    model = Payment
    template_name = "customadmin/orders/payment_list.html"
    context_object_name = "payments"


@method_decorator(login_required, name='dispatch')
class PaymentUpdate(SuccessMessageMixin, UpdateView):
    model = Payment
    template_name = "customadmin/orders/payment_update.html"
    fields = '__all__'
    success_message = "The order updated!"
    success_url = reverse_lazy('payment_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    
    def get_success_message(self, cleaned_data):
        payment_id = self.object.id  # Access the payment's unique identifier
        return f"Payment {payment_id} updated successfully."
    

#============================================ Offers =======================================================================
class CategoryOffers(ListView):
    model = CategoryOffer
    template_name = "customadmin/offers/category_offers.html"
    context_object_name = "offers"

class ProductOffers(ListView):
    model = Offer
    template_name = "customadmin/offers/product_offers.html"
    context_object_name = "offers"

