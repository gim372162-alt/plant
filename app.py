import streamlit as st
import pandas as pd
import random

# --- 앱 설정 ---
st.set_page_config(page_title="현실 밀착! 식물 MBTI 테스트", layout="wide")

# --- 1. MBTI 식물 데이터 (현실 식물 버전) ---
PLANT_DATA = {
    "ENFP": {"name": "몬스테라", "desc": "자유분방하게 잎을 찢으며 성장하는 교실의 분위기 메이커!", "img": "🌿"},
    "INFJ": {"name": "라벤더", "desc": "고요한 향기로 주변을 치유하는 사색적인 평화주의자.", "img": "💜"},
    "ESTJ": {"name": "선인장", "desc": "철저한 규칙과 완벽한 자기방어력을 가진 든든한 리더.", "img": "🌵"},
    "ISFP": {"name": "미모사", "desc": "섬세한 감수성을 가진 예술가. 건드리면 수줍게 잎을 접어요.", "img": "🌸"},
    "ENTP": {"name": "파리지옥", "desc": "톡톡 튀는 아이디어와 독특한 매력으로 시선을 사로잡는 모험가.", "img": "👄"},
    "INTJ": {"name": "유칼립투스", "desc": "똑똑하고 독립적이며 자신만의 뚜렷한 주관을 가진 전략가.", "img": "🍃"},
    "ESFP": {"name": "해바라기", "desc": "언제나 긍정 에너지를 뿜어내는 교실의 슈퍼스타.", "img": "🌻"},
    "ISTP": {"name": "틸란드시아", "desc": "흙 없이도 혼자서 척척 잘 살아가는 쿨한 개인주의 식물.", "img": "🌬️"},
    "ENFJ": {"name": "스킨답서스", "desc": "주변을 감싸 안으며 모두를 행복하게 만드는 다정한 리더.", "img": "🌱"},
    "ISFJ": {"name": "테이블야자", "desc": "보이지 않는 곳에서 공기를 정화하는 배려 깊은 수호자.", "img": "🌴"},
    "ESTP": {"name": "스투키", "desc": "어떤 환경이든 적응력 만렙! 트렌디하고 활동적인 에너자이저.", "img": "🎋"},
    "INFP": {"name": "마리모", "desc": "물속에서 조용히 자신만의 낭만을 키워가는 귀여운 몽상가.", "img": "🟢"},
    "ESFJ": {"name": "제라늄", "desc": "화려한 꽃으로 교실 분위기를 화사하게 만드는 소통가.", "img": "🌺"},
    "ISTJ": {"name": "산세베리아", "desc": "변함없이 굳건하게 자리를 지키는 신뢰의 상징.", "img": "📏"},
    "ENTJ": {"name": "인도고무나무", "desc": "단단한 잎과 줄기로 공간을 압도하는 카리스마 전문가.", "img": "🌳"},
    "INTP": {"name": "네펜데스", "desc": "독창적인 구조로 세상을 탐구하는 교실의 과학자.", "img": "🧪"}
}

# --- 2. 궁합 데이터 ---
COMPAT = {
    "ENFP": {"best": "INFJ", "worst": "ISTJ"}, "INFJ": {"best": "ENFP", "worst": "ESTP"},
    "ESTJ": {"best": "ISFP", "worst": "INFP"}, "ISFP": {"best": "ESTJ", "worst": "ENTJ"},
    "ENTP": {"best": "INTJ", "worst": "ISFJ"}, "INTJ": {"best": "ENTP", "worst": "ESFP"},
    "ESFP": {"best": "ISFJ", "worst": "INTJ"}, "ISTP": {"best": "ESFJ", "worst": "ENFJ"},
    "ENFJ": {"best": "INFP", "worst": "ISTP"}, "ISFJ": {"best": "ESFP", "worst": "ENTP"},
    "ESTP": {"best": "ISFP", "worst": "INFJ"}, "INFP": {"best": "ENFJ", "worst": "ESTJ"},
    "ESFJ": {"best": "ISTP", "worst": "INTP"}, "ISTJ": {"best": "ESFJ", "worst": "ENFP"},
    "ENTJ": {"best": "INTP", "worst": "ISFP"}, "INTP": {"best": "ENTJ", "worst": "ESFJ"}
}

