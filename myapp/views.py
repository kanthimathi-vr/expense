from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm, RegisterForm
from django.utils.timezone import now
from datetime import date

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'expenses/register.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()
    month_expenses = Expense.objects.filter(user=user, date__year=today.year, date__month=today.month)

    total_spent = month_expenses.aggregate(total=Sum('amount'))['total'] or 0

    category_breakdown = month_expenses.values('category').annotate(total=Sum('amount'))

    context = {
        'total_spent': total_spent,
        'category_breakdown': category_breakdown,
    }
    return render(request, 'expenses/dashboard.html', context)

@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_create_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_update_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def admin_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    users = User.objects.all()
    return render(request, 'expenses/admin_view.html', {'users': users})
