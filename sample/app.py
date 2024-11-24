from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, abort
from MyAPIManager import APIManager

app = Flask(__name__)

# セッションごとのデータ（アプリケーション固有）
dic_values = {}

# APIManagerのインスタンスを作成
api_manager = APIManager()
app.register_blueprint(api_manager.get_blueprint())

#------------------------------------------------------------#
# アプリケーション固有のAPI
#------------------------------------------------------------#

@app.route('/set_data', methods=['POST'])
def set_data():
    """セッションIDとvalueを受け取り、値を保存"""
    api_manager.check_api_key()

    session_id = request.json.get('session_id')
    value = request.json.get('value')

    # セッションIDが存在するか確認
    if not api_manager.check_session_id(session_id):
        abort(403, "無効なセッションIDです。")

    try:
        dic_values[session_id] = dic_values.get(session_id, {})
        dic_values[session_id]['value'] = int(value)
        api_manager.update_last_access(session_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. 'value' must be an integer."}), 400

    return jsonify({"message": "Value set successfully."})

@app.route('/calculate', methods=['GET'])
def calculate():
    """保持したvalueに3を足した結果を返す"""
    api_manager.check_api_key()

    session_id = request.args.get('session_id')

    # セッションIDが存在するか確認
    if not api_manager.check_session_id(session_id):
        abort(403, "無効なセッションIDです。")

    if session_id not in dic_values or 'value' not in dic_values[session_id]:
        abort(403, "セッションに値が設定されていません。")

    api_manager.update_last_access(session_id)
    result = dic_values[session_id]['value'] + 3
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=8080)




























# from flask import Flask, request, jsonify, abort
# from datetime import datetime, timedelta
# import uuid
# import threading
# import secrets
# import json
# import os
# from cryptography.fernet import Fernet

# app = Flask(__name__)

# # セッションごとのデータ（アプリケーション固有）
# dic_values = {}

# class APIManager:
#     def __init__(self, api_keys_file="api_keys.json", session_timeout=timedelta(minutes=10)):
#         self.api_keys_file = api_keys_file
#         self.session_timeout = session_timeout
#         self.sessions = {}
#         self.key = self.load_key()
#         self.cipher = Fernet(self.key)
#         self.api_keys = self.load_api_keys()
#         self.start_session_cleanup()

#     def load_key(self):
#         key = os.getenv("ENCRYPTION_KEY")
#         if key is None:
#             raise ValueError("環境変数に暗号化キーが設定されていません。")
#         return key.encode()

#     def save_api_keys(self):
#         data = json.dumps(self.api_keys).encode()
#         encrypted_data = self.cipher.encrypt(data)
#         with open(self.api_keys_file, 'wb') as f:
#             f.write(encrypted_data)

#     def load_api_keys(self):
#         if os.path.exists(self.api_keys_file):
#             with open(self.api_keys_file, 'rb') as f:
#                 encrypted_data = f.read()
#                 try:
#                     data = self.cipher.decrypt(encrypted_data)
#                     return json.loads(data)
#                 except Exception as e:
#                     print(f"APIキーの読み込み中にエラーが発生しました: {e}")
#                     return {}
#         return {}

#     def check_api_key(self):
#         """ヘッダーからAPIキーを検証"""
#         api_key = request.headers.get("x-api-key")
#         if not api_key or api_key not in self.api_keys:
#             abort(403, "無効なAPIキーです。")

#     def create_api_key(self, user_id, memo):
#         new_api_key = secrets.token_hex(32)
#         self.api_keys[new_api_key] = {
#             'user_id': user_id,
#             'memo': memo,
#             'created_at': datetime.now().isoformat()
#         }
#         self.save_api_keys()
#         return new_api_key

#     def delete_api_key(self, api_key):
#         if api_key in self.api_keys:
#             del self.api_keys[api_key]
#             self.save_api_keys()
#             return True
#         return False

#     def session_start(self):
#         session_id = str(uuid.uuid4())
#         self.sessions[session_id] = {
#             'last_access': datetime.now()
#         }
#         return session_id

#     def check_session_id(self, session_id):
#         return session_id in self.sessions

#     def update_last_access(self, session_id):
#         if session_id in self.sessions:
#             self.sessions[session_id]['last_access'] = datetime.now()

#     def cleanup_sessions(self):
#         """古いセッションを削除"""
#         now = datetime.now()
#         for session_id in list(self.sessions.keys()):
#             if now - self.sessions[session_id]['last_access'] > self.session_timeout:
#                 del self.sessions[session_id]
#                 # セッションに関連するアプリケーションデータも削除
#                 if session_id in dic_values:
#                     del dic_values[session_id]
#         # 1分後に再度実行
#         threading.Timer(60, self.cleanup_sessions).start()

#     def start_session_cleanup(self):
#         """セッションクリーナーをデーモンスレッドで開始"""
#         threading.Thread(target=self.cleanup_sessions, daemon=True).start()

# # APIManagerのインスタンスを作成
# api_manager = APIManager()

# #------------------------------------------------------------#
# # API
# #------------------------------------------------------------#

# @app.route('/create_api_key', methods=['POST'])
# def create_api_key():
#     user_id = request.json.get('user_id')
#     memo = request.json.get('memo')
    
#     if not user_id or not memo:
#         return jsonify({"error": "Missing 'user_id' or 'memo'."}), 400
    
#     new_api_key = api_manager.create_api_key(user_id, memo)
    
#     return jsonify({"api_key": new_api_key})

# @app.route('/delete_api_key', methods=['DELETE'])
# def delete_api_key():
#     api_key = request.json.get('api_key')
    
#     if not api_key:
#         return jsonify({"error": "Missing 'api_key'."}), 400
    
#     success = api_manager.delete_api_key(api_key)
#     if success:
#         return jsonify({"message": "API key deleted successfully."})
#     else:
#         return jsonify({"error": "Invalid API key."}), 400

# @app.route('/session_start', methods=['GET'])
# def session_start():
#     """新しいセッションIDを発行"""
#     api_manager.check_api_key()
    
#     session_id = api_manager.session_start()
#     return jsonify({"session_id": session_id})

# # セッションごとのデータ（アプリケーション固有）
# @app.route('/set_data', methods=['POST'])
# def set_data():
#     """セッションIDとvalueを受け取り、値を保存"""
#     api_manager.check_api_key()
    
#     session_id = request.json.get('session_id')
#     value = request.json.get('value')
    
#     # セッションIDが存在するか確認
#     if not api_manager.check_session_id(session_id):
#         abort(403, "無効なセッションIDです。")
    
#     try:
#         dic_values[session_id] = dic_values.get(session_id, {})
#         dic_values[session_id]['value'] = int(value)
#         api_manager.update_last_access(session_id)
#     except (ValueError, TypeError):
#         return jsonify({"error": "Invalid input. 'value' must be an integer."}), 400
    
#     return jsonify({"message": "Value set successfully."})

# @app.route('/calculate', methods=['GET'])
# def calculate():
#     """保持したvalueに3を足した結果を返す"""
#     api_manager.check_api_key()
    
#     session_id = request.args.get('session_id')
    
#     # セッションIDが存在するか確認
#     if not api_manager.check_session_id(session_id):
#         abort(403, "無効なセッションIDです。")
    
#     if session_id not in dic_values or 'value' not in dic_values[session_id]:
#         abort(403, "セッションに値が設定されていません。")
    
#     api_manager.update_last_access(session_id)
#     result = dic_values[session_id]['value'] + 3
#     return jsonify({"result": result})

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)