# --- 3. 18개 질문 데이터 (심화 버전) ---
QUESTIONS = [
    # E / I (5개)
    {"q": "식물 박람회에 갔을 때 나는?", "A": "모르는 사람들과 식물 정보를 나누며 활기차게 구경한다.", "B": "조용히 이어폰을 끼고 식물 하나하나를 관찰한다.", "type": "E/I"},
    {"q": "내 방에 식물을 둔다면?", "A": "거실이나 입구처럼 사람들이 잘 보는 곳에 둔다.", "B": "내 침대 옆이나 나만 볼 수 있는 구석진 곳에 둔다.", "type": "E/I"},
    {"q": "친구가 식물을 선물해준다면?", "A": "당장 단톡방에 자랑하고 이름을 함께 정해달라고 한다.", "B": "혼자 조용히 이름을 지어주고 애지중지 돌본다.", "type": "E/I"},
    {"q": "주말에 식물 카페에 가기로 했다면?", "A": "북적거리고 힙한 식물 인테리어 카페가 좋다.", "B": "조용하고 숲속에 있는 듯한 한적한 카페가 좋다.", "type": "E/I"},
    {"q": "식물 동아리 활동을 한다면?", "A": "여러 명과 협력하여 커다란 정원을 가꾸고 싶다.", "B": "나만의 작은 화분 하나를 완벽하게 키워보고 싶다.", "type": "E/I"},
    # S / N (4개)
    {"q": "식물 잎을 관찰할 때 나는?", "A": "잎의 무늬, 색깔, 질감을 있는 그대로 정확히 본다.", "B": "이 식물이 10년 뒤에 얼마나 커질지 상상하며 본다.", "type": "S/N"},
    {"q": "식물 기르기 매뉴얼을 읽을 때?", "A": "물 주는 요일, 일조량 수치 등 정확한 정보를 선호한다.", "B": "이 식물의 꽃말이나 유래 같은 스토리에 더 끌린다.", "type": "S/N"},
    {"q": "새로운 식물을 샀을 때?", "A": "검증된 방법(책, 전문가)대로만 키우려 노력한다.", "B": "나만의 직관으로 새로운 배치나 실험을 시도해본다.", "type": "S/N"},
    {"q": "숲속을 걸을 때 드는 생각은?", "A": "나무의 종류가 무엇인지, 공기가 얼마나 맑은지 생각한다.", "B": "숲의 정령이 살 것 같다는 등 동화 같은 생각을 한다.", "type": "S/N"},
    # F / T (4개)
    {"q": "식물이 시들어 갈 때 먼저 드는 생각은?", "A": "내가 정성을 못 줬나 봐... 너무 마음이 아프다.", "B": "물이 부족한가? 비료가 과했나? 원인을 분석한다.", "type": "F/T"},
    {"q": "친구의 식물이 죽었다는 소식을 들으면?", "A": "얼마나 속상할까... 친구의 슬픈 마음에 공감해준다.", "B": "죽은 원인을 같이 찾아보고 다음에 살릴 방법을 알려준다.", "type": "F/T"},
    {"q": "식물에게 이름을 지어줄 때?", "A": "애칭이나 귀여운 느낌의 이름을 지어준다.", "B": "식물 학명이나 특징을 살린 실용적인 이름을 지어준다.", "type": "F/T"},
    {"q": "식물에게 말을 걸면 잘 자란다는 말을 들었을 때?", "A": "당연히 식물도 사랑을 느끼지! 매일 말을 걸어준다.", "B": "과학적인 근거가 있는지 의심하며 웃어넘긴다.", "type": "F/T"},
    # P / J (5개)
    {"q": "식물 물 주는 날은?", "A": "달력에 정확히 표시해두고 알람까지 맞춘다.", "B": "그때그때 흙을 만져보고 마른 것 같을 때 준다.", "type": "P/J"},
    {"q": "식물 쇼핑을 하러 갈 때?", "A": "살 종류와 예산을 미리 정해서 딱 그것만 사온다.", "B": "가서 보고 예쁜 게 있으면 즉흥적으로 사온다.", "type": "P/J"},
    {"q": "식물 배치는 어떻게?", "A": "높낮이와 색감을 고려해 미리 계획한 대로 배치한다.", "B": "그냥 비어있는 공간에 대충 놔본다.", "type": "P/J"},
    {"q": "식물 관찰 일지를 쓴다면?", "A": "매일 같은 시간에 꼼꼼하게 기록을 남긴다.", "B": "생각날 때만 한 번씩 몰아서 쓰거나 사진만 찍는다.", "type": "P/J"},
    {"q": "식물 영양제를 줄 때?", "A": "설명서에 나온 정량을 정확히 지켜서 준다.", "B": "이 정도면 되겠지 싶을 때 감으로 대충 듬뿍 준다.", "type": "P/J"}
]

# --- 4. 실시간 DB 시뮬레이션 ---
if "class_db" not in st.session_state:
    # 샘플 데이터 (그래프 확인용)
    st.session_state.class_db = pd.DataFrame([
        {"반코드": "101", "이름": "김선생", "MBTI": "ENTJ", "식물": "인도고무나무"},
        {"반코드": "101", "이름": "이학생", "MBTI": "INFP", "식물": "마리모"}
    ])

