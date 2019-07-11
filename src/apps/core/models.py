"""Base model classes module"""

from django.db import models
from django.utils import timezone
from uuid import uuid4


class BaseModel(models.Model):
    """Base model"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        """Meta"""
        abstract = True


class BaseAuditableModel(BaseModel):
    """Base auditable model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True)
    updated_by = models.CharField(max_length=200, blank=True)

    class Meta:
        """Meta"""
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft deleting"""

        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """Hard deleting"""
        return super(BaseAuditableModel, self) \
            .delete(using=using, keep_parents=keep_parents)
