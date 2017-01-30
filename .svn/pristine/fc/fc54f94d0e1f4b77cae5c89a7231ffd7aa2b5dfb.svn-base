import json
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from base.api.views import business
from base.models import Business
from base.prodserv_forms import PositionForm, WorkerForm, ServiceForm, IngredientsForm
from base.prodserv_models import Product, ProductPrice, Service, Position, Worker, Ingredients, Measure, Recipe, \
    ServiceWorkers

__author__ = 'maykel'


class ProductList(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        data = []
        items = []
        for product in products:
            product_data = {'id': product.id,
                       'category':
                           {'description': product.category.description,
                            'id': product.category.id},
                                    'name': product.name,
                                    'description': product.description,
                                    'recipe': {'name': product.recipe.name,
                                               'id': product.recipe.name}
                       }
            range = ProductPrice.objects.filter(product=product)
            for item in range:
                items.append({'min': item.min, 'max': item.max, 'price': item.serializable_value('price')})
            product_data['items'] = items
            data.append(product_data)
        return JsonResponse((data), safe=False, status=200)

class ServicesList(View):
    def get(self, request, *args, **kwargs):
        w = Service.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        print(w)
        workers = []

        data = []
        if w:
            for item in w:
                workers.append(ServiceWorkers.objects.filter(service=item))
            data.append({'id':item.id, 'name': item.name, 'description': item.description, 'tarifa_horaria': float(item.tarifa_horaria), 'workers':[] })
        return JsonResponse(list(data), safe=False, status=200)

class ServicesAdd(View):
    form_class = ServiceForm
    def post(self, request, *args, **kwargs):
        data = (json.loads(request.body.decode()))
        print(data)
        form = self.form_class(data)
        if form.is_valid():
            w = Service()
            w.name = data.get('name')
            w.description = data.get('description')
            w.tarifa_horaria = data.get('tarifa_horaria')
            w.business = Business.objects.get_business_by_user(self.request.user)
            try:
                w.save()
                for item in data.get('workers'):
                    ws = ServiceWorkers()
                    ws.service = Service.objects.filter(id=w.id).first()
                    ws.worker = Worker.objects.filter(id=item.get('id')).first()
                    try:
                        ws.save()
                    except:
                        return JsonResponse({'errors':'Error de Servidor'}, safe=False, status=500)
                data_ = {'id': w.id, 'name': w.name, 'description': w.description, 'tarifa_horaria': w.tarifa_horaria}
                return JsonResponse(data=data_, status=200)
            except:
                return HttpResponse(status=500)
        else:
            return JsonResponse(form.errors, safe=False, status=400)

class ServicesEdit(View):
    form_class = ServiceForm
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        data = (json.loads(request.body.decode()))
        if id:
            p = Service.objects.filter(id=id).first()
            p.name = data.get('name')
            p.description = data.get('description')
            p.tarifa_horaria = data.get('tarifa_horaria')
            p.business = Business.objects.get_business_by_user(self.request.user)
            try:
                p.save()
                data_ = {'id': p.id, 'name': p.name, 'description': p.description, 'tarifa_horaria': p.tarifa_horaria}
                return JsonResponse(data=data_, status=200)
            except:
                return JsonResponse({'errors': 'Database error'}, safe=False, status=500)
        else:
            return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)

class ServicesRemove(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()
        data = json.loads(request.body.decode())
        ids = [service.get('id') for service in data]
        try:
            deleted = Service.objects.bulk_delete(ids=ids, business=business)
            return JsonResponse(status=200, data={'deleted': deleted})
        except Exception as e:
            return HttpResponse(status=400)

class PositionList(View):
    def get(self, request, *args, **kwargs):
        categ = Position.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        data=[]
        if categ:
            for item in categ:
                data.append({'id':item.id,'name':item.name, 'description': item.description})
        return JsonResponse(data, safe=False, status=200)

class PositionAdd(View):
    form_class = PositionForm
    def post(self, request, *args, **kwargs):
        # data = {'description': 'Mesero'}/
        data = (json.loads(request.body.decode()))
        form = self.form_class(data)
        if form.is_valid():
            p = Position()
            p.description = data.get('description')
            p.name = data.get('name')
            p.business = Business.objects.get_business_by_user(self.request.user)
            try:
                p.save()
                return HttpResponse(status=200)
            except:
                return HttpResponse(status=500)
        else:
            return JsonResponse(form.errors, safe=False, status=200)

class PositionEdit(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        if id:
            p = Position.objects.filter(id=id).first()
            if p:
                data = {'name': p.name, 'description': p.description}
                return JsonResponse(data, safe=False, status=200)
            else:
                return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)
        else:
            return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)
    def post(self, request, *args, **kwargs):
        data = (json.loads(request.body.decode()))
        id = self.kwargs.get('id')

        if id:
            p = Position.objects.filter(id=id).first()
            p.description = data.get('description')
            p.name = data.get('name')
            p.business = Business.objects.get_business_by_user(self.request.user)
            try:
                p.save()
                return HttpResponse(status=201)
            except:
                return JsonResponse({'errors': 'Database error'}, safe=False, status=500)
        else:
            return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)

