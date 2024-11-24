from cryptography.fernet import Fernet
# 暗号化キーの生成（初回のみ使用して保存しておく）
key = Fernet.generate_key()
print(key)
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)
