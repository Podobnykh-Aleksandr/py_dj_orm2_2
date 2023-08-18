from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tags = []
        main_tags = []
        for form in self.forms:
            if len(form.cleaned_data):
                tags.append(form.cleaned_data['tag'])
                main_tags.append(1 if form.cleaned_data['is_main'] else 0)

            if len(tags) != len(set(tags)):
                raise ValidationError('Один из тегов повторяется')

            if sum(main_tags) == 0:
                raise ValidationError('Статье не присвоен основной тег')

            if sum(main_tags) > 1:
                raise ValidationError('В статье основной тег используется '
                                      'более 1 раза')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
