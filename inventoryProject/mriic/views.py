from django.shortcuts import render,redirect, get_object_or_404
from .forms import NewUserForm,ItemForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Item
from django.core.paginator import Paginator
from .forms import *
# Create your views here.
# for users

query_name = None

def itemDesc(request,Item_id):
      my_item=get_object_or_404(Item,pk=Item_id)
      return render(request,'mriic/itemDesc.html',{'my_item':my_item})

def item_add(request):
    form=ItemForm()
    if request.method == 'POST':
        ac = request.POST.get('action')
        if ac == 'save':
            val = request.POST.get('cat_name')
            try:
                obj = Category.objects.create(name=val)
                obj.save()
                print(f'{val} has been added successfully!')
            except:
                messages.error(request, f'Integrity Error: field {val} already exists!')
        elif ac == 'submit':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        elif ac == 'delete':
            val = request.POST.get('cat_name')
            try:
                obj = Category.objects.filter(name=val)
                obj.delete()
                print(f'{val} has been deleted successfully!')
            except:
                messages.error(request, f'Value Error: field {val} does not exist!')
    else:
        form = ItemForm()
    return render(request, 'mriic/item.html', {'form': form})

def search(request):
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            
            results = Item.objects.filter(name__contains=query_name)
            return render(request, 'mriic/search.html', {"results":results})
    return render(request, 'mriic/index.html')

def home(request):
    
        contact_list = Item.objects.all().filter(featured=True)
        paginator = Paginator(contact_list, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
	    # my_item=Item.objects.all()contact_list
        return render(request, 'mriic/index.html', {'page_obj': page_obj})

def signup_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
                        
			login(request, user)
			messages.success(request, "Signup successful." )
			return redirect(home)
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="mriic/signup.html", context={"signup_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			# username = request.POST('username')
			# password = request.POST('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect(home)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="mriic/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect(home) 

def chk(i,request,n,x):
	if i==1:
		messages.success(request, f"value for {n} has been edited to {x}!")
		return None
	else:
		pass

def filter_item(request):
    categories = Category.objects.all() 
    items = Item.objects.all() 
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories') 
        if selected_categories:
            items = Item.objects.filter(category__name__in=selected_categories) 
    context = {'categories': categories, 'items': items}
    return render(request, "mriic/filter.html", context)

@login_required
@user_passes_test(lambda u : u.is_staff)
def inv(request):
    if request.method == 'POST':
        results=Item.objects.all()
        context={
            "results":results
        }
        # print(f"{request.POST.get('search')}  {type(request.POST.get('search'))}")
        s_val = request.POST.get('search')
        r_val = request.POST.get('action')
        if s_val == '1':
            s_name = request.POST.get('s_name')
            results = Item.objects.filter(name__contains = s_name)
            context={
                "results":results
            }        
            return render(request, "mriic/inventory.html",context)
        
        if r_val == 'save':
            feat = request.POST.get('isFeatured')
            x = int(request.POST.get('qty'))
            nval = str(request.POST.get('item_name')).strip()
            obj = Item.objects.get(name=nval)
            db_x = obj.item_qty
            db_feat = obj.featured
            if x is not db_x:
                chk(Item.objects.filter(name=nval).update(item_qty=x),request,nval,x)
            if feat and (feat is not db_feat):
                Item.objects.filter(name=nval).update(featured=True)
            elif feat is None and (db_feat is True):
                Item.objects.filter(name=nval).update(featured=False)

        
        if r_val=='delete':
            nval = str(request.POST.get('item_name')).strip()
            Item.objects.filter(name=nval).delete()

        return render(request,"mriic/inventory.html", context)
    
    else:
        results=Item.objects.all()
        context={
            "results":results
        }
        return render(request,"mriic/inventory.html", context)

