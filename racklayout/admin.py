from django.contrib import admin
from racklayout.models import Metro, Dc, Asset, Rack, Row, HalfUnit
# Register your models here.

admin.site.register(Metro)
admin.site.register(Dc)
admin.site.register(Row)
admin.site.register(Rack)
admin.site.register(Asset)
admin.site.register(HalfUnit)
