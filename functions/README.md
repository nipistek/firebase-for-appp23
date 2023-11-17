# 설명

- main.py

firebase functions에 보낼 메소드 쓰는 곳

- sending_data_to_database.py

osupumplist2 폴더에 있는 txt 파일을 읽어서 firebase firestore에 보내는 데이터베이스 시딩에 쓰일 작은 스크립트.

파이어베이스_어드민_뭐시기.json 파일이 이 파일과 같은 위치에 필요하다.

__주의: 실행은 최상위 폴더에서 할 것__

txt 파일의 형식은 다음과 같다.
1. 무시하려면 `#` 으로 처리한다. 단, 스크립트가 2줄씩 읽으니 2줄씩 처리해야 한다는 점에 유의.
2. 홀수 번째 줄에는 나무위키에서 긁어온 '차례' 부분과 storeSupport에 쓰이는 5개 문자가, 짝수 번째 줄에는 그 오락실의 주소가 들어간다.