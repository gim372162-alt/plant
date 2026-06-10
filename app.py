import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (태블릿/모바일 모두 최적화)
st.set_page_config(page_title="우리 반 식물 MBTI", layout="wide")

# 2. 현실 기반 16가지 식물 데이터 정의
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

# 3. 절대 깨지지 않는 엄선된 18개 심화 질문 리스트
QUESTIONS = [
    {"q": "식물 박람회에 갔을 때 나는?", "A": "모르는 사람들과 식물 정보를 나누며 활기차게 구경한다.", "B": "조용히 이어폰을 끼고 식물 하나하나를 관찰한다.", "type": "E/I"},
    {"q": "내 방에 식물을 둔다면?", "A": "거실이나 입구처럼 사람들이 잘 보는 곳에 둔다.", "B": "내 침대 옆이나 나만 볼 수 있는 구석진 곳에 둔다.", "type": "E/I"},
    {"q": "친구가 식물을 선물해준다면?", "A": "당장 단톡방에 자랑하고 이름을 함께 정해달라고 한다.", "B": "혼자 조용히 이름을 지어주고 애지중지 돌본다.", "type": "E/I"},
    {"q": "주말에 식물 카페에 가기로 했다면?", "A": "북적거리고 힙한 식물 인테리어 카페가 좋다.", "B": "조용하고 숲속에 있는 듯한 한적한 카페가 좋다.", "type": "E/I"},
    {"q": "식물 동아리 활동을 한다면?", "A": "여러 명과 협력하여 커다란 정원을 가꾸고 싶다.", "B": "나만의 작은 화분 하나를 완벽하게 키워보고 싶다.", "type": "E/I"},
    {"q": "식물 잎을 관찰할 때 나는?", "A": "잎의 무늬, 색깔, 질감을 있는 그대로 정확히 본다.", "B": "이 식물이 10년 뒤에 얼마나 커질지 상상하며 본다.", "type": "S/N"},
    {"q": "식물 기르기 매뉴얼을 읽을 때?", "A": "물 주는 요일, 일조량 수치 등 정확한 정보를 선호한다.", "B": "이 식물의 꽃말이나 유래 같은 스토리에 더 끌린다.", "type": "S/N"},
    {"q": "새로운 식물을 샀을 때?", "A": "검증된 방법(책, 전문가)대로만 키우려 노력한다.", "B": "나만의 직관으로 새로운 배치나 실험을 시도해본다.", "type": "S/N"},
    {"q": "숲속을 걸을 때 드는 생각은?", "A": "나무의 종류가 무엇인지, 공기가 얼마나 맑은지 생각한다.", "B": "숲의 정령이 살 것 같다는 등 동화 같은 생각을 한다.", "type": "S/N"},
    {"q": "식물이 시들어 갈 때 먼저 드는 생각은?", "A": "내가 정성을 못 줬나 봐... 너무 마음이 아프다.", "B": "물이 부족한가? 비료가 과했나? 원인을 분석한다.", "type": "F/T"},
    {"q": "친구의 식물이 죽었다는 소식을 들으면?", "A": "얼마나 속상할까... 친구의 슬픈 마음에 공감해준다.", "B": "죽은 원인을 같이 찾아보고 다음에 살릴 방법을 알려준다.", "type": "F/T"},
    {"q": "식물에게 이름을 지어줄 때?", "A": "애칭이나 귀여운 느낌의 이름을 지어준다.", "B": "식물 학명이나 특징을 살린 실용적인 이름을 지어준다.", "type": "F/T"},
    {"q": "식물에게 말을 걸면 잘 자란다는 말을 들었을 때?", "A": "당연히 식물도 사랑을 느끼지! 매일 말을 걸어준다.", "B": "과학적인 근거가 있는지 의심하며 웃어넘긴다.", "type": "F/T"},
    {"q": "식물 물 주는 날은?", "A": "달력에 정확히 표시해두고 알람까지 맞춘다.", "B": "그때그때 흙을 만져보고 마른 것 같을 때 준다.", "type": "P/J"},
    {"q": "식물 쇼핑을 하러 갈 때?", "A": "살 종류와 예산을 미리 정해서 딱 그것만 사온다.", "B": "가서 보고 예쁜 게 있으면 즉흥적으로 사온다.", "type": "P/J"},
    {"q": "식물 배치는 어떻게?", "A": "높낮이와 색감을 고려해 미리 계획한 대로 배치한다.", "B": "그냥 비어있는 공간에 대충 놔본다.", "type": "P/J"},
    {"q": "식물 관찰 일지를 쓴다면?", "A": "매일 같은 시간에 꼼꼼하게 기록을 남긴다.", "B": "생각날 때만 한 번씩 몰아서 쓰거나 사진만 찍는다.", "type": "P/J"},
    {"q": "식물 영양제를 줄 때?", "A": "설명서에 나온 정량을 정확히 지켜서 준다.", "B": "이 정도면 되겠지 싶을 때 감으로 대충 듬뿍 준다.", "type": "P/J"}
]

# 4. 가상 DB 공간 안전 확보
if "db_list" not in st.session_state:
    st.session_state.db_list = [
        {"반코드": "101", "이름": "김민준", "MBTI": "ENTJ", "식물": "인도고무나무"},
        {"반코드": "101", "이름": "이서연", "MBTI": "INFP", "식물": "마리모"},
        {"반코드": "101", "이름": "박지우", "MBTI": "INFJ", "식물": "라벤더"}
    ]

