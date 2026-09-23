from rest_framework import serializers
from .models import FileObject

class FileObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileObject
        fields = ['id', 'name', 'object_type', 'parent', 'owner', 'local_file_path', 'size_bytes', 'created_at']
        read_only_fields = ['id', 'owner', 'size_bytes', 'created_at']

    def create(self, validated_data):
        # We automatically set the owner to whoever made the API request
        validated_data['owner'] = self.context['request'].user
        
        # If a file was uploaded, calculate its size
        uploaded_file = validated_data.get('local_file_path')
        if uploaded_file:
            validated_data['size_bytes'] = uploaded_file.size
            
        return super().create(validated_data)