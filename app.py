import streamlit as st
import pandas as pd
import time
import random

# Page Configuration
st.set_page_config(page_title="교실 속 식물 MBTI 테스트", layout="wide", initial_sidebar_state="expanded")

# --- 1. MBTI & 식물 매칭 데이터 정의 ---
MBTI_PLANTS = {
    "ENFP": {"name": "몬스테라", "desc": "자유롭게 잎을 찢으며 무한 성장하는 교실의 핵인싸 식물!"},
    "INFJ": {"name": "라벤더", "desc": "깊은 향기로 주변을 차분하게 치유해 주는 사색적인 식물."},
    "ESTJ": {"name": "선인장", "desc": "철저한 규칙과 규칙적인 관리 속에서 가장 곧게 자라는 식물."},
    "ISFP": {"name": "미모사", "desc": "자극에 민감하지만 누구보다 따뜻하고 예술적인 감수성을 가진 식물."},
    "ENTP": {"name": "파리지옥", "desc": "호기심 가득! 독특한 매력으로 사람들의 시선을 사로잡는 식물."},
    "INTJ": {"name": "유칼립투스", "desc": "독립적이고 스마트하며, 자신만의 뚜렷한 주관을 가진 식물."},
    "ESFP": {"name": "해바라기", "desc": "언제나 태양을 바라보듯 긍정적이고 에너지가 넘치는 식물."},
    "ISTP": {"name": "틸란드시아", "desc": "흙 없이도 혼자서 척척 잘 살아가는 쿨한 공중 식물."},
    "ENFJ": {"name": "스킨답서스", "desc": "주변 식물들을 감싸 안으며 모두를 행복하게 만드는 리더 식물."},
    "ISFJ": {"name": "테이블야자", "desc": "보이지 않는 곳에서 공기를 정화해 주는 묵묵한 배려의 식물."},
    "ESTP": {"name": "스투키", "desc": "어떤 환경이든 적응력 만렙! 트렌디하고 활동적인 식물."},
    "INFP": {"name": "마리모", "desc": "물속에서 조용히 자신만의 낭만을 키워가는 귀여운 수중 식물."},
    "ESFJ": {"name": "제라늄", "desc": "화려한 꽃으로 교실 분위기를 화사하게 만드는 다정한 소통가 식물."},
    "ISTJ": {"name": "산세베리아", "desc": "변함없이 굳건하게 자리를 지키는 교실의 든든한 버팀목 식물."},
    "ENTJ": {"name": "인도고무나무", "desc": "단단한 잎과 줄기로 공간을 압도하는 카리스마 리더 식물."},
    "INTP": {"name": "네펜데스", "desc": "독창적인 구조로 세상을 탐구하는 교실 속의 과학자 식물."}
}

# --- 2. MBTI 궁합 매트릭스 정의 ---
COMPATIBILITY = {
    "ENFP": {"환상": "INFJ", "환장": "ISTJ"}, "INFJ": {"환상": "ENFP", "환장": "ESTP"},
    "ESTJ": {"환상": "ISFP", "환장": "INFP"}, "ISFP": {"환상": "ESTJ", "환장": "ENTJ"},
    "ENTP": {"환상": "INTJ", "환장": "ISFJ"}, "INTJ": {"환상": "ENTP", "환장": "ESFP"},
    "ESFP": {"환상": "ISFJ", "환장": "INTJ"}, "ISTP": {"환상": "ESFJ", "환장": "ENFJ"},
    "ENFJ": {"환상": "INFP", "환장": "ISTP"}, "ISFJ": {"환상": "ESFP", "환장": "ENTP"},
    "ESTP": {"환상": "ISFP", "환장": "INFJ"}, "INFP": {"환상": "ENFJ", "환장": "ESTJ"},
    "ESFJ": {"환상": "ISTP", "환장": "INTP"}, "ISTJ": {"환상": "ESFJ", "환장": "ENFP"},
    "ENTJ": {"환상": "INTP", "환장": "ISFP"}, "INTP": {"환상": "ENTJ", "환장": "ESFJ"}
}

