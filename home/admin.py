from django.contrib import admin
from .models import Men_category, Men_product_category, Men_Product
from .models import Women_category, Women_product_category, Women_Product
from .models import Kid_category, Kid_product_category, Kid_Product

# Register your models here.
admin.site.register(Men_category)
admin.site.register(Men_product_category)
admin.site.register(Men_Product)
admin.site.register(Women_category)
admin.site.register(Women_product_category)
admin.site.register(Women_Product)
admin.site.register(Kid_category)
admin.site.register(Kid_product_category)
admin.site.register(Kid_Product)
