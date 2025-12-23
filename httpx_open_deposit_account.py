import time
import httpx


create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
user_id = create_user_response.json()['user']['id']

create_deposit_account_payload = {
  "userId": user_id
}

open_deposit_account_response = httpx.post("http://localhost:8003/api/v1/accounts/open-deposit-account", json=create_deposit_account_payload)

print(open_deposit_account_response.json())
print(open_deposit_account_response.status_code)
