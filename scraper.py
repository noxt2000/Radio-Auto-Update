import requests
import json
import os

def update_gist(radio_data):
    # 사용자님의 Gist ID입니다.
    gist_id = "3613497490a95c68cf2a7f3e45a3bdc3"
    # 금고(Secrets)에 저장한 토큰을 가져옵니다.
    token = os.getenv("GIST_TOKEN") 
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Gist에 올릴 파일 데이터 구성
    payload = {
        "files": {
            "RadioStreamer.json": {
                "content": json.dumps(radio_data, indent=2, ensure_ascii=False)
            }
        }
    }
    
    # GitHub API를 통해 Gist 수정 요청
    url = f"https://api.github.com/gists/{gist_id}"
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("✅ Gist 업데이트 성공!")
    else:
        print(f"❌ 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # 현재 정상 작동하는 라디오 목록 데이터입니다.
    # 나중에는 이 부분을 자동으로 캐오는 코드로 업그레이드할 수 있습니다.
    channels = [
        {"id": "MBC_FM4U", "title": "MBC FM4U", "url": "https://mfmlive.imbc.com/audio/mfm/_definst_/mfm.stream/playlist.m3u8"},
        {"id": "MBC_STD", "title": "MBC 표준FM", "url": "https://sfmlive.imbc.com/audio/sfm/_definst_/sfm.stream/playlist.m3u8"},
        {"id": "KBS_COOL", "title": "KBS Cool FM", "url": "https://coolfm.kbs.co.kr/live/coolfm.stream/playlist.m3u8"},
        {"id": "KBS_1R", "title": "KBS 1라디오", "url": "https://kbs-hls.kbs.co.kr/radio/1r/playlist.m3u8"},
        {"id": "KBS_2R", "title": "KBS 2라디오", "url": "https://kbs-hls.kbs.co.kr/radio/2r/playlist.m3u8"},
        {"id": "SBS_POWER", "title": "SBS 파워FM", "url": "https://c15ncmsvc.sbs.co.kr/sbs_powerfm/_definst_/sbs_powerfm.stream/playlist.m3u8"},
        {"id": "SBS_LOVE", "title": "SBS 러브FM", "url": "https://c15ncmsvc.sbs.co.kr/sbs_lovefm/_definst_/sbs_lovefm.stream/playlist.m3u8"}
    ]
    
    update_gist(channels)
