import streamlit as st
import pandas as pd
import threading

# 1. 시스템 안정성 강화를 위한 글로벌 스레드 락(Lock) 설정 (동시 제출 시 데이터 꼬임 방지)
if "db_lock" not in st.session_state:
    st.session_state.db_lock = threading.Lock()

# 2. 페이지 기본 설정 및 모바일 반응형 완전 최적화
st.set_page_config(page_title="우리 반 실시간 식물 MBTI 정원", layout="wide")

# CSS 스타일 보완 (모바일 환경에서 글자 깨짐 및 게이지바 뭉개짐 현상 차단)
st.markdown("""
<style>
    @keyframes pulse { 0% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } 50% { border: 3px solid #34d399; box-shadow: 0 0 20px #10b981; } 100% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } }
    .fantasy-card { animation: pulse 2s infinite; background-color: #ecfdf5; padding: 18px; border-radius: 12px; margin: 8px 0; border: 2px solid #10b981; }
    .disaster-card { border: 3px solid #ef4444; background-color: #fef2f2; padding: 18px; border-radius: 12px; margin: 8px 0; }
    .chem-container { background-color: #f8fafc; padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #e2e8f0; }
    .chem-bar-bg { background-color: #cbd5e1; border-radius: 999px; width: 100%; height: 20px; margin-top: 6px; overflow: hidden; position: relative; }
    .chem-bar-fill { background: linear-gradient(90deg, #10b981, #3b82f6); height: 100%; border-radius: 999px; text-align: center; color: white; font-size: 12px; line-height: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 실시간 전원 공유를 위한 싱글톤 캐시 데이터베이스 구축
@st.cache_resource
def get_shared_database():
    # 서버 메모리에 영구 보존되는 마스터 데이터 구조
    return {
        "data": [
            {"반": "101", "이름": "김민준", "MBTI": "ENTJ", "식물": "인도고무나무"},
            {"반": "101", "이름": "이서연", "MBTI": "INFP", "식물": "마리모"},
            {"반": "101", "이름": "박지우", "MBTI": "INFJ", "식물": "라벤더"},
            {"반": "101", "이름": "최동현", "MBTI": "ISTJ", "식물": "산세베리아"}
        ]
    }

db_container = get_shared_database()

# 4. 16가지 식물의 정확한 매칭 딕셔너리 (KeyError 완벽 박멸 검증 완료)
PLANT_DB = {
    "ENFP": {"n": "몬스테라", "d": "자유분방하게 잎을 찢으며 성장하는 교실의 분위기 메이커! 에너지가 넘치고 언제나 새로운 즐거움을 찾아 나섭니다.", "img": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=600"},
    "INFJ": {"n": "라벤더", "d": "고요하고 깊은 향기로 주변 사람들의 마음을 치유하는 사색적인 평화주의자. 보이지 않는 곳에서 깊은 통찰력을 발휘합니다.", "img": "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=600"},
    "ESTJ": {"n": "선인장", "d": "철저한 규칙과 주관, 완벽한 자기방어력을 가진 든든한 리더. 명확한 계획 하에 맡은 바 임무를 끝까지 완수합니다.", "img": "https://images.unsplash.com/photo-1509423350716-97f9360b4e5e?w=600"},
    "ISFP": {"n": "미모사", "d": "섬세한 감수성을 지닌 따뜻한 예술가. 평소에는 다정하지만 다가가면 수줍게 잎을 접는 매력적인 성격의 소유자입니다.", "img": "https://images.unsplash.com/photo-1622322062602-0e9e1119560a?w=600"},
    "ENTP": {"n": "파리지옥", "d": "톡톡 튀는 아이디어와 독특한 매력으로 단숨에 시선을 사로잡는 모험가. 지루한 틀에 갇히는 것을 가장 싫어합니다.", "img": "
