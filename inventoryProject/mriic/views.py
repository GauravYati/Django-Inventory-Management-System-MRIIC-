from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BorrowRequestForm, ItemForm, NewUserForm
from .models import BorrowRequest, Category, Item


def is_staff_user(user):
    return user.is_authenticated and user.is_active and user.is_staff


def paginate_items(request, queryset, per_page=12):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))


def pagination_query(request):
    query = request.GET.copy()
    query.pop('page', None)
    encoded = query.urlencode()
    return f'{encoded}&' if encoded else ''


def home(request):
    featured_items = Item.objects.filter(featured=True).prefetch_related('category').order_by('name')
    return render(
        request,
        'mriic/index.html',
        {'page_obj': paginate_items(request, featured_items, 8), 'page_query': pagination_query(request)},
    )


def itemDesc(request, Item_id):
    my_item = get_object_or_404(Item.objects.prefetch_related('category', 'tags'), pk=Item_id)
    borrow_form = BorrowRequestForm(initial={'quantity': 1})
    active_borrows = my_item.borrow_requests.filter(status=BorrowRequest.APPROVED)
    return render(
        request,
        'mriic/itemDesc.html',
        {'my_item': my_item, 'borrow_form': borrow_form, 'active_borrows': active_borrows},
    )


@require_POST
def borrow_request_create(request, Item_id):
    item = get_object_or_404(Item, pk=Item_id)
    form = BorrowRequestForm(request.POST)
    if form.is_valid():
        borrow_request = form.save(commit=False)
        borrow_request.item = item
        if borrow_request.quantity > item.item_qty:
            messages.error(request, f'Only {item.item_qty} unit(s) are currently available.')
        else:
            borrow_request.save()
            messages.success(request, 'Borrow request submitted. Staff will review it before inventory is deducted.')
    else:
        messages.error(request, 'Borrow request could not be submitted. Please check the form.')
    return redirect('itemDesc', Item_id=item.pk)


def search(request):
    query_name = (request.POST.get('name') or request.GET.get('q') or '').strip()
    items = Item.objects.none()

    if query_name:
        items = (
            Item.objects.filter(
                Q(name__icontains=query_name)
                | Q(category__name__icontains=query_name)
                | Q(tags__name__icontains=query_name)
            )
            .prefetch_related('category')
            .distinct()
            .order_by('name')
        )

    return render(
        request,
        'mriic/search.html',
        {'page_obj': paginate_items(request, items), 'query': query_name, 'page_query': pagination_query(request)},
    )


def filter_item(request):
    categories = Category.objects.order_by('name')
    selected_categories = request.POST.getlist('categories') or request.GET.getlist('categories')
    items = Item.objects.prefetch_related('category').order_by('name')

    if selected_categories:
        items = items.filter(category__name__in=selected_categories).distinct()

    context = {
        'categories': categories,
        'page_obj': paginate_items(request, items),
        'selected_categories': selected_categories,
        'page_query': pagination_query(request),
    }
    return render(request, 'mriic/filter.html', context)


