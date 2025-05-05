from django.contrib import admin
from .models import User,Category,Tag,ItemTag,Item,ClaimRequest

class ItemTagInline(admin.TabularInline):
    model = ItemTag

class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemTagInline
    ]


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemTag)
admin.site.register(ClaimRequest)

