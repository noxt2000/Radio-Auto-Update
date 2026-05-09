import requests
import json
import os

# 1. 고정 설정값
GIST_ID = "3613497490a95c68cf2a7f3e45a3bdc3"
# 깃허브 액션 환경변수(Secret)에서 토큰을 가져오고, 없으면 직접 입력용으로 비워둠
GH_TOKEN = os.environ.get("GH_TOKEN") or "여기에_직접_토큰을_넣어_테스트하세요"

def get_sbs_url(channel_id):
    """SBS (PowerFM: powerfm, LoveFM: lovefm) 주소 추출"""
    try:
        api_url = f"https://apis.sbs.co.kr/play-api/get-streaming-url?channel={channel_id}&protocol=hls&device=pc"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://play.sbs.co.kr/'
        }
        res = requests.get(api_url, headers=headers, timeout=10)
        return res.json().get('url', "")
    except Exception as e:
        print(f"SBS {channel_id} 에러: {e}")
        return ""

def get_mbc_url(type_id):
    """MBC (FM4U: mbc, 표준FM: sfm) 주소 추출"""
    try:
        # mbc: FM4U, sfm: 표준FM
        api_url = f"https://control.imbc.com/v2/item/getItem?item=audio&channel={type_id}&agent=pc&protocol=hls"
        res = requests.get(api_url, timeout=10)
        return res.json().get('MediaUrl', "")
    except Exception as e:
        print(f"MBC {type_id} 에러: {e}")
        return ""

def get_kbs_url(channel_id):
    """KBS (CoolFM: 24, 1라디오: 21, 2라디오: 22) 주소 추출"""
    try:
        api_url = f"https://api.kbs.co.kr/p27/2plus/menu/get_streaming_url?channel_id={channel_id}&protocol=hls"
        res = requests.get(api_url, timeout=10)
        return res.json().get('url', "")
    except Exception as e:
        print(f"KBS {channel_id} 에러: {e}")
        return ""

def main():
    print("🚀 방송사별 최신 라디오 주소 수집 시작...")

    # 안드로이드 앱의 ID와 매칭되는 리스트 생성
    radio_list = [
        {"id": "SBS_POWER", "name": "SBS 파워FM", "url": get_sbs_url("powerfm")},
        {"id": "SBS_LOVE", "name": "SBS 러브FM", "url": get_sbs_url("lovefm")},
        {"id": "MBC_FM4U", "name": "MBC FM4U", "url": get_mbc_url("mbc")},
        {"id": "MBC_STD", "name": "MBC 표준FM", "url": get_mbc_url("sfm")},
        {"id": "KBS_COOL", "name": "KBS CoolFM", "url": get_kbs_url("24")},
        {"id": "KBS_1R", "name": "KBS 1라디오", "url": get_kbs_url("21")},
        {"id": "KBS_2R", "name": "KBS 2라디오", "url": get_kbs_url("22")}
    ]

    # 유효한 주소만 남기기 (실패한 채널 확인용)
    for channel in radio_list:
        if not channel["url"]:
            print(f"⚠️ 경고: {channel['name']} 주소를 가져오지 못했습니다.")

    # 2. Gist 업데이트 실행
    print("📡 Gist 업데이트 중...")
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    payload = {
        "description": "RadioStreamer 최신 주소 자동 업데이트",
        "files": {
            "RadioStreamer.json": {
                "content": json.dumps(radio_list, ensure_ascii=False, indent=2)
            }
        }
    }

    gist_api_url = f"https://api.github.com/gists/{GIST_ID}"
    response = requests.patch(gist_api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ 모든 라디오 주소가 성공적으로 Gist에 업데이트되었습니다!")
    else:
        print(f"❌ Gist 업데이트 실패: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