def signup_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful.')
            return redirect('home')
        messages.error(request, 'Registration failed. Please check the highlighted fields.')
    else:
        form = NewUserForm()

    return render(request, 'mriic/signup.html', {'signup_form': form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_staff:
                    messages.error(request, 'This login is restricted to staff accounts.')
                    return redirect('login')
                login(request, user)
                return redirect('home')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'mriic/login.html', {'login_form': form})


@require_POST
@user_passes_test(is_staff_user, login_url='login')
def logout_request(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')


@user_passes_test(is_staff_user, login_url='login')
def item_add(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'category_add':
            category_name = (request.POST.get('cat_name') or '').strip()
            if category_name:
                _, created = Category.objects.get_or_create(name=category_name)
                message = f'Category "{category_name}" added.' if created else f'Category "{category_name}" already exists.'
                messages.success(request, message)
            else:
                messages.error(request, 'Enter a category name before saving.')
            return redirect('image_upload')

        if action == 'category_delete':
            category_name = (request.POST.get('cat_name') or '').strip()
            deleted_count, _ = Category.objects.filter(name=category_name).delete()
            if deleted_count:
                messages.success(request, f'Category "{category_name}" deleted.')
            else:
                messages.error(request, f'Category "{category_name}" was not found.')
            return redirect('image_upload')

        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'"{item.name}" has been added to inventory.')
            return redirect('inv')
        messages.error(request, 'Item could not be saved. Please check the form.')
    else:
        form = ItemForm()

    return render(request, 'mriic/item.html', {'form': form, 'categories': Category.objects.order_by('name')})


@user_passes_test(is_staff_user, login_url='login')
def item_edit(request, Item_id):
    item = get_object_or_404(Item, pk=Item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" updated.')
            return redirect('inv')
        messages.error(request, 'Resource could not be updated. Please check the form.')
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        'mriic/item.html',
        {'form': form, 'categories': Category.objects.order_by('name'), 'editing_item': item},
    )


@require_POST
@user_passes_test(is_staff_user, login_url='login')
def borrow_request_update(request, request_id):
    action = request.POST.get('action')
    with transaction.atomic():
        borrow_request = get_object_or_404(
            BorrowRequest.objects.select_for_update().select_related('item'),
            pk=request_id,
        )
        item = Item.objects.select_for_update().get(pk=borrow_request.item_id)

        if action == 'approve' and borrow_request.status == BorrowRequest.PENDING:
            if borrow_request.quantity > item.item_qty:
                messages.error(request, f'Cannot approve "{item.name}". Only {item.item_qty} unit(s) are available.')
            else:
                item.item_qty -= borrow_request.quantity
                item.save(update_fields=['item_qty'])
                borrow_request.status = BorrowRequest.APPROVED
                borrow_request.save(update_fields=['status', 'updated_at'])
                messages.success(request, f'Approved borrow request for "{item.name}".')

        elif action == 'reject' and borrow_request.status == BorrowRequest.PENDING:
            borrow_request.status = BorrowRequest.REJECTED
            borrow_request.save(update_fields=['status', 'updated_at'])
            messages.info(request, f'Rejected borrow request for "{item.name}".')

        elif action == 'return' and borrow_request.status == BorrowRequest.APPROVED:
            item.item_qty += borrow_request.quantity
            item.save(update_fields=['item_qty'])
            borrow_request.status = BorrowRequest.RETURNED
            borrow_request.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'Marked "{item.name}" as returned.')

        else:
            messages.error(request, 'That borrow request action is not valid for the current status.')

    return redirect('inv')


@user_passes_test(is_staff_user, login_url='login')
def inv(request):
    item_id = request.GET.get('item')
    search_term = (request.GET.get('q') or '').strip()
    results = Item.objects.prefetch_related('category').order_by('name')
    borrow_requests = BorrowRequest.objects.select_related('item').filter(
        status__in=[BorrowRequest.PENDING, BorrowRequest.APPROVED]
    )

    if item_id:
        results = results.filter(pk=item_id)
    elif search_term:
        results = results.filter(name__icontains=search_term)

    if request.method == 'POST':
        item = get_object_or_404(Item, pk=request.POST.get('item_id'))
        action = request.POST.get('action')

        if action == 'save':
            try:
                item.item_qty = max(int(request.POST.get('qty') or 0), 0)
            except ValueError:
                messages.error(request, 'Quantity must be a valid number.')
                return redirect(f'{request.path}?item={item.pk}')
            item.featured = request.POST.get('isFeatured') == 'on'
            item.save(update_fields=['item_qty', 'featured'])
            messages.success(request, f'"{item.name}" updated.')
            return redirect(f'{request.path}?item={item.pk}')

        if action == 'delete':
            item_name = item.name
            item.delete()
            messages.success(request, f'"{item_name}" deleted.')
            return redirect('inv')

    return render(
        request,
        'mriic/inventory.html',
        {
            'results': results,
            'search_term': search_term,
            'total_items': Item.objects.count(),
            'featured_items': Item.objects.filter(featured=True).count(),
            'low_stock_items': Item.objects.filter(item_qty__lte=2).count(),
            'borrow_requests': borrow_requests,
            'pending_borrow_count': borrow_requests.filter(status=BorrowRequest.PENDING).count(),
            'active_borrow_count': borrow_requests.filter(status=BorrowRequest.APPROVED).count(),
        },
    )
