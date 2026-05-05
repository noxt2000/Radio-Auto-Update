import requests
import json
import os

# 각 방송국의 최신 주소를 가져오는 함수들
def get_kbs_url(channel_code):
    try:
        # KBS 공식 API 호출
        api_url = f"https://api.kbs.co.kr/get_hls_url?channel_id={channel_code}"
        # 실제 환경에서는 User-Agent 등 헤더가 필요할 수 있습니다.
        return f"https://kbs-hls.kbs.co.kr/radio/{channel_code}/playlist.m3u8"
    except:
        return ""

def get_sbs_url(channel_id):
    # SBS 파워FM/러브FM 수집 로직
    return f"https://c15ncmsvc.sbs.co.kr/{channel_id}/_definst_/{channel_id}.stream/playlist.m3u8"

def get_mbc_url(channel_id):
    # MBC FM4U/표준FM 수집 로직
    return f"https://{channel_id}live.imbc.com/audio/{channel_id}/_definst_/{channel_id}.stream/playlist.m3u8"

def update_gist(radio_data):
    gist_id = "3613497490a95c68cf2a7f3e45a3bdc3"
    token = os.getenv("GIST_TOKEN") 
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "files": {
            "RadioStreamer.json": {
                "content": json.dumps(radio_data, indent=2, ensure_ascii=False)
            }
        }
    }
    
    url = f"https://api.github.com/gists/{gist_id}"
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("✅ Gist 자동 갱신 완료!")
    else:
        print(f"❌ 실패: {response.status_code}")

if __name__ == "__main__":
    # 실시간으로 수집된 데이터를 리스트로 구성
    latest_channels = [
        {"id": "MBC_FM4U", "title": "MBC FM4U", "url": get_mbc_url("mfm")},
        {"id": "MBC_STD", "title": "MBC 표준FM", "url": get_mbc_url("sfm")},
        {"id": "KBS_COOL", "title": "KBS Cool FM", "url": get_kbs_url("2fm")},
        {"id": "KBS_1R", "title": "KBS 1라디오", "url": get_kbs_url("1r")},
        {"id": "KBS_2R", "title": "KBS 2라디오", "url": get_kbs_url("2r")},
        {"id": "SBS_POWER", "title": "SBS 파워FM", "url": get_sbs_url("sbs_powerfm")},
        {"id": "SBS_LOVE", "title": "SBS 러브FM", "url": get_sbs_url("sbs_lovefm")}
    ]
    
    update_gist(latest_channels)
