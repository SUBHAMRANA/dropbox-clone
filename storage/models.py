import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Using UUIDs for primary keys is a system design best practice 
    # to prevent ID enumeration and make database sharding easier later.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.username

class FileObject(models.Model):
    class ObjectTypes(models.TextChoices):
        FILE = 'FILE', 'File'
        FOLDER = 'FOLDER', 'Folder'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    object_type = models.CharField(max_length=10, choices=ObjectTypes.choices)
    
    # Adjacency List: A folder can contain other folders or files.
    # 'self' allows recursive relationships. null=True means it's at the root level.
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_objects')
    
    # We store the physical file locally for Phase 1. 
    # In Phase 2, this will change to an S3 URL.
    local_file_path = models.FileField(upload_to='uploads/', null=True, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # A user cannot have two files/folders with the exact same name in the same directory
        unique_together = ('name', 'parent', 'owner')
        indexes = [
            models.Index(fields=['owner', 'parent']), # Speeds up listing a directory
        ]

    def __str__(self):
        return f"{self.object_type}: {self.name}"

class AccessControlList(models.Model):
    """
    Manages sharing and permissions. Separating this from the FileObject 
    allows us to easily query "Files shared with me" without heavy table scans.
    """
    class Permissions(models.TextChoices):
        VIEW = 'VIEW', 'View'
        EDIT = 'EDIT', 'Edit'

    object = models.ForeignKey(FileObject, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_access')
    permission = models.CharField(max_length=10, choices=Permissions.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('object', 'user')