import requests

# APIのURL
base_url = "http://localhost:8080"

def create_api_key(user_id, memo):
    payload = {
        "user_id": user_id,
        "memo": memo
    }
    response = requests.post(f"{base_url}/create_api_key", json=payload)
    response.raise_for_status()
    api_key = response.json()["api_key"]
    print("Generated API Key:", api_key)
    return api_key


# 1. /start_using エンドポイントにアクセスしてセッションIDを取得
def start_using(headers):
    response = requests.get(f"{base_url}/session_start", headers=headers)
    response.raise_for_status()
    session_data = response.json()
    session_id = session_data["session_id"]
    print("Session ID:", session_id)
    return session_id

# 2. /set_data エンドポイントでセッションIDとvalueを設定
def set_data(headers, session_id, value):
    payload = {
        "session_id": session_id,
        "value": value
    }
    response = requests.post(f"{base_url}/set_data", headers=headers, json=payload)
    response.raise_for_status()
    print(response.json()["message"])

# 3. /calculate エンドポイントにアクセスして結果を取得
def calculate(headers, session_id):
    params = {
        "session_id": session_id
    }
    response = requests.get(f"{base_url}/calculate", headers=headers, params=params)
    response.raise_for_status()
    result = response.json()["result"]
    print("Calculation Result:", result)
    return result

if __name__ == "__main__":

    user_id = "user123"
    memo = "Test API Key"
    api_key = create_api_key(user_id, memo)
    headers = {
        "x-api-key": api_key
    }

    # セッションを開始してIDを取得
    session_id = start_using(headers)
    
    # データを設定
    value_to_set = 10
    set_data(headers, session_id, value_to_set)
    
    # 計算結果を取得
    calculate(headers, session_id)