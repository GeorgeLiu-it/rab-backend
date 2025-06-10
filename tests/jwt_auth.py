import os
import jwt
import datetime

def auth_headers():
    jwt_secret = "george"
    os.environ["JWT_SECRET"] = jwt_secret
    payload = {
        "id": "testuser",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=11),
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}

print(auth_headers())