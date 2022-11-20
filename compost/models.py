import uuid

from django.db import models
from ruamel.yaml import timestamp


class Household(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    members_count = models.IntegerField(verbose_name="Members living in the household")
    green_land_size = models.IntegerField(verbose_name="Green land size (m2)")


class CompostCategory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)


class Composter(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey("compost.Household", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    capacity = models.IntegerField("Composter capacity in liters")
    fill_amount = models.IntegerField("Composter fill amount in liters", blank=True)
    estimated_density = models.FloatField("Estimated mass density in km/l", default=0.5)
    categories = models.ManyToManyField(
        "compost.CompostCategory",
        related_name="composters",
        related_query_name="composter",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class ComposterAction(models.Model):

    class ActionType(models.TextChoices):
        FILL = "fill", "Fill"
        EMPTY = "empty", "Empty"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    composter = models.ForeignKey("compost.Composter", on_delete=models.CASCADE)
    fill_amount = models.IntegerField("Composter fill amount after action")
    category = models.ForeignKey("compost.CompostCategory", models.CASCADE, null=True)
    action_type = models.CharField(max_length=5, choices=ActionType.choices)

    def save(self, *args, **kwargs):
        action = super().save(*args, **kwargs)
        if action.action_type == ComposterAction.ActionType.FILL:
            self.composter.categories.add(self.category)
        self.composter.fill_amount = action.fill_amount
        self.composter.save()
        return action


class CompostAudit(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    composter = models.ForeignKey("compost.Composter", on_delete=models.CASCADE)
    recorded_density = models.FloatField(blank=True)

    def save(self, *args, **kwargs):
        audit = super().save(*args, **kwargs)
        self.composter.estimated_density = self.recorded_density
        self.composter.save()
        return audit

