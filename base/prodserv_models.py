__author__ = 'maykel'

from django.db import models
from base.models import Business
from caterfull.serialize import ModelSerialize

class ServiceManager(models.Manager):
    def bulk_delete(self, ids, business):
        return self.filter(id__in=ids).filter(business=business).delete()

class Service(models.Model, ModelSerialize):
    objects = ServiceManager()
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=350)
    tarifa_horaria = models.DecimalField(decimal_places=2, max_digits=9)
    business = models.ForeignKey(Business)
    def get_service_price(self, cant):
        return (self.tarifa_horaria) *cant

class PositionManager(models.Manager):
    def bulk_delete(self, ids, business):
        return self.filter(id__in=ids).filter(business=business).delete()

class Position(models.Model):
    objects = PositionManager()
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=350)
    business = models.ForeignKey(Business)
    class Meta:
        unique_together = (('description', 'business'),)
    def __str__(self):
        return self.description

class WorkerManager(models.Manager):
    def bulk_delete(self, ids, business):
        return self.filter(id__in=ids).filter(business=business).delete()

class Worker(models.Model):
    objects = WorkerManager()
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    business = models.ForeignKey(Business)
    position = models.ForeignKey(Position)
    def __str__(self):
        return self.name

class ServiceWorkers(models.Model):
    service = models.ForeignKey(Service)
    worker = models.ForeignKey(Worker)

class Magnitude(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.name

class MeasureManager(models.Manager):
    def get_measures_of_magnitude(self, magnitude):
        return self.filter(magnitude=magnitude)

class Measure(models.Model):
    objects = MeasureManager()
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=300, null=True, blank=True)
    siglas = models.CharField(max_length=250, null=False, blank=False, default="")
    magnitude = models.ForeignKey(Magnitude, default=0)
    def __str__(self):
        return self.name

class ConversionManger(models.Manager):
    def convert_cant_measure_to_goal(self, measure, measure_goal, cant):
        res = self.filter(measure=measure).filter(measure_goal=measure_goal).first()
        if res:
            return res.factor * cant
        else:
            return {'message': 'No existe la conversion'}

class Conversion(models.Model):
    objects = ConversionManger()
    measure = models.ForeignKey(Measure)
    measure_goal = models.ForeignKey(Measure, related_name='goal')
    factor = models.DecimalField(decimal_places=2, max_digits=9)

class IngredientsManager(models.Manager):
    def bulk_delete(self, ids, business):
        return self.filter(id__in=ids).filter(business=business).delete()

class Ingredients(models.Model):
    objects = IngredientsManager()
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    measure = models.ForeignKey(Measure)
    business = models.ForeignKey(Business, default=0)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=350)
    business = models.ForeignKey(Business, default=0)
    class Meta:
        unique_together = (('name', 'business'),)
    def __str__(self):
        return self.name

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredients)
    cant = models.DecimalField(decimal_places=2, max_digits=9)
    measure = models.ForeignKey(Measure)

class Category(models.Model):
    description = models.CharField(max_length=100)
    business = models.ForeignKey(Business)
    def __str__(self):
        return self.description

class Product(models.Model, ModelSerialize):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=350)
    recipe = models.OneToOneField(Recipe)
    business = models.ForeignKey(Business, default=0)
    category = models.ForeignKey(Category)
    def get_product_price(self, cant):
        if self.productprice_set.filter(min__lt=cant).filter(max__gt=cant).count() == 0:
            result = self.productprice_set.filter(max=0).first()
        else:
            result = self.productprice_set.filter(min__lt=cant).filter(max__gt=cant).first()
        return result.price * (cant)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'recipe', 'business'),)

class ProductPrice(models.Model):
    min = models.IntegerField(null=False)
    max = models.IntegerField(null=False)#(If max is 0 mean infinity)
    price = models.DecimalField(null=False, default=0.00, max_digits=9, decimal_places=2)
    product = models.ForeignKey(Product)
    def get_total(self):
        return round(self.max*self.price, 2)






