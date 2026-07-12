from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):

    expenses = Expense.objects.select_related("vehicle").all()

    context = {
        "expenses": expenses,
    }

    return render(
        request,
        "expenses/expense_list.html",
        context,
    )


@login_required
def expense_create(request):

    form = ExpenseForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Expense added successfully."
            )

            return redirect("expense_list")

    return render(
        request,
        "expenses/expense_form.html",
        {
            "form": form,
            "title": "Add Expense",
        },
    )