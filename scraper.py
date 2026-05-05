import requests
import json
import os

def get_kbs_url(channel_code):
    return f"https://kbs-hls.kbs.co.kr/radio/{channel_code}/playlist.m3u8"

def get_sbs_url(channel_id):
    return f"https://c15ncmsvc.sbs.co.kr/{channel_id}/_definst_/{channel_id}.stream/playlist.m3u8"

def get_mbc_url(channel_id):
    return f"https://{channel_id}live.imbc.com/audio/{channel_id}/_definst_/{channel_id}.stream/playlist.m3u8"

def update_gist(radio_data):
    gist_id = "3613497490a95c68cf2a7f3e45a3bdc3"
    token = os.getenv("GIST_TOKEN") 
    
    if not token:
        print("❌ GIST_TOKEN이 없습니다.")
        return

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
    print(f"✅ Gist 업데이트 완료: {response.status_code}")

if __name__ == "__main__":
    latest_channels = [
        # ⭐ MBC FM4U 버튼에 '절대 끊기지 않는 글로벌 테스트 방송'을 연결했습니다.
        {"id": "MBC_FM4U", "title": "TEST STREAM", "url": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"},
        
        {"id": "MBC_STD", "title": "MBC 표준FM", "url": get_mbc_url("sfm")},
        {"id": "KBS_COOL", "title": "KBS Cool FM", "url": get_kbs_url("2fm")},
        {"id": "KBS_1R", "title": "KBS 1라디오", "url": get_kbs_url("1r")},
        {"id": "KBS_2R", "title": "KBS 2라디오", "url": get_kbs_url("2r")},
        {"id": "SBS_POWER", "title": "SBS 파워FM", "url": get_sbs_url("sbs_powerfm")},
        {"id": "SBS_LOVE", "title": "SBS 러브FM", "url": get_sbs_url("sbs_lovefm")}
    ]
    update_gist(latest_channels)
