from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, ListView

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ItemForm, SearchForm, ClaimRequestForm
from .models import Category, Item, ClaimRequest


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('home')

def index(request):
    return render(request,"mainapp/index.html")

class UnclaimedItems(ListView):
    model = Item
    template_name = 'mainapp/lost-items.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Item.objects.filter(category__name=category,item_status='Unclaimed')
        return Item.objects.filter(item_status='Unclaimed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.request.GET.get('category')
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'mainapp/item-detail.html'
    context_object_name = 'item'

@login_required(login_url="login")
def report(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            form.save_m2m()
            return redirect("items")
    else:
        form = ItemForm()

    return render(request, 'mainapp/report-found.html', {"form": form})

def search(request):
    search_text = request.GET.get("search", "").strip()
    items = []
    form = SearchForm(request.GET)
    if form.is_valid() and search_text:
        search_text = form.cleaned_data["search"]
        items = Item.objects.filter(name__icontains=search_text)

    return render(request, "mainapp/search-item.html", {
        "form": form,
        "items": items,
        "search_text": search_text
    })

@login_required
def claim_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.user == request.user:
        return redirect('item-detail', pk=pk)

    if request.method == 'POST':
        form = ClaimRequestForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.claimant = request.user
            claim.receiver = item.user
            claim.found_item = item
            claim.contact_info = request.user.phone_number
            claim.save()
            return redirect('item-detail', pk=pk)
    else:
        form = ClaimRequestForm()

    return render(request, 'mainapp/claim_form.html', {'form': form, 'item': item})


@login_required
def profile(request):
    user = request.user
    sent_claim_requests = ClaimRequest.objects.filter(claimant=user)
    received_claim_requests = ClaimRequest.objects.filter(receiver=user)

    context = {
        'user': user,
        'sent_claim_requests': sent_claim_requests,
        'received_claim_requests': received_claim_requests
    }
    return render(request, 'mainapp/profile.html', context)

@login_required
def approve_claim(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id)

    if claim.receiver == request.user:
        claim.status = 'approved'
        claim.save()

        item = claim.found_item
        item.item_status = Item.StatusChoices.CLAIMED
        item.save()

        ClaimRequest.objects.filter(
            found_item=item,
            status='pending'
        ).exclude(id=claim_id).update(status='rejected')

    return redirect('profile')

@login_required
def reject_claim(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id)
    if claim.receiver == request.user:
        claim.status = 'rejected'
        claim.save()
    return redirect('profile')
