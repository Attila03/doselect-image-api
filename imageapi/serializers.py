import os

from django.conf import settings

from rest_framework import serializers


class ImagePostSerializer(serializers.Serializer):

    image = serializers.ImageField(max_length=255, allow_empty_file=False)

    def validate(self, data):
        # checks if filename already exists irrespective of extension, raise error if it does.
        username = self.context['request'].user.username
        user_images_path = os.path.join(settings.MEDIA_ROOT, username)
        filenames = [os.path.splitext(f)[0] for f in os.listdir(user_images_path)
                        if os.path.isfile(os.path.join(user_images_path, f))]
        image = data['image']
        image_name, image_extension = os.path.splitext(image.name)
        if image_name in filenames:
            raise serializers.ValidationError({
                "filename_error": "A file with name '{}' already exists.To update the image "
                                  "send patch request instead".format(image_name)
            })
        return data


class ImagePatchSerializer(serializers.Serializer):

    image = serializers.ImageField(max_length=255, allow_empty_file=False)

