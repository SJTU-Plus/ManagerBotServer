# ManagerBotServer

ManagerBotServer 是 [ManagerBot](https://github.com/dujiajun/ManagerBot) 的配套网页。

 ## 如何使用
 
 1. 创建 Python（>=3.7） 虚拟环境
     ```shell script
      virtualenv venv
      source venv/bin/activate
    ```
 2. 安装依赖
    ```shell script
    pip install -r requirements.txt
    ```
 3. 新建并配置`config.json`
    ```json
    {
    "ENV": "development",
    "JACCOUNT_CLIENT_ID": "",
    "JACCOUNT_CLIENT_SECRET": "",
    "JACCOUNT_ACCESS_TOKEN_URL": "https://jaccount.sjtu.edu.cn/oauth2/token",
    "JACCOUNT_AUTHORIZE_URL": "https://jaccount.sjtu.edu.cn/oauth2/authorize",
    "JACCOUNT_API_BASE_URL": "https://api.sjtu.edu.cn/",
    "JACCOUNT_CLIENT_KWARGS": {
        "scope": "openid",
        "token_endpoint_auth_method": "client_secret_basic",
        "token_placement": "header"
    },
    "ATTESTATION_SECRET": ""
    }
    ```
    其中`secret`可以按照`cmac_attestation.py`中的方式生成。
 4. 运行`app.py`
