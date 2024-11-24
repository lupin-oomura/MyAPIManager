"# MyAPIManager" 

## 使い方

### まずは暗号化キーを発行する
- `暗号化キーの発行.py`を実行して、print(key)で出てくるキー情報をコピー
```
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
```
バッチで動かすんだったら、`pipenv run python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); print(key.decode())"`。
- そのキーを.envに保存。
    例: ENCRYPTION_KEY=xxxxx`

### APIの作成
- sampleフォルダにある`app.py`を参考に、APIを自作してください。だいぶ楽できると思います。

### テスト
その自作したAPIがちゃんと動いているかは、
* コンテナを立ち上げる・・・sampleにある`Dockerfile`を使えば、8080で立ち上がります。
* test_sendvalues.pyを実行する→エラーが出ず13という数字がかえってくれば成功
