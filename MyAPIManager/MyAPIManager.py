from flask import Blueprint, request, jsonify, abort
from datetime import datetime, timedelta
import uuid
import threading
import secrets
import json
import os
from cryptography.fernet import Fernet

class APIManager:
    def __init__(self, api_keys_file="api_keys.json", session_timeout=timedelta(minutes=10)):
        self.api_keys_file = api_keys_file
        self.session_timeout = session_timeout
        self.sessions = {}
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.api_keys = self.load_api_keys()
        self.cleanup_thread = None
        self.start_session_cleanup()

        # Flask Blueprintの作成
        self.bp = Blueprint('api_manager', __name__)

        # ルートの登録
        self.register_routes()

    def load_key(self):
        key = os.getenv("ENCRYPTION_KEY")
        if key is None:
            raise ValueError("環境変数に暗号化キーが設定されていません。")
        return key.encode()

    def save_api_keys(self):
        data = json.dumps(self.api_keys).encode()
        encrypted_data = self.cipher.encrypt(data)
        with open(self.api_keys_file, 'wb') as f:
            f.write(encrypted_data)

    def load_api_keys(self):
        if os.path.exists(self.api_keys_file):
            with open(self.api_keys_file, 'rb') as f:
                encrypted_data = f.read()
                try:
                    data = self.cipher.decrypt(encrypted_data)
                    return json.loads(data)
                except Exception as e:
                    print(f"APIキーの読み込み中にエラーが発生しました: {e}")
                    return {}
        return {}

    def check_api_key(self):
        """ヘッダーからAPIキーを検証"""
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key not in self.api_keys:
            abort(403, "無効なAPIキーです。")

    def create_api_key_logic(self, user_id, memo):
        new_api_key = secrets.token_hex(32)
        self.api_keys[new_api_key] = {
            'user_id': user_id,
            'memo': memo,
            'created_at': datetime.now().isoformat()
        }
        self.save_api_keys()
        return new_api_key

    def delete_api_key_logic(self, api_key):
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            self.save_api_keys()
            return True
        return False

    def session_start_logic(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'last_access': datetime.now()
        }
        return session_id

    def check_session_id(self, session_id):
        return session_id in self.sessions

    def update_last_access(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id]['last_access'] = datetime.now()

    def cleanup_sessions(self):
        """古いセッションを削除"""
        now = datetime.now()
        for session_id in list(self.sessions.keys()):
            if now - self.sessions[session_id]['last_access'] > self.session_timeout:
                del self.sessions[session_id]
        # 1分後に再度実行
        threading.Timer(60, self.cleanup_sessions).start()

    def start_session_cleanup(self):
        """セッションクリーナーをデーモンスレッドで開始"""
        self.cleanup_sessions()

    def register_routes(self):
        @self.bp.route('/create_api_key', methods=['POST'])
        def create_api_key():
            data = request.get_json()
            user_id = data.get('user_id')
            memo = data.get('memo')

            if not user_id or not memo:
                return jsonify({"error": "Missing 'user_id' or 'memo'."}), 400

            new_api_key = self.create_api_key_logic(user_id, memo)
            return jsonify({"api_key": new_api_key})

        @self.bp.route('/delete_api_key', methods=['DELETE'])
        def delete_api_key():
            data = request.get_json()
            api_key = data.get('api_key')

            if not api_key:
                return jsonify({"error": "Missing 'api_key'."}), 400

            success = self.delete_api_key_logic(api_key)
            if success:
                return jsonify({"message": "API key deleted successfully."})
            else:
                return jsonify({"error": "Invalid API key."}), 400

        @self.bp.route('/session_start', methods=['GET'])
        def session_start():
            """新しいセッションIDを発行"""
            self.check_api_key()

            session_id = self.session_start_logic()
            return jsonify({"session_id": session_id})

    def get_blueprint(self):
        return self.bp
