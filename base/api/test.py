from base.model_invoice import Event
from base.models import N_State, Customer, Address, Business


def test_set_address():

    state = N_State.objects.first()
    lista = Customer.objects.all()

    for cust in lista:
        ad = Address(first_line="Calle del medio", zip=10400, city="Havana", state=state)
        ad.save()
        cust.address = ad
        cust.save()
        print(cust)

def test_set_Event():

    state = N_State.objects.first()
    lista = Event.objects.all()

    for cust in lista:
        ad = Address(first_line="Calle del medio", zip=10400, city="Havana", state=state)
        ad.save()
        cust.address = ad
        cust.save()
        print(cust)

def test_set_business():

    state = N_State.objects.first()
    lista = Business.objects.all()

    for cust in lista:
        ad = Address(first_line="Calle del medio", zip=10400, city="Havana", state=state)
        ad.save()
        cust.address = ad
        cust.save()
        print(cust)