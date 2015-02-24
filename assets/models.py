from django.db import models
from map.models import Place

# Create your models here.
class Asset(models.Model):
    property = models.ForeignKey(Place)
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')
    creation = models.DateField('date of registration', auto_now_add=True)
    #status = models.ForeignKey(Status)

    class Meta:
        verbose_name = 'asset'
        verbose_name_plural = 'assets'

    def __unicode__(self):
        return self.name