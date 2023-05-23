from django.contrib import admin
from .models import PositiveWords, NegativeWords

admin.site.register(PositiveWords)
admin.site.register(NegativeWords)
