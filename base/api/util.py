

__author__ = 'amado'
# No importar modelos
def serialize_query(query_set, fields=[]):
    lista = []
    for ent in query_set:
        data_sl = ent.serialize(fields=fields)
        lista.append(data_sl)
    return lista
#
# def test_set_address():
#
#     state = N_State.objects.first()
#     lista = Customer.objects.all()
#
#     for cust in lista:
#         ad = Address(first_line="Calle del medio", zip=10400, city="Havana", state=state)
#         ad.customer = cust
#         ad.save()
#         print(cust)

