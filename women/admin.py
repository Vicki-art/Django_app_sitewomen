from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class HusbandFilter(admin.SimpleListFilter):
    title = 'Marital status'
    parameter_name = 'marital_status'

    def lookups(self, request, model_admin):
        return [('married', 'Married'), ('single', 'Single')]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


class WomenAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'content', 'post_photo', 'photo', 'cat', 'is_published', 'tag')
    readonly_fields = ('slug', 'post_photo')
    list_display = ('title', 'cat', 'post_photo', 'husband', 'slug', 'is_published')
    list_display_links = ('title', 'cat', 'husband')
    list_editable = ('slug',)
    ordering = ('-time_create',)
    list_per_page = 5
    actions = ('make_published', 'stop_publishing')
    search_fields = ('title__startswith', 'cat__name__endswith')
    list_filter = (HusbandFilter, 'cat__name')
    filter_horizontal = ('tag',)
    save_on_top = True

    @admin.display(description='Photo')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные статьи')
    def make_published(self, request, queryset):
        to_publish = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {to_publish} статей')

    @admin.action(description='Снять с публикации выбранные статьи')
    def stop_publishing(self, request, queryset):
        not_publish = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {not_publish} статей', messages.WARNING)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Women, WomenAdmin)

admin.site.register(Category, CategoryAdmin)
