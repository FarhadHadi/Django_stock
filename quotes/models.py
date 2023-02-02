from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10) #CharField is type of data

    def __str__(self):
        return self.ticker

    
