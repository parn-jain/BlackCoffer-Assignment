from django.db import models

# Create your models here.
class Data(models.Model):
    title = models.TextField(null=True, blank=True)
    topic = models.CharField(max_length=100,null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    intensity = models.IntegerField(null=True, blank=True)
    sector = models.CharField(max_length=50,blank=True,null=True)
    insight = models.TextField(null=True,blank=True)
    url = models.URLField(blank=True,null=True)
    region = models.CharField(max_length=50,null=True,blank=True)
    impact = models.IntegerField(null=True, blank=True)
    added = models.DateTimeField(null=True,blank=True)
    published = models.DateTimeField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    relevance = models.IntegerField(null=True, blank=True)
    likelihood = models.IntegerField(null=True, blank=True)
    pestle = models.CharField(max_length=50,null=True,blank=True)
    source = models.CharField(max_length=50,null=True,blank=True)

    