# 5. UI 및 스타일 주입
st.markdown("""
<style>
    @keyframes pulse { 0% { border: 2px solid #10b981; box-shadow: 0 0 5px #10b981; } 50% { border: 2px solid #34d399; box-shadow: 0 0 20px #10b981; } 100% { border: 2px solid #10b981; box-shadow: 0 0 5px #10b981; } }
    .fantasy-card { animation: pulse 2s infinite; background-color: #ecfdf5; padding: 18px; border-radius: 12px; margin: 8px 0; }
    .disaster-card { border: 2px solid #ef4444; background-color: #fef2f2; padding: 18px; border-radius: 12px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 우리 반 실시간 식물 MBTI 교실")
st.write("나의 리얼 일상 속 태도로 소울 식물을 찾고, 친구들과의 실시간 식물 지도를 완성해 보세요.")

st.markdown("### 🔑 기본 정보 입력")
c1, c2 = st.columns(2)
with c1:
    c_code = st.text_input("학급 코드 입력 (예: 101)", "101").strip()
with c2:
    u_name = st.text_input("이름을 입력해 주세요", "").strip()

st.divider()

if u_name:
    t1, t2 = st.tabs(["📝 MBTI 테스트 진행", "📊 학급 실시간 대시보드"])
    
    with t1:
        st.info("모든 문항에 체크한 뒤 맨 아래 [결과 제출하기] 버튼을 눌러주세요.")
        user_ans = {}
        
        # 모바일 화면 가독성 극대화를 위한 디자인 매핑
        for i, q in enumerate(QUESTIONS):
            user_ans[i] = st.radio(
                f"**Q{i+1}. {q['q']}**", 
                [q["A"], q["B"]], 
                key=f"real_q_{i}"
            )
            st.write("")
            
        if st.button("🚀 나의 식물 결과 제출하기"):
            scores = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
            for i, q in enumerate(QUESTIONS):
                if user_ans[i] == q["A"]:
                    scores[q["type"]] += 1
                else:
                    scores[q["type"]] -= 1
                    
            res_mbti = (
                ("E" if scores["E/I"] >= 0 else "I") +
                ("S" if scores["S/N"] >= 0 else "N") +
                ("F" if scores["F/T"] >= 0 else "T") +
                ("P" if scores["P/J"] >= 0 else "J")
            )
            
            # 중복 데이터 제거 방식의 간소화 안정화 로직
            st.session_state.db_list = [item for item in st.session_state.db_list if not (item["반코드"] == c_code and item["이름"] == u_name)]
            st.session_state.db_list.append({
                "반코드": c_code, 
                "이름": u_name, 
                "MBTI": res_mbti, 
                "식물": PLANT_DATA[res_mbti]["name"]
            })
            
            st.balloons()
            
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.success(f"🎉 테스트 완료! 당신은 {res_mbti}입니다.")
                st.header(f"{PLANT_DATA[res_mbti]['img']} {PLANT_DATA[res_mbti]['name']}")
                st.info(PLANT_DATA[res_mbti]['desc'])
            with r_col2:
                st.write("#### 🧬 소울 궁합 매칭")
                st.write(f"💚 환상의 단짝: **{PLANT_DATA[COMPAT[res_mbti]['best']]['name']}** ({COMPAT[res_mbti]['best']})")
                st.write(f"💔 환장의 상성: **{PLANT_DATA[COMPAT[res_mbti]['worst']]['name']}** ({COMPAT[res_mbti]['worst']})")

    with t2:
        df = pd.DataFrame(st.session_state.db_list)
        class_df = df[df["반코드"] == c_code]
        
        if not class_df.empty:
            d_col1, d_col2 = st.columns([2, 1])
            with d_col1:
                st.write("#### 📈 우리 반 식물 분포 현황")
                st.bar_chart(class_df["MBTI"].value_counts())
            with d_col2:
                st.write("#### 📋 가드너 참여 명단")
                st.dataframe(class_df[["이름", "MBTI", "식물"]], use_container_width=True, hide_index=True)
                
            st.divider()
            st.write("#### 🤝 실시간 케미 매칭 상황")
            
            my_info = class_df[class_df["이름"] == u_name]
            if not my_info.empty:
                my_mbti = my_info.iloc[0]["MBTI"]
                b_mbti = COMPAT[my_mbti]["best"]
                w_mbti = COMPAT[my_mbti]["worst"]
                
                m1, m2 = st.columns(2)
                with m1:
                    st.success("✨ 실시간 우리 반 단짝 (Pulse)")
                    for _, row in class_df.iterrows():
                        if row["MBTI"] == b_mbti and row["이름"] != u_name:
                            st.markdown(f"<div class='fantasy-card'>🎯 <b>{row['이름']}</b> ({row['식물']}) 님이 당신의 소울 가드너입니다!</div>", unsafe_allow_html=True)
                with m2:
                    st.error("⚡ 주의 요망 상성")
                    for _, row in class_df.iterrows():
                        if row["MBTI"] == w_mbti and row["이름"] != u_name:
                            st.markdown(f"<div class='disaster-card'>💥 <b>{row['이름']}</b> ({row['식물']}) 님과 가치관 조율이 필요합니다!</div>", unsafe_allow_html=True)
        else:
            st.warning("등록된 데이터가 없습니다. 먼저 테스트를 완료해 주세요.")
else:
    st.info("💡 위 입력창에 본인의 이름과 학급 코드를 입력하면 즉시 18개 질문이 나타납니다.")
