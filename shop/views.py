from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from . models import *
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    trending_product=Product.objects.filter(trending=1)
    return render(request,'home.html',{'trending_product':trending_product})


def register(request):
    form=CustomUserForm()
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,'registraion succcess you can login now...!')
          return redirect('login')
        
    return render(request,'register.html',{'form':form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=name,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or Password")
                return redirect('login')
        return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,'collections.html',{'category':category})

def collections_view(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'products.html',{'products':products,'category':name})
    else:
        messages.warning(request,"no such category found")
        return redirect('collections')
    

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname ,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"productdetails.html",{'products':products})
        else:
            messages.error(request,"No such product found")
            return redirect('collectionsview', name='default')
    else:
        messages.error(request,"No such category found")
        return redirect('collectionsview', name='default')
    
def add_To_Cart(request):   
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart Success'},status=200)
                    else:
                        return JsonResponse({'status':'Product Not Available'},status=200)
        else:
            return JsonResponse ({'status':'Login to Add Cart'},status=200) 
    else:
        return JsonResponse ({'status':'Invalid Access'},status=200)    
    
def cart_page(request):
    
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        total=0
        for item in cart:
            total += item.total_cost
        return render(request,"cart.html",{'cart':cart,'total':total})
    else:
        return redirect("/")
    
def remove_page(request,id):
    remove_cart=Cart.objects.get(id=id)
    remove_cart.delete()
    return redirect('cart')


def favourite_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                   Favourite.objects.create(user=request.user,product_id=product_id)
                   return JsonResponse ({'status':'Product Add to Favourite'},status=200) 
            
        else:
            return JsonResponse ({'status':'Login to Add Favourite'},status=200) 
    else:
        return JsonResponse ({'status':'Invalid Access'},status=200)    
    
def favourite_view(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"favourite.html",{'fav':fav})
    else:
        return redirect("/")
    
def remove_fav(request,id):
    if request.user.is_authenticated:
       remove_fav=Favourite.objects.get(id=id)
       remove_fav.delete()
       return redirect('favourite_view')
    else:
       return redirect("/")
    
    
    
    
    
    
    
    
   
    
 