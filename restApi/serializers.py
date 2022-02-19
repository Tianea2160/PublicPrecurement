from rest_framework import serializers
from .models import Corporation
from .functions import make_code_list, make_industry_name, modify_data, vec_x_data
import pandas as pd
import json
import sys
import joblib
import pickle
from sklearn.model_selection import train_test_split

class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'

