# --- 3. MBTI 식물 관련 질문 12개 ---
QUESTIONS = [
    {"q": "1. 식물원 체험학습을 갈 때 나는?", "A": "친구들과 모여서 수다 떨며 시끌벅적하게 가고 싶다.", "B": "친한 친구 한두 명과 조용히 식물을 관찰하며 가고 싶다.", "type": "E/I"},
    {"q": "2. 새로 산 화분을 방에 둘 때 나의 행동은?", "A": "눈에 잘 띄고 예쁜 곳에 일단 올려둔다.", "B": "햇빛 양, 통풍 위치를 꼼꼼히 계산해서 최적의 자리에 둔다.", "type": "P/J"},
    {"q": "3. 시들어가는 식물을 보았을 때 먼저 드는 생각은?", "A": "헉, 불쌍해... 왜 시들었지? 속상하다.", "B": "물이 부족한가? 과습인가? 원인을 분석해야겠다.", "type": "F/T"},
    {"q": "4. 식물 가꾸기 관찰 일지를 쓸 때 나는?", "A": "오늘 식물이 얼마나 자랐는지 눈에 보이는 대로 정확히 기록한다.", "B": "식물이 자라는 모습을 보며 느낀 감상이나 상상을 더해 기록한다.", "type": "S/N"},
    {"q": "5. 주말에 친구가 깜짝 식물 마켓에 가자고 한다면?", "A": "좋아! 당장 가자! 계획 없어도 재밌겠다.", "B": "미리 말해줬으면 좋았을 텐데... 동선을 생각하느라 고민된다.", "type": "P/J"},
    {"q": "6. 친구가 '나 오늘 우울해서 반려식물 샀어'라고 한다면?", "A": "무슨 일 있어? 왜 우울해? 기분은 좀 나아졌어?", "B": "오 무슨 식물 샀어? 키우기 쉬운 거야?", "type": "F/T"},
    {"q": "7. 식물원 가이드 투어를 들을 때 나는?", "A": "설명해 주는 식물의 이름과 특징을 그대로 기억하려 노력한다.", "B": "식물의 유래나 비밀스러운 이야기에 상상의 나래를 편다.", "type": "S/N"},
    {"q": "8. 식물 동아리에서 새로운 사람들을 만났을 때 나는?", "A": "먼저 다가가 인사를 건네고 말을 트는 편이다.", "B": "상대방이 먼저 말을 걸어올 때까지 기다리는 편이다.", "type": "E/I"},
    {"q": "9. 방학 동안 식물 키우기 숙제를 받았다면?", "A": "미리 요일별로 물 주는 계획표를 짜서 벽에 붙여둔다.", "B": "생각날 때나 흙이 마른 것 같아 보일 때 유연하게 준다.", "type": "P/J"},
    {"q": "10. '말을 알아듣는 신비한 식물'이 있다면?", "A": "말도 안 돼, 과학적으로 불가능해.", "B": "와 진짜 신기하다! 매일 비밀 이야기를 털어놔야지.", "type": "S/N"},
    {"q": "11. 친구가 정성껏 키운 식물이 죽어서 울고 있다면?", "A": "휴지를 건네며 슬픈 마음에 깊이 공감해 준다.", "B": "울지 마, 다음엔 영양제를 주거나 다르게 키워보자 해결책을 준다.", "type": "F/T"},
    {"q": "12. 식물 박람회에 도착했을 때 나의 행동은?", "A": "지도를 보며 어디부터 갈지 순서를 정하고 움직인다.", "B": "발길이 이끄는 대로, 눈에 띄는 화려한 부스부터 구경한다.", "type": "P/J"}
]

# --- 4. 가상 실시간 데이터베이스 (초기화) ---
if "class_db" not in st.session_state:
    # 예시용 가상 데이터 미리 넣어두기 (실시간 동기화 느낌 전달용)
    st.session_state.class_db = pd.DataFrame([
        {"반코드": "301", "이름": "김민준", "MBTI": "ENFP", "식물": "몬스테라"},
        {"반코드": "301", "이름": "이서연", "MBTI": "INFJ", "식물": "라벤더"},
        {"반코드": "301", "이름": "박지훈", "MBTI": "ISTJ", "식물": "산세베리아"},
        {"반코드": "301", "이름": "최예은", "MBTI": "ESTP", "식물": "스투키"},
        {"반코드": "302", "이름": "홍길동", "MBTI": "INFP", "식물": "마리모"}
    ])