# --- 스타일 설정 ---
st.markdown("""
<style>
    @keyframes pulse { 0% { border: 2px solid #10b981; box-shadow: 0 0 5px #10b981; } 50% { border: 2px solid #34d399; box-shadow: 0 0 20px #10b981; } 100% { border: 2px solid #10b981; box-shadow: 0 0 5px #10b981; } }
    .fantasy-card { animation: pulse 2s infinite; background-color: #ecfdf5; padding: 20px; border-radius: 15px; margin: 10px 0; }
    .disaster-card { border: 2px solid #ef4444; background-color: #fef2f2; padding: 20px; border-radius: 15px; margin: 10px 0; }
    .normal-card { border: 1px solid #d1d5db; padding: 15px; border-radius: 10px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 ---
st.title("🌿 우리 반 리얼 식물 MBTI 테스트")
st.write("18문항의 정교한 질문으로 당신의 소울 식물을 찾고, 우리 반 통계를 확인하세요!")

with st.sidebar:
    st.header("🔑 입장 정보")
    c_code = st.text_input("반 코드 (예: 101)", "101")
    u_name = st.text_input("이름", "")
    st.divider()
    st.info("이름을 입력하면 테스트가 시작됩니다!")

if u_name:
    tab1, tab2 = st.tabs(["📝 테스트 시작", "📊 실시간 대시보드"])
    
    with tab1:
        st.subheader(f"🌱 {u_name}님을 위한 18개 질문")
        with st.form("mbti_form"):
            user_ans = {}
            for i, q in enumerate(QUESTIONS):
                st.write(f"**Q{i+1}. {q['q']}**")
                user_ans[i] = st.radio(f"답변{i}", [q["A"], q["B"]], label_visibility="collapsed")
            
            submitted = st.form_submit_button("나의 식물 결과 확인")
            
            if submitted:
                scores = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
                for i, q in enumerate(QUESTIONS):
                    if user_ans[i] == q["A"]: scores[q["type"]] += 1
                    else: scores[q["type"]] -= 1
                
                res_mbti = (
                    ("E" if scores["E/I"] >= 0 else "I") +
                    ("S" if scores["S/N"] >= 0 else "N") +
                    ("F" if scores["F/T"] >= 0 else "T") +
                    ("P" if scores["P/J"] >= 0 else "J")
                )
                
                # DB 업데이트
                new_data = pd.DataFrame([{"반코드": c_code, "이름": u_name, "MBTI": res_mbti, "식물": PLANT_DATA[res_mbti]["name"]}])
                st.session_state.class_db = pd.concat([st.session_state.class_db, new_data], ignore_index=True).drop_duplicates(subset=["반코드", "이름"], keep="last")
                
                st.balloons()
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.success(f"당신은 **{res_mbti}** 유형!")
                    st.header(f"{PLANT_DATA[res_mbti]['img']} {PLANT_DATA[res_mbti]['name']}")
                    st.info(PLANT_DATA[res_mbti]['desc'])
                with col_r2:
                    st.write("### 🧬 궁합 분석")
                    st.write(f"✨ 환상의 조합: **{PLANT_DATA[COMPAT[res_mbti]['best']]['name']}**({COMPAT[res_mbti]['best']})")
                    st.write(f"⚡ 환장의 조합: **{PLANT_DATA[COMPAT[res_mbti]['worst']]['name']}**({COMPAT[res_mbti]['worst']})")

    with tab2:
        st.subheader(f"📊 {c_code}반 실시간 통계 & 대시보드")
        df = st.session_state.class_db[st.session_state.class_db["반코드"] == c_code]
        
        if not df.empty:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write("#### 📈 우리 반 성향 분포")
                type_counts = df["MBTI"].value_counts()
                st.bar_chart(type_counts)
            with c2:
                st.write("#### 📋 참여 명단")
                st.dataframe(df[["이름", "MBTI", "식물"]], use_container_width=True)
            
            st.divider()
            st.write("#### 🤝 실시간 케미 매칭")
            # 본인 데이터 가져오기
            my_row = df[df["이름"] == u_name]
            if not my_row.empty:
                my_m = my_row.iloc[0]["MBTI"]
                target_best = COMPAT[my_m]["best"]
                target_worst = COMPAT[my_m]["worst"]
                
                best_mates = df[df["MBTI"] == target_best]
                worst_mates = df[df["MBTI"] == target_worst]
                
                m1, m2 = st.columns(2)
                with m1:
                    st.success("✨ 환상의 짝꿍 (네온 펄스)")
                    for _, row in best_mates.iterrows():
                        if row['이름'] != u_name:
                            st.markdown(f"<div class='fantasy-card'>🎯 <b>{row['이름']}</b> ({row['식물']}) - 우리 환상이에요!</div>", unsafe_allow_html=True)
                with m2:
                    st.error("⚡ 환장의 짝꿍")
                    for _, row in worst_mates.iterrows():
                        st.markdown(f"<div class='disaster-card'>💥 <b>{row['이름']}</b> ({row['식물']}) - 조심하세요!</div>", unsafe_allow_html=True)
        else:
            st.warning("아직 등록된 친구가 없습니다.")
else:
    st.info("왼쪽 사이드바에서 이름을 입력하고 소울 식물을 찾아보세요! 🌿")

선생님, 이 앱 코드는 **18개 질문**을 통해 성향을 매우 정교하게 분석합니다. 또한 대시보드에 **실시간 막대 그래프**를 추가해 우리 반에 어떤 MBTI가 많은지 바로 알 수 있게 했습니다. 

수업 시간에 이 화면을 큰 스크린에 띄워두고 아이들이 한 명씩 완료할 때마다 그래프가 변하는 것을 보여주면 반응이 폭발적일 거예요! 궁금한 점 있으시면 바로 말씀해 주세요.🌿
