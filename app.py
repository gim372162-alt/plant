import streamlit as st
import pandas as pd
import random

# 1. 기본 설정 및 디자인 테마
st.set_page_config(page_title="우리반 식물 MBTI", layout="wide")

st.markdown("""
<style>
    @keyframes pulse { 0% { border: 3px solid #00ff88; box-shadow: 0 0 5px #00ff88; } 50% { border: 3px solid #00ff88; box-shadow: 0 0 20px #00ff88; } 100% { border: 3px solid #00ff88; box-shadow: 0 0 5px #00ff88; } }
    .fantasy-card { animation: pulse 2s infinite; background-color: #f0fff4; padding: 20px; border-radius: 15px; margin: 10px 0; border: 2px solid #00ff88; }
    .disaster-card { border: 3px solid #ff4b4b; background-color: #fff5f5; padding: 20px; border-radius: 15px; margin: 10px 0; }
    .chem-bar-bg { background-color: #eee; border-radius: 10px; width: 100%; height: 20px; margin-top: 5px; }
    .chem-bar-fill { background: linear-gradient(90deg, #34d399, #3b82f6); height: 100%; border-radius: 10px; text-align: center; color: white; font-size: 12px; line-height: 20px; }
    .stRadio > div { background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# 2. 식물 데이터 (이름, 이미지, 설명)
PLANT_DB = {
    "ENFP": {"n": "몬스테라", "d": "자유롭게 잎을 찢으며 성장하는 교실 인싸! 에너지가 넘쳐요.", "img": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=500"},
    "INFJ": {"n": "라벤더", "d": "깊은 향기로 주변을 치유하는 사색가. 조용한 평화를 사랑해요.", "img": "https://images.unsplash.com/photo-1595163363023-745a7698517c?w=500"},
    "ESTJ": {"n": "선인장", "d": "철저한 자기관리와 규칙! 어떤 환경에서도 굳건한 리더입니다.", "img": "https://images.unsplash.com/photo-1509423350716-97f9360b4e5e?w=500"},
    "ISFP": {"n": "미모사", "d": "섬세한 감수성을 가진 예술가. 건드리면 수줍게 잎을 접는 매력.", "img": "https://images.unsplash.com/photo-1622322062602-0e9e1119560a?w=500"},
    "ENTP": {"n": "파리지옥", "d": "독특하고 똑똑한 아이디어 뱅크! 지루한 건 딱 질색이에요.", "img": "https://images.unsplash.com/photo-1599144365312-f28876a4ee0f?w=500"},
    "INTJ": {"n": "유칼립투스", "d": "전략적이고 스마트한 독립가. 자신만의 목표가 뚜렷합니다.", "img": "https://images.unsplash.com/photo-1545241047-6083a3684587?w=500"},
    "ESFP": {"n": "해바라기", "m": "언제나 태양을 보듯 긍정적! 주변에 웃음을 주는 스타 식물.", "img": "https://images.unsplash.com/photo-1470472304068-4398a9daab00?w=500"},
    "ISTP": {"n": "틸란드시아", "d": "흙 없이도 잘 자라는 쿨한 개인주의자. 적응력이 최고예요.", "img": "https://images.unsplash.com/photo-1508608825823-187510526732?w=500"},
    "ENFJ": {"n": "스킨답서스", "d": "모두를 따뜻하게 감싸 안는 소통가. 함께 있을 때 빛나요.", "img": "https://images.unsplash.com/photo-1599202860130-f600f4948364?w=500"},
    "ISFJ": {"n": "테이블야자", "d": "조용히 공기를 정화해주는 배려의 수호자. 변치 않는 우정.", "img": "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=500"},
    "ESTP": {"n": "스투키", "d": "트렌디하고 활동적인 에너자이저! 모험을 두려워하지 않아요.", "img": "https://images.unsplash.com/photo-1598592232741-5747bcc2436a?w=500"},
    "INFP": {"n": "마리모", "d": "물속에서 낭만을 키우는 몽상가. 작고 소중한 감수성의 소유자.", "img": "https://images.unsplash.com/photo-1605364448408-0902c525167b?w=500"},
    "ESFJ": {"n": "제라늄", "d": "다정한 소통과 나눔의 아이콘. 정원을 화사하게 가꿔줍니다.", "img": "https://images.unsplash.com/photo-1615852503254-ca7924d6739f?w=500"},
    "ISTJ": {"n": "산세베리아", "d": "정직하고 성실한 원칙주의자. 믿음직한 교실의 기둥입니다.", "img": "https://images.unsplash.com/photo-1593433551532-c13f64567756?w=500"},
    "ENTJ": {"n": "고무나무", "d": "강력한 리더십과 카리스마! 목표를 향해 거침없이 나아갑니다.", "img": "https://images.unsplash.com/photo-1616400619175-50ac0f7eba7c?w=500"},
    "INTP": {"n": "네펜데스", "d": "독창적인 구조를 가진 논리 술사. 궁금한 건 못 참아요.", "img": "https://images.unsplash.com/photo-1525498128493-380d1990a112?w=500"}
}

# 3. 궁합 매트릭스
MATCH_RULES = {
    "ENFP": {"b": "INFJ", "w": "ISTJ"}, "INFJ": {"b": "ENFP", "w": "ESTP"},
    "ESTJ": {"b": "ISFP", "w": "INFP"}, "ISFP": {"b": "ESTJ", "w": "ENTJ"},
    "ENTP": {"b": "INTJ", "w": "ISFJ"}, "INTJ": {"b": "ENTP", "w": "ESFP"},
    "ESFP": {"b": "ISFJ", "w": "INTJ"}, "ISTP": {"b": "ESFJ", "w": "ENFJ"},
    "ENFJ": {"b": "INFP", "w": "ISTP"}, "ISFJ": {"b": "ESFP", "w": "ENTP"},
    "ESTP": {"b": "ISFP", "w": "INFJ"}, "INFP": {"b": "ENFJ", "w": "ESTJ"},
    "ESFJ": {"b": "ISTP", "w": "INTP"}, "ISTJ": {"b": "ESFJ", "w": "ENFP"},
    "ENTJ": {"b": "INTP", "w": "ISFP"}, "INTP": {"b": "ENTJ", "w": "ESFJ"}
}

# 4. 18개 질문지
QS = [
    {"q": "식물 박람회에서 나는?", "a": "활발하게 정보를 묻는다", "b": "조용히 사진만 찍는다", "t": "E/I"},
    {"q": "내 방에 식물을 둔다면?", "a": "거실 정중앙", "b": "나만의 구석진 책상", "t": "E/I"},
    {"q": "식물이 죽었을 때 반응은?", "a": "너무 슬프고 미안하다", "b": "원인을 분석하고 버린다", "t": "F/T"},
    {"q": "식물 이름 짓기?", "a": "귀여운 애칭(초록이)", "b": "실용적인 이름(몬스테라1)", "t": "F/T"},
    {"q": "물 주는 날 정하기?", "a": "요일별로 계획표 작성", "b": "그때그때 감으로", "t": "P/J"},
    {"q": "식물 쇼핑 갈 때?", "a": "살 것만 딱 산다", "b": "이것저것 다 구경한다", "t": "P/J"},
    {"q": "식물 잎을 볼 때?", "a": "색깔과 모양을 정확히 본다", "b": "자라날 미래를 상상한다", "t": "S/N"},
    {"q": "매뉴얼을 읽을 때?", "a": "수치와 통계를 중시", "b": "꽃말과 유래를 중시", "t": "S/N"},
    {"q": "단체 활동 중 내 역할은?", "a": "분위기 주도하기", "b": "조용히 뒤에서 돕기", "t": "E/I"},
    {"q": "주말 식물 카페 투어?", "a": "친구들과 시끌벅적하게", "b": "혼자 여유롭게", "t": "E/I"},
    {"q": "화분이 깨졌다면?", "a": "식물이 다쳤을까 봐 걱정", "b": "치울 방법부터 생각", "t": "F/T"},
    {"q": "식물 영양제 줄 때?", "a": "마음이 동할 때 듬뿍", "b": "정해진 정량만 딱", "t": "P/J"},
    {"q": "새 식물을 골랐을 때?", "a": "예뻐서 바로 샀다", "b": "키우기 쉬운지 확인했다", "t": "S/N"},
    {"q": "분갈이 숙제?", "a": "미리 준비해서 완료", "b": "마감 직전에 허겁지겁", "t": "P/J"},
    {"q": "식물 선물하기?", "a": "내가 정성껏 키운 것", "b": "상대에게 유용한 것", "t": "F/T"},
    {"q": "관찰 일지 쓰기?", "a": "사실 위주로 꼼꼼히", "b": "감상 위주로 자유롭게", "t": "S/N"},
    {"q": "동아리 회식을 한다면?", "a": "무조건 참석!", "b": "상황 봐서 불참", "t": "E/I"},
    {"q": "말을 듣는 식물이 있다면?", "a": "매일 비밀을 털어놓는다", "b": "원리가 뭔지 연구한다", "t": "S/N"}
]

# 5. 데이터 동기화 (세션)
if "db" not in st.session_state:
    st.session_state.db = [
        {"반": "101", "이름": "김선생", "MBTI": "ENTJ", "식물": "고무나무"},
        {"반": "101", "이름": "이학생", "MBTI": "INFP", "식물": "마리모"}
    ]

# 6. 메인 UI
st.title("🌿 우리 반 실시간 식물 MBTI 정원")
st.write("나와 닮은 식물을 찾고 우리 반 친구들과의 케미를 실시간으로 확인하세요!")

# 상단 정보 입력 (사이드바 대신 메인 배치)
c1, c2 = st.columns(2)
with c1:
    class_id = st.text_input("학급 코드 (예: 101)", "101").strip()
with c2:
    user_name = st.text_input("본인 이름 입력", "").strip()

st.divider()

if not user_name:
    st.info("💡 이름을 입력하시면 테스트가 시작됩니다.")
else:
    tab_test, tab_dash = st.tabs(["📝 테스트", "📊 대시보드"])

    with tab_test:
        st.subheader(f"🌱 {user_name} 학생을 위한 18개 질문")
        ans = {}
        for i, q_item in enumerate(QS):
            ans[i] = st.radio(f"**Q{i+1}. {q_item['q']}**", [q_item["a"], q_item["b"]], key=f"q{i}")
            st.write("")

        if st.button("🌿 나의 식물 결과 확인 및 동기화"):
            s = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
            for i, q_item in enumerate(QS):
                if ans[i] == q_item["a"]: s[q_item["t"]] += 1
                else: s[q_item["t"]] -= 1
            
            mbti = (("E" if s["E/I"] >= 0 else "I") + ("S" if s["S/N"] >= 0 else "N") + 
                    ("F" if s["F/T"] >= 0 else "T") + ("P" if s["P/J"] >= 0 else "J"))
            
            p_res = PLANT_DB[mbti]
            # DB 업데이트 (중복 제거)
            st.session_state.db = [row for row in st.session_state.db if not (row["반"]==class_id and row["이름"]==user_name)]
            st.session_state.db.append({"반": class_id, "이름": user_name, "MBTI": mbti, "식물": p_res["n"]})
            
            st.balloons()
            st.success("데이터가 대시보드에 실시간 반영되었습니다!")
            
            # 결과 카드
            res_c1, res_c2 = st.columns([1, 1.5])
            with res_c1:
                st.image(p_res["img"], caption=f"나의 식물: {p_res['n']}", use_container_width=True)
            with res_c2:
                st.header(f"당신은 **[{p_res['n']}]** 입니다!")
                st.subheader(f"유형: {mbti}")
                st.write(p_res["d"])
                st.divider()
                st.write(f"✨ 환상 궁합: **{PLANT_DB[MATCH_RULES[mbti]['b']]['n']}**")
                st.write(f"💔 환장 상성: **{PLANT_DB[MATCH_RULES[mbti]['w']]['n']}**")

    with tab_dash:
        st.subheader(f"📊 {class_id}반 리얼타임 가드닝 맵")
        df = pd.DataFrame(st.session_state.db)
        my_df = df[df["반"] == class_id]
        
        if not my_df.empty:
            col_graph, col_list = st.columns([1.5, 1])
            with col_graph:
                st.write("#### 📈 우리 반 식물 분포")
                st.bar_chart(my_df["식물"].value_counts())
                
                # 실시간 궁합 섹션
                st.write("#### 🤝 실시간 케미 매칭")
                me = my_df[my_df["이름"] == user_name]
                if not me.empty:
                    my_mbti = me.iloc[0]["MBTI"]
                    target_b = MATCH_RULES[my_mbti]["b"]
                    target_w = MATCH_RULES[my_mbti]["w"]
                    
                    b_list = my_df[my_df["MBTI"] == target_b]
                    w_list = my_df[my_df["MBTI"] == target_w]
                    
                    m_c1, m_c2 = st.columns(2)
                    with m_c1:
                        st.markdown("**✨ 환상 궁합**")
                        if b_list.empty: st.caption("아직 없어요")
                        for _, r in b_list.iterrows():
                            st.markdown(f"<div class='fantasy-card'>🎯 <b>{r['이름']}</b> ({r['식물']})</div>", unsafe_allow_html=True)
                    with m_c2:
                        st.markdown("**⚡ 환장 상성**")
                        if w_list.empty: st.caption("아직 없어요")
                        for _, r in w_list.iterrows():
                            st.markdown(f"<div class='disaster-card'>💥 <b>{row['이름']}</b> ({r['식물']})</div>", unsafe_allow_html=True)
            
            with col_list:
                st.write("#### 🌿 전체 친구 궁합 지수")
                me = my_df[my_df["이름"] == user_name]
                if not me.empty:
                    my_m = me.iloc[0]["MBTI"]
                    for _, row in my_df.iterrows():
                        if row["이름"] == user_name: continue
                        # 궁합 계산: MBTI 글자 일치 개수 + 랜덤 보정
                        match_cnt = sum(1 for a, b in zip(my_m, row["MBTI"]) if a == b)
                        pct = 25 + (match_cnt * 15) + random.randint(-5, 5)
                        pct = min(99, max(10, pct))
                        
                        st.markdown(f"""
                        <div style='margin-bottom:10px;'>
                            <b>{row['이름']}</b> ({row['식물']}) - {pct}%
                            <div class='chem-bar-bg'><div class='chem-bar-fill' style='width:{pct}%'>{pct}%</div></div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("데이터가 없습니다.")
