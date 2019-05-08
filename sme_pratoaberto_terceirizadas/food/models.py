import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sme_pratoaberto_terceirizadas.abstract_shareable import Describable, TimestampAble
from sme_pratoaberto_terceirizadas.school.models import SchoolAge, SchoolGroup, SchoolUnitType, ManagementType
from sme_pratoaberto_terceirizadas.users.models import User


class MenuStatus(models.Model):
    """Status do Cardápio"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Title"), max_length=99)


class MenuType(Describable):
    """Tipo de Menu (Comum, Lactante, Diabético, etc)"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Food(models.Model):
    """Comida"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Title"), max_length=99)
    details = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(default=True)


class MealType(Describable):
    """Tipo de Refeição"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Meal Type")
        verbose_name_plural = _("Meal Types")


class Meal(models.Model):
    """Refeição"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    meal_title = models.ForeignKey(MealType, on_delete=models.DO_NOTHING)
    management = models.ForeignKey(ManagementType, on_delete=models.DO_NOTHING)
    unit_type = models.ForeignKey(SchoolUnitType, on_delete=models.DO_NOTHING)
    grouping = models.ForeignKey(SchoolGroup, on_delete=models.DO_NOTHING)
    age = models.ForeignKey(SchoolAge, on_delete=models.DO_NOTHING)
    meal = models.ManyToManyField(Food)
    date = models.DateField()

    def __str__(self):
        return self.meal_title

    class Meta:
        verbose_name = _("Meal Title")
        verbose_name_plural = _("Meal Titles")


class DayMenu(TimestampAble):
    """Cardápio para um dia"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.ForeignKey(MenuStatus, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    management = models.ForeignKey(ManagementType, on_delete=models.DO_NOTHING)
    unit_type = models.ForeignKey(SchoolUnitType, on_delete=models.DO_NOTHING)
    grouping = models.ForeignKey(SchoolGroup, on_delete=models.DO_NOTHING)
    date = models.DateField()
    meals = models.ManyToManyField(Meal)
