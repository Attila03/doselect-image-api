API for managing images

Registration Endpoint: https://imagemanager-api.herokuapp.com/register/

Token Endpoint: https://imagemanager-api.herokuapp.com/api-token-auth/

Refresh Token: https://imagemanager-api.herokuapp.com/refresh-token/

API Endpoints

GET List : https://imagemanager-api.herokuapp.com/api/images/

Returns a list of image urls for the authenticated user.

Format: {"image_name": image_url, .... }

POST : https://imagemanager-api.herokuapp.com/api/images/

Upload a image file with multipart/form-data

GET Detail : https://imagemanager-api.herokuapp.com/api/images/{image_name}

Returns a base64 encoded image: {'image': base64 encoded string}

DELETE: https://imagemanager-api.herokuapp.com/api/images/{image_name}

Deletes the image if present

PATCH: https://imagemanager-api.herokuapp.com/register/{image_name}

Updates the image if present

{image_name} in all cases should be exact with file extensions.



