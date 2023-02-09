from django.contrib import admin

from my_game_list.games.models import GameFollow


@admin.register(GameFollow)
class GameFollowAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("creation_time",)
    list_display = readonly_fields + list_filter + raw_id_fields
