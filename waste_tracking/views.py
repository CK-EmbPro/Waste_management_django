from django.shortcuts import render, redirect, get_object_or_404
from .models import Waste 
from .forms import WasteForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="users:user_login")
def waste_list(request):
    wastes = Waste.objects.all()

    # Check if the user has a 'role' attribute
    if hasattr(request.user, 'role'):
        if request.user.role == 'collector':
            template = 'waste_tracking/collector/waste_list.html'
        elif request.user.role == 'normal_user':
            template = 'waste_tracking/normal_user/waste_list.html'
        else:
            # Redirect for invalid roles
            return redirect("users:user_login")
    else:
        # Redirect for unauthenticated users
        return redirect("users:user_login")

    return render(request, template, {'wastes': wastes})

def add_waste(request):
    if request.method == 'POST':
        form= WasteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wastes:waste_list')
        
    else: 
        form = WasteForm()
    
    return render(request, 'waste_tracking/add_waste.html', {'form': form})


def edit_waste(request, id):
    waste = get_object_or_404(Waste, id=id )
    if request.method == 'POST':
        form = WasteForm(request.POST, instance=waste)
        if form.is_valid():
            form.save()
            return redirect("wastes:waste_list")

    else: 
        form = WasteForm(instance=waste)
        
    return render(request, "waste_tracking/edit_waste.html", {'form': form})


def delete_waste(request, id):
    waste = get_object_or_404(Waste, id=id)
    waste.delete()
    return redirect('wastes:u_waste_list')

def collector_dashboard(request):
    # Collected wastes grouped by month
    collected_wastes_list = Waste.objects.filter(is_collected=True)\
        .annotate(month=TruncMonth('date_collected'))\
        .values('month')\
        .annotate(total_weight=Sum('weight'))\
        .order_by('month')

    # Not collected wastes grouped by month
    not_collected_wastes_list = Waste.objects.filter(is_collected=False)\
        .annotate(month=TruncMonth('date_collected'))\
        .values('month')\
        .annotate(total_weight=Sum('weight'))\
        .order_by('month')

    # Extract months and weights
    collected_months = [waste['month'].strftime('%B %Y') for waste in collected_wastes_list]
    collected_weights = [waste['total_weight'] for waste in collected_wastes_list]

    not_collected_months = [waste['month'].strftime('%B %Y') for waste in not_collected_wastes_list]
    not_collected_weights = [waste['total_weight'] for waste in not_collected_wastes_list]

    # Combine all months for consistency
    all_months = sorted(set(collected_months + not_collected_months))

    # Fill missing data for collected and not collected wastes
    def fill_missing_data(months, weights, all_months):
        filled_weights = []
        for month in all_months:
            if month in months:
                filled_weights.append(weights[months.index(month)])
            else:
                filled_weights.append(0)
        return filled_weights

    collected_weights = fill_missing_data(collected_months, collected_weights, all_months)
    not_collected_weights = fill_missing_data(not_collected_months, not_collected_weights, all_months)

    return render(request, "waste_tracking/collector/dashboard.html", {
        'collected_wastes': collected_weights,
        'non_collected_wastes': not_collected_weights,
        'months_list': all_months
    })
    
    
def normaluser_dashboard(request):
    biodegradable_wastes_list = Waste.objects.filter(category='biodegradable')\
        .annotate(month=TruncMonth('date_collected'))\
        .values('month')\
        .annotate(total_weight=Sum('weight'))\
        .order_by('month')
        
    non_biodegradable_wastes_list = Waste.objects.filter(category='non_biodegradable')\
        .annotate(month=TruncMonth('date_collected'))\
        .values('month')\
        .annotate(total_weight=Sum('weight'))\
        .order_by('month')

    # Extract the months and total weights for both biodegradable and non-biodegradable wastes
    biodegradable_months = [waste['month'].strftime('%B %Y') for waste in biodegradable_wastes_list]
    biodegradable_weights = [waste['total_weight'] for waste in biodegradable_wastes_list]

    non_biodegradable_months = [waste['month'].strftime('%B %Y') for waste in non_biodegradable_wastes_list]
    non_biodegradable_weights = [waste['total_weight'] for waste in non_biodegradable_wastes_list]

    # Combine both lists of months to ensure a complete list of months across both categories
    all_months = sorted(set(biodegradable_months + non_biodegradable_months))

    # Fill missing data for months where a category doesn't have data
    def fill_missing_data(months, weights, all_months):
        filled_months = []
        filled_weights = []
        for month in all_months:
            if month in months:
                filled_months.append(month)
                filled_weights.append(weights[months.index(month)])
            else:
                filled_months.append(month)
                filled_weights.append(0)
        return filled_months, filled_weights

    # Fill missing months for both categories
    biodegradable_months, biodegradable_weights = fill_missing_data(biodegradable_months, biodegradable_weights, all_months)
    non_biodegradable_months, non_biodegradable_weights = fill_missing_data(non_biodegradable_months, non_biodegradable_weights, all_months)

    return render(request, "waste_tracking/normal_user/dashboard.html", {
        'biodegradable_wastes': biodegradable_weights,
        'non_biodegradable_wastes': non_biodegradable_weights,
        'months_list': all_months
    })
def biodegradable_wastes(request):
    biodegradable_wastes = Waste.objects.filter(category = 'biodegradable')
    return render(request, "waste_tracking/normal_user/biodegradable.html", {'wastes':biodegradable_wastes })


def non_biodegradable_wastes(request):
    non_biodegradable_wastes_list = Waste.objects.filter(category = 'non_biodegradable')
    return render(request, "waste_tracking/normal_user/non_biodegradable.html", {'wastes':non_biodegradable_wastes_list })


def collected_wastes(request):
    collected_wastes_list = Waste.objects.filter(is_collected = True)
    return render(request, "waste_tracking/collector/collected.html", {'wastes': collected_wastes_list})


def not_collected_wastes(request):
    not_collected_wastes_list = Waste.objects.filter(is_collected = False)
    return render(request, "waste_tracking/collector/not_collected.html", {'wastes': not_collected_wastes_list})

def mark_as_collected(request, waste_id):
    waste = get_object_or_404(Waste, id = waste_id)
    
    if not waste.is_collected:
        waste.is_collected = True
        waste.save()
        messages.success(request, 'Waste marked as collected successfully')
    else:
        messages.error(request, "This waste has already been collected")
        
    return redirect("wastes:not_collected_wastes")