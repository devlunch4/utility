
## 라이브러리 설치 및 오프라인 환경 설정

### 1. 필요한 라이브러리 설치

이 프로젝트는 다음의 라이브러리를 사용합니다:

- `PyPDF2`: PDF 파일 읽기 및 쓰기 작업
- `Pillow`: 이미지 처리 (PDF 분할용)
- `tkinter`: GUI 생성 (Python 표준 라이브러리, 별도 설치 불필요)

**라이브러리 설치 방법 (인터넷 환경)**

1. `requirements.txt` 파일을 사용하여 필요한 라이브러리를 한 번에 설치합니다:

    ```bash
    pip install -r requirements.txt
    ```

    `requirements.txt` 파일 내용:
    ```txt
    PyPDF2==3.0.1
    Pillow==10.0.0
    ```

### 2. 오프라인 환경 설정

인터넷이 없는 환경에서 라이브러리를 설치하려면, 아래와 같이 오프라인 패키지를 다운로드하여 설치할 수 있습니다.

#### (1) 온라인 환경에서 패키지 다운로드

인터넷에 연결된 환경에서, 필요한 패키지를 다운로드합니다:

```bash
pip download -r requirements.txt -d ./offline_packages
```

이 명령어는 `requirements.txt`에 명시된 모든 라이브러리를 `offline_packages` 폴더에 다운로드합니다.

#### (2) 오프라인 환경에서 패키지 설치

다운로드된 패키지를 오프라인 환경으로 옮긴 후, 아래 명령어로 설치합니다:

```bash
pip install --no-index --find-links=./offline_packages -r requirements.txt
```

---

이렇게 하면, 인터넷 연결 없이도 필요한 라이브러리들을 설치하여 프로젝트를 실행할 수 있습니다.