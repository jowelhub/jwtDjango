import jwt
import datetime
import os

payload = {
    'email': 'manualtest@example.com',
    'name': 'Manual Test User',
    'picture': 'https://example.com/image.jpg',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)  # Expire in 5 minutes
}
jwt_token = jwt.encode(payload, os.environ.get('JWT_DECODE_KEY'), algorithm='HS256')
print(jwt_token)