# 설명
1. [firebase cli를 설치한다](https://firebaseopensource.com/projects/firebase/firebase-tools/)
2. `python -m venv venv` 를 functions 안에서 수행한다.
3. 윈도우에서는 `venv\Scripts\activate`를, 이외 리눅스나 맥에서는 `source venv/bin/activate`를 한다.
4. `pip install -r requirements.txt`
3. functions 폴더에서 파일을 수정한다.
4. 최상위 폴더에서 firebase deploy --only functions

* functions 폴더에도 readme가 있으니 이것도 참고
__추후 기능 확장 예정__