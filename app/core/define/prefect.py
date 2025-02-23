class Blocks:
    class S3Bucket:
        MINIO_STORAGE_CODE_NAME = "minio-storage-code"

    class CodeStorage:
        URL_NAME: str = "code-storage-url"
        ACCESS_KEY_NAME: str = "code-storage-access-key"
        SECRET_KEY_NAME: str = "code-storage-secret-key"

    class Github:
        URL_NAME: str = "github-url"
        ACCESS_TOKEN_NAME: str = "github-access-token"


class Variables:
    PASSED_X_DAYS: str = "passed_x_days"
