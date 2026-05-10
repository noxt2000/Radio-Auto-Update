import requests
import json
import os

# 1. 설정값 확인
GIST_ID = "3613497490a95c68cf2a7f3e45a3bdc3"
GH_TOKEN = os.environ.get("GIST_TOKEN") 

# 방송국 서버를 완벽하게 속이기 위한 '진짜 브라우저' 헤더
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_sbs_url(channel_id):
    try:
        api_url = f"https://apis.sbs.co.kr/play-api/get-streaming-url?channel={channel_id}&protocol=hls&device=pc"
        h = HEADERS.copy()
        h['Referer'] = 'https://play.sbs.co.kr/'
        res = requests.get(api_url, headers=h, timeout=10)
        return res.json().get('url', "")
    except: return ""

def get_mbc_url(type_id):
    try:
        api_url = f"https://control.imbc.com/v2/item/getItem?item=audio&channel={type_id}&agent=pc&protocol=hls"
        h = HEADERS.copy()
        h['Referer'] = 'https://mini.imbc.com/'
        res = requests.get(api_url, headers=h, timeout=10)
        return res.json().get('MediaUrl', "")
    except: return ""

def get_kbs_url(channel_id):
    try:
        api_url = f"https://api.kbs.co.kr/p27/2plus/menu/get_streaming_url?channel_id={channel_id}&protocol=hls"
        res = requests.get(api_url, headers=HEADERS, timeout=10)
        return res.json().get('url', "")
    except: return ""

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
        print(f"{ch['name']}: {'✅ 성공' if ch['url'] else '❌ 실패'}")

    if not GH_TOKEN:
        print("❌ 에러: GIST_TOKEN이 없습니다.")
        return

    print("📡 Gist 업데이트 중...")
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"files": {"RadioStreamer.json": {"content": json.dumps(radio_list, ensure_ascii=False, indent=2)}}}
    
    res = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)
    if res.status_code == 200:
        print("🎉 업데이트 완료!")
    else:
        print(f"❌ 실패: {res.status_code} {res.text}")

if __name__ == "__main__":
    main()
