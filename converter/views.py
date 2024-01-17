from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from converter.models import Currency


def currency_list(request):
    currency_list = Currency.objects.all()

    currencies_per_page = 50
    paginator = Paginator(currency_list, currencies_per_page)

    page = request.GET.get('page')
    try:
        currencies = paginator.page(page)
    except PageNotAnInteger:
        currencies = paginator.page(1)
    except EmptyPage:
        currencies = paginator.page(paginator.num_pages)

    return render(request, 'currency_list.html', {'currencies': currencies})
