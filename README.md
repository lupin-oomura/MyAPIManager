"# MyAPIManager" 

## 使い方

1. まずは暗号化キーを発行する
- `暗号化キーの発行.py`を実行して、print(key)で出てくるキー情報をコピー
```
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
```
- そのキーを.envに保存。
    例: ENCRYPTION_KEY=xxxxx`

- sampleフォルダにある`app.py`や`Dockerfile`を参考に、APIを自作してください。だいぶ楽できると思います。
- その自作したAPIがちゃんと動いているかは、
① コンテナを立ち上げる
② test_sendvalues.pyを実行する→エラーが出ず13という数字がかえってくれば成功
