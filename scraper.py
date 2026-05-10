import requests
import json
import os
import time

# 1. 설정값 
GIST_ID = "3613497490a95c68cf2a7f3e45a3bdc3"
GH_TOKEN = os.environ.get("GIST_TOKEN") 

def get_radio_urls():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })

    radio_results = []

    # --- 1. MBC 수집 로직 (최신 API) ---
    print("📡 MBC 최신 서버 연결 중...")
    for cid, name, internal_id in [("MBC_FM4U", "MBC FM4U", "mfm"), ("MBC_STD", "MBC 표준FM", "sfm")]:
        try:
            url = f"https://sminiplay.imbc.com/aacplay.ashx?agent=webapp&channel={internal_id}"
            res = session.get(url, timeout=10)
            addr = res.text.strip()
            
            if addr.startswith("http"):
                radio_results.append({"id": cid, "name": name, "url": addr})
                print(f"{name}: ✅ 성공")
            else:
                radio_results.append({"id": cid, "name": name, "url": ""})
                print(f"{name}: ❌ 실패")
        except Exception as e:
            radio_results.append({"id": cid, "name": name, "url": ""})
            print(f"{name}: ❌ 실패")
        time.sleep(1)

    # --- 2. KBS 수집 로직 (최신 API) ---
    print("📡 KBS 최신 서버 연결 중...")
    for cid, name, kid in [("KBS_COOL", "KBS CoolFM", "24"), ("KBS_1R", "KBS 1라디오", "21"), ("KBS_2R", "KBS 2라디오", "22")]:
        try:
            url = f"https://cfpwwwapi.kbs.co.kr/api/v1/landing/live/channel_code/{kid}"
            res = session.get(url, timeout=10)
            data = res.json()
            addr = data.get('channel_item', [{}])[0].get('service_url', "")
            
            radio_results.append({"id": cid, "name": name, "url": addr})
            print(f"{name}: {'✅ 성공' if addr else '❌ 실패'}")
        except Exception as e:
            radio_results.append({"id": cid, "name": name, "url": ""})
            print(f"{name}: ❌ 실패")
        time.sleep(1)

    # --- 3. SBS 수집 로직 (마지막 퍼즐: 최신 텍스트 API 적용!) ---
    print("📡 SBS 최신 서버 연결 중...")
    for cid, name, pc_code, fm_code in [("SBS_POWER", "SBS 파워FM", "powerpc", "powerfm"), 
                                        ("SBS_LOVE", "SBS 러브FM", "lovepc", "lovefm")]:
        try:
            # SBS도 MBC처럼 텍스트 주소만 뱉어내는 최신 API로 변경되었습니다.
            url = f"https://apis.sbs.co.kr/play-api/1.0/livestream/{pc_code}/{fm_code}?protocol=hls&ssl=Y"
            res = session.get(url, headers={'Referer': 'https://play.sbs.co.kr/'}, timeout=10)
            addr = res.text.strip()
            
            # 주소가 http로 시작하면 정상!
            if addr.startswith("http"):
                radio_results.append({"id": cid, "name": name, "url": addr})
                print(f"{name}: ✅ 성공")
            else:
                radio_results.append({"id": cid, "name": name, "url": ""})
                print(f"{name}: ❌ 실패")
        except Exception as e:
            radio_results.append({"id": cid, "name": name, "url": ""})
            print(f"{name}: ❌ 실패")
        time.sleep(1)

    return radio_results

def main():
    print("🚀 최신 API 엔진으로 라디오 주소 수집 시작...\n")
    
    radio_list = get_radio_urls()

    if not GH_TOKEN or GH_TOKEN.startswith("ghp_여기에"):
        print("\n❌ 에러: GH_TOKEN 잊지 말고 꼭 넣어주세요!")
        return

    print("\n📡 Gist 업데이트 중...")
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"files": {"RadioStreamer.json": {"content": json.dumps(radio_list, ensure_ascii=False, indent=2)}}}
    
    res = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)
    if res.status_code == 200:
        print("🎉 모든 방송국(MBC, KBS, SBS) 퍼즐 완성! Gist 업데이트 성공!")
    else:
        print(f"❌ Gist 업데이트 실패: {res.status_code}")

if __name__ == "__main__":
    main()