class PositionRemove(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()
        data = json.loads(request.body.decode())
        ids = [position.get('id') for position in data]
        try:
            deleted = Position.objects.bulk_delete(ids=ids, business=business)
            return JsonResponse(status=200, data={'deleted': deleted})
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
class WorkerList(View):
    def get(self, request, *args, **kwargs):
        w = Worker.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        data = []
        if w:
            for item in w:
                data.append({'id': item.id, 'name': item.name, 'last_name': item.last_name,
                             'position': {'name': item.position.name, 'id': item.position.id}})
        return JsonResponse(data, safe=False, status=200)

class WorkerAdd(View):
    form_class = WorkerForm
    def post(self, request, *args, **kwargs):
        data = (json.loads(request.body.decode()))
        print(data)
        form = self.form_class(data)
        if form.is_valid():
            w = Worker()
            w.name = data.get('name')
            w.last_name = data.get('last_name')
            w.position = Position.objects.filter(id=data.get('position').get('id')).first()
            w.business = Business.objects.get_business_by_user(self.request.user)
            try:
                w.save()
                data_ = {'id': w.id, 'name': w.name, 'last_name': w.last_name, 'position': {'description': w.position.name, 'id':w.position.id }}
                return JsonResponse(data=data_, status=200)
            except:
                return HttpResponse(status=500)
        else:
            return JsonResponse(form.errors, safe=False, status=200)
class WorkerRemove(View):
     def post(self, request, *args, **kwargs):
        # if not check_permission(request=request, permission='remove_customer'):
        #    return HttpResponse(status=401)
        user = request.user
        business = Business.objects.filter(owner=user).first()
        data = json.loads(request.body.decode())
        ids = [workers.get('id') for workers in data]

        try:
            deleted = Worker.objects.bulk_delete(ids=ids, business=business)
            print(deleted)
            return JsonResponse(status=200, data={'deleted': deleted})
        except Exception as e:
            return HttpResponse(status=400)
class WorkerEdit(View):
    form_class = WorkerForm
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        data = (json.loads(request.body.decode()))
        if id:
            w=Worker.objects.filter(id=id).first()
            w.name = data.get('name')
            w.last_name = data.get('last_name')
            w.position = Position.objects.filter(id=data.get('position').get('id')).first()
            w.business = Business.objects.get_business_by_user(self.request.user)
            try:
                w.save()
                data_ = {'id': w.id, 'name': w.name, 'last_name': w.last_name, 'position': {'description': w.position.name, 'id':w.position.id}}
                return JsonResponse(data_, safe=False, status=200)
            except:
                return JsonResponse({'errors': 'Database error'}, safe=False, status=500)


        else:
            return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)

class MeasuresList(View):
    def get(self, request, *args, **kwargs):
        ing = Measure.objects.filter()
        data = []
        if ing:
            for item in ing:
                data.append({'id': item.id, 'name': item.name, 'description': item.description, 'siglas': item.siglas})
        return JsonResponse(data, safe=False, status=200)

class IngredientsList(View):
    def get(self, request, *args, **kwargs):
        ing = Ingredients.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        data = []
        if ing:
            for item in ing:
                data.append({'id': item.id, 'name': item.name, 'description': item.description,
                             'measure': {'siglas': item.measure.siglas, 'id': item.measure.id}})
        return JsonResponse(data, safe=False, status=200)

class IngredientsAdd(View):
    form_class = IngredientsForm
    def post(self, request, *args, **kwargs):
        data = (json.loads(request.body.decode()))
        form = self.form_class(data)
        if form.is_valid():
            ing = Ingredients()
            ing.name = data.get('name')
            ing.description = data.get('description')
            ing.measure = Measure.objects.filter(id=data.get('measure').get('id')).first()
            ing.business = Business.objects.get_business_by_user(self.request.user)
            try:
                ing.save()
                data_ = {'id': ing.id, 'name': ing.name, 'description': ing.description,
                             'measure': {'siglas': ing.measure.siglas, 'id': ing.measure.id}}
                return JsonResponse(data_, safe=False, status=200)
            except Exception as e:
                print(e)
                return HttpResponse(status=400)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)

class IngredientsRemove(View):
     def post(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()
        data = json.loads(request.body.decode())
        ids = [ingredients.get('id') for ingredients in data]
        try:
            deleted = Ingredients.objects.bulk_delete(ids=ids, business=business)
            return JsonResponse(status=200, data={'deleted': deleted})
        except Exception as e:
            return HttpResponse(status=400)

class IngredientsEdit(View):
    form_class = IngredientsForm
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        data = (json.loads(request.body.decode()))
        if id:
            ingredients = Ingredients.objects.filter(id=id).first()
            ingredients.name = data.get('name')
            ingredients.description = data.get('description')
            ingredients.measure = Measure.objects.filter(id=data.get('measure').get('id')).first()
            ingredients.business = Business.objects.get_business_by_user(user=self.request.user)
            try:
                ingredients.save()
                data_ = {'id': ingredients.id, 'name': ingredients.name, 'description': ingredients.description,
                             'measure': {'siglas': ingredients.measure.siglas, 'id': ingredients.measure.id}}
                return JsonResponse(data_, safe=False, status=200)
            except:
                return JsonResponse({'errors': 'Database error'}, safe=False, status=500)
        else:
            return JsonResponse({'errors': 'Page not Found'}, safe=False, status=404)

class RecipesList(View):
    def get(self, request, *args, **kwargs):
        ing = Recipe.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        data = []
        if ing:
            for item in ing:
                data.append({'id': item.id, 'name': item.name, 'description': item.description})
        return JsonResponse(data, safe=False, status=200)

class WServicesList(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        if not id:
            workers = Worker.objects.filter(business=Business.objects.get_business_by_user(self.request.user))
        else:
            workers = ServiceWorkers.objects.filter(service=Service.objects.filter(id=id).first())
        data = []
        if workers:
            print(workers)
            for item in workers:
                data.append({'id':item.id,'name': item.name, 'last_name': item.last_name,
                             'position': {'description': item.position.description, 'id':item.position.id}})
        return JsonResponse(data, safe=False, status=200)

