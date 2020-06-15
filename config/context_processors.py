from drugs.models import DrugItem
from customers.models import Customer
from expenses.models import Expenses

from order.models import DrugOrder


def common(request):
    try:
        total_drugs = DrugItem.objects.all()
        total_customers = Customer.objects.all()
        total_orders = DrugOrder.objects.all()
        total_expenses = Expenses.objects.all()

        context = {
            'total_drugs': total_drugs,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_expenses': total_expenses,
        }
        return context
    except:
        pass


def session_handler(request):
    try:
        if 'customer' in request.session:
            context = {
                'session_customer': request.session['customer']
            }
            return context
        else:
            context = {
                'session_customer':None
            }
            return context

    except TypeError:
        pass
