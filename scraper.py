import requests
import json
import os

# 1. 설정값 (본인의 Gist ID 확인)
GIST_ID = "3613497490a95c68cf2a7f3e45a3bdc3"
# GitHub Secrets에서 가져오기
GH_TOKEN = os.environ.get("GIST_TOKEN") 

# 브라우저인 척 위장하는 더 강력한 헤더
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_sbs_url(channel_id):
    """SBS 주소 추출"""
    try:
        api_url = f"https://apis.sbs.co.kr/play-api/get-streaming-url?channel={channel_id}&protocol=hls&device=pc"
        headers = COMMON_HEADERS.copy()
        headers['Referer'] = 'https://play.sbs.co.kr/'
        res = requests.get(api_url, headers=headers, timeout=10)
        return res.json().get('url', "")
    except:
        return ""

def get_mbc_url(type_id):
    """MBC 주소 추출"""
    try:
        api_url = f"https://control.imbc.com/v2/item/getItem?item=audio&channel={type_id}&agent=pc&protocol=hls"
        headers = COMMON_HEADERS.copy()
        headers['Referer'] = 'https://mini.imbc.com/'
        res = requests.get(api_url, headers=headers, timeout=10)
        data = res.json()
        return data.get('MediaUrl') or data.get('AACLiveURL') or ""
    except:
        return ""

def get_kbs_url(channel_id):
    """KBS 주소 추출"""
    try:
        api_url = f"https://api.kbs.co.kr/p27/2plus/menu/get_streaming_url?channel_id={channel_id}&protocol=hls"
        res = requests.get(api_url, headers=COMMON_HEADERS, timeout=10)
        return res.json().get('url', "")
    except:
        return ""

def main():
    print("🚀 방송사별 최신 라디오 주소 수집 시작...")

    radio_list = [
        {"id": "SBS_POWER", "name": "SBS 파워FM", "url": get_sbs_url("powerfm")},
        {"id": "SBS_LOVE", "name": "SBS 러브FM", "url": get_sbs_url("lovefm")},
        {"id": "MBC_FM4U", "name": "MBC FM4U", "url": get_mbc_url("mbc")},
        {"id": "MBC_STD", "name": "MBC 표준FM", "url": get_mbc_url("sfm")},
        {"id": "KBS_COOL", "name": "KBS CoolFM", "url": get_kbs_url("24")},
        {"id": "KBS_1R", "name": "KBS 1라디오", "url": get_kbs_url("21")},
        {"id": "KBS_2R", "name": "KBS 2라디오", "url": get_kbs_url("22")}
    ]

    for ch in radio_list:
        status = "✅ 성공" if ch["url"] else "❌ 실패"
        print(f"{ch['name']}: {status}")

    # 토큰 유효성 검사
    if not GH_TOKEN or len(GH_TOKEN) < 10:
        print("❌ 에러: GIST_TOKEN이 비어있거나 잘못되었습니다. Secrets 설정을 다시 확인하세요.")
        return

    print("📡 Gist 업데이트 중...")
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    payload = {
        "files": {
            "RadioStreamer.json": {
                "content": json.dumps(radio_list, ensure_ascii=False, indent=2)
            }
        }
    }

    gist_api_url = f"https://api.github.com/gists/{GIST_ID}"
    response = requests.patch(gist_api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("🎉 모든 주소가 Gist에 업데이트되었습니다!")
    else:
        print(f"❌ Gist 업데이트 실패: {response.status_code}")
        print(f"메시지: {response.text}")

if __name__ == "__main__":
    main()