# --- Custom CSS (환상궁합 애니메이션 테두리 포함) ---
st.markdown("""
<style>
    @keyframes pulse-border {
        0% { border-color: rgba(46, 204, 113, 0.4); box-shadow: 0 0 5px rgba(46, 204, 113, 0.2); }
        50% { border-color: rgba(46, 204, 113, 1); box-shadow: 0 0 15px rgba(46, 204, 113, 0.6); }
        100% { border-color: rgba(46, 204, 113, 0.4); box-shadow: 0 0 5px rgba(46, 204, 113, 0.2); }
    }
    .best-match-card {
        border: 2px solid #2ecc71;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f4fbf7;
        animation: pulse-border 2s infinite ease-in-out;
    }
    .worst-match-card {
        border: 2px solid #e74c3c;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #fdf2f2;
    }
    .normal-match-card {
        border: 1px solid #dcdde1;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #ffffff;
    }
    .title-text {
        text-align: center;
        color: #2c3e50;
        font-family: 'Nanum Gothic', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. 사이드바: 실시간 로그인/입력란 ---
with st.sidebar:
    st.header("🌿 교실 접속 정보")
    room_code = st.text_input("반 코드 입력 (예: 301)", value="301")
    student_name = st.text_input("본인 이름 입력", value="")
    
    st.divider()
    st.markdown("💡 **선생님 가이드:**\n학생들에게 동일한 '반 코드'를 입력하게 하세요. 로그인 없이 실시간 데이터가 한 대시보드로 동기화됩니다.")

st.markdown("<h1 class='title-text'>🌱 내 맘속의 작은 정원: 식물 MBTI 테스트</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>나와 닮은 식물을 찾고 우리 반 친구들과의 실시간 궁합을 확인해봐요!</p>", unsafe_allow_html=True)
st.divider()

if not student_name:
    st.warning("👈 먼저 왼쪽 사이드바에서 **이름**을 입력해 주셔야 테스트를 시작할 수 있습니다!")
else:
    # --- 6. 테스트 진행 화면 ---
    st.subheader(f"📝 {student_name} 학생의 식물 성향 테스트 (12문항)")
    
    scores = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
    
    # 12개 질문 출력 및 답변 수집
    with st.form("mbti_form"):
        answers = {}
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**{q['q']}**")
            answers[i] = st.radio(f"선택 {i}", [q["A"], q["B"]], label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            
        submit_btn = st.form_submit_with_button("🌿 나의 식물 결과 확인하고 실시간 동기화하기")
        
    if submit_btn:
        # MBTI 계산 계산
        for i, q in enumerate(QUESTIONS):
            q_type = q["type"]
            if answers[i] == q["A"]:
                # A를 선택했을 때의 성향 매칭
                if q_type == "E/I": scores["E/I"] += 1
                elif q_type == "S/N": scores["S/N"] += 1
                elif q_type == "F/T": scores["F/T"] += 1
                elif q_type == "P/J": scores["P/J"] += 1
            else:
                # B를 선택했을 때
                if q_type == "E/I": scores["E/I"] -= 1
                elif q_type == "S/N": scores["S/N"] -= 1
                elif q_type == "F/T": scores["F/T"] -= 1
                elif q_type == "P/J": scores["P/J"] -= 1
                
        my_mbti = (
            ("E" if scores["E/I"] >= 0 else "I") +
            ("S" if scores["S/N"] >= 0 else "N") +
            ("F" if scores["F/T"] >= 0 else "T") +
            ("P" if scores["P/J"] >= 0 else "J")
        )
        
        my_plant = MBTI_PLANTS[my_mbti]["name"]
        my_desc = MBTI_PLANTS[my_mbti]["desc"]
        
        # 실시간 DB 업데이트 (기존 데이터 있으면 덮어쓰기, 없으면 추가)
        db = st.session_state.class_db
        db = db[~((db["반코드"] == room_code) & (db["이름"] == student_name))] # 기존 데이터 제거
        new_row = pd.DataFrame([{"반코드": room_code, "이름": student_name, "MBTI": my_mbti, "식물": my_plant}])
        st.session_state.class_db = pd.concat([db, new_row], ignore_index=True)
        
        # --- 7. 결과 화면 렌더링 ---
        st.balloons()
        st.success("🎉 테스트 완료! 데이터가 교실 대시보드에 실시간 동기화되었습니다.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"### 🌸 {student_name}님의 식물 MBTI: **{my_mbti}**")
            st.markdown(f"## 당신은 영혼의 반려식물 **[{my_plant}]** 입니다!")
            st.info(my_desc)
            
            # 가상 이미지 박스 (체험용 일러스트 공간)
            st.image("https://images.unsplash.com/photo-1545241047-6083a3684587?w=500", 
                     caption=f"아름답게 자라나는 {my_plant}의 모습 (예시 사진)", use_container_width=True)
            
        with col2:
            st.markdown(f"### 📊 우리 반 ({room_code}반) 실시간 매칭 실황")
            
            # 같은 반 학생 데이터만 필터링
            class_mates = st.session_state.class_db[st.session_state.class_db["반코드"] == room_code]
            
            target_best = COMPATIBILITY[my_mbti]["환상"]
            target_worst = COMPATIBILITY[my_mbti]["환장"]
            
            # 1. 환상의 조합 출력
            st.markdown("#### ✨ 🤝 환상의 조합 (Soulmates)")
            best_mates = class_mates[class_mates["MBTI"] == target_best]
            if not best_mates.empty:
                for _, mate in best_mates.iterrows():
                    st.markdown(f"""
                    <div class="best-match-card">
                        🎯 <b>{mate['이름']}</b> ({mate['MBTI']} - {mate['식물']})<br>
                        <small style="color: #27ae60;">서로 최고의 시너지를 내는 완벽한 식물 생태계 파트너!</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption(f"아직 우리 반에 환상의 조합({target_best})을 가진 친구가 없습니다. 친구들을 독려해 보세요!")
                
            # 2. 환장의 조합 출력
            st.markdown("#### ⚡ 🌵 환장의 조합 (Tom & Jerry)")
            worst_mates = class_mates[class_mates["MBTI"] == target_worst]
            if not worst_mates.empty:
                for _, mate in worst_mates.iterrows():
                    st.markdown(f"""
                    <div class="worst-match-card">
                        🔥 <b>{mate['이름']}</b> ({mate['MBTI']} - {mate['식물']})<br>
                        <small style="color: #c0392b;">물 주는 주기부터 햇빛 취향까지 정반대! 다름을 인정하면 최고의 절친이 될지도?</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption(f"아직 우리 반에 환장의 조합({target_worst})을 가진 친구가 없습니다.")
                
            # 3. 다른 중간 조합 퍼센트로 나타내기
            st.markdown("#### 🌿 다른 친구들과의 케미 지수")
            other_mates = class_mates[(class_mates["이름"] != student_name) & 
                                      (class_mates["MBTI"] != target_best) & 
                                      (class_mates["MBTI"] != target_worst)]
            
            if not other_mates.empty:
                for _, mate in other_mates.iterrows():
                    # MBTI 글자 일치 개수에 따라 재미용 퍼센트 랜덤/매칭 계산
                    match_count = sum(1 for a, b in zip(my_mbti, mate['MBTI']) if a == b)
                    pct = 30 + (match_count * 15) + random.randint(-5, 5) # 기본 30% + 일치당 15% + 약간의 변동
                    pct = min(max(pct, 15), 90) # 15% ~ 90% 사이 제한
                    
                    st.markdown(f"""
                    <div class="normal-match-card">
                        🌱 <b>{mate['이름']}</b> ({mate['MBTI']} - {mate['식물']})
                        <div style="background-color: #ddd; border-radius: 10px; width: 100%;">
                            <div style="background-color: #3498db; width: {pct}%; padding: 2px 0; text-align: center; color: white; border-radius: 10px; font-size: 11px;">
                                {pct}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("비교할 다른 반 친구들이 아직 없습니다.")
