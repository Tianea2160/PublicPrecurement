from django.db import models

class Corporation(models.Model):
    howToDecideTheWinner = models.CharField(max_length=20)
    bidRate = models.FloatField()
    industryRestriction = models.CharField(max_length=100)
    # result
    bidOrNot = models.CharField(max_length=2)
    create_data = models.DateTimeField(auto_now_add=True)
