import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (스마트폰/태블릿 최적화)
st.set_page_config(page_title="우리 반 식물 MBTI 정원", layout="wide")

# 안전한 인라인 CSS 테마 주입
st.markdown("""
<style>
    @keyframes pulse { 0% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } 50% { border: 3px solid #34d399; box-shadow: 0 0 20px #10b981; } 100% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } }
    .fantasy-card { animation: pulse 2s infinite; background-color: #ecfdf5; padding: 18px; border-radius: 12px; margin: 8px 0; border: 2px solid #10b981; }
    .disaster-card { border: 3px solid #ef4444; background-color: #fef2f2; padding: 18px; border-radius: 12px; margin: 8px 0; }
    .chem-container { background-color: #f8fafc; padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #e2e8f0; }
    .chem-bar-bg { background-color: #cbd5e1; border-radius: 999px; width: 100%; height: 16px; margin-top: 6px; overflow: hidden; }
    .chem-bar-fill { background: linear-gradient(90deg, #10b981, #3b82f6); height: 100%; border-radius: 999px; text-align: center; color: white; font-size: 11px; line-height: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. 16가지 식물의 정확한 고화질 사진 및 매뉴얼 상세 데이터 (KeyError 완벽 차단)
PLANT_DB = {
    "ENFP": {"n": "몬스테라", "d": "자유분방하게 잎을 찢으며 성장하는 교실의 분위기 메이커! 에너지가 넘치고 언제나 새로운 즐거움을 찾아 나섭니다.", "img": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=600"},
    "INFJ": {"n": "라벤더", "d": "고요하고 깊은 향기로 주변 사람들의 마음을 치유하는 사색적인 평화주의자. 보이지 않는 곳에서 깊은 통찰력을 발휘합니다.", "img": "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=600"},
    "ESTJ": {"n": "선인장", "d": "철저한 규칙과 주관, 완벽한 자기방어력을 가진 든든한 리더. 명확한 계획 하에 맡은 바 임무를 끝까지 완수합니다.", "img": "https://images.unsplash.com/photo-1509423350716-97f9360b4e5e?w=600"},
    "ISFP": {"n": "미모사", "d": "섬세한 감수성을 지닌 따뜻한 예술가. 평소에는 다정하지만 다가가면 수줍게 잎을 접는 매력적인 성격의 소유자입니다.", "img": "https://images.unsplash.com/photo-1622322062602-0e9e1119560a?w=600"},
    "ENTP": {"n": "파리지옥", "d": "톡톡 튀는 아이디어와 독특한 매력으로 단숨에 시선을 사로잡는 모험가. 지루한 틀에 갇히는 것을 가장 싫어합니다.", "img": "https://images.unsplash.com/photo-1525498128493-380d1990a112?w=600"},
    "INTJ": {"n": "유칼립투스", "d": "똑똑하고 독립적이며 자신만의 뚜렷한 주관을 가진 냉철한 전략가. 논리적이고 깊이 있는 지식을 탐구하는 것을 좋아합니다.", "img": "https://images.unsplash.com/photo-1545241047-6083a3684587?w=600"},
    "ESFP": {"n": "해바라기", "d": "언제나 태양을 바라보듯 밝고 긍정적인 에너지를 뿜어내는 교실의 슈퍼스타! 친구들과 어울리는 매 순간을 사랑합니다.", "img": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=600"}, # 정확한 해바라기 이미지로 전면 수정
    "ISTP": {"n": "틸란드시아", "d": "흙 없이도 혼자서 바람을 맞으며 척척 잘 살아가는 쿨한 개인주의 식물. 상황 적응력이 뛰어나고 다방면에 손재주가 좋습니다.", "img": "https://images.unsplash.com/photo-1508608825823-187510526732?w=600"},
    "ENFJ": {"n": "스킨답서스", "d": "주변 뼈대를 부드럽게 감싸 안으며 모두를 행복하게 만드는 다정한 가이드. 타인의 성장을 격려하고 돕는 데 아낌이 없습니다.", "img": "https://images.unsplash.com/photo-1599202860130-f600f4948364?w=600"},
    "ISFJ": {"n": "테이블야자", "d": "티 내지 않고 묵묵히 공간의 공기를 정화해주는 배려 깊은 수호자. 주변 사람들을 꼼꼼하고 따뜻하게 챙겨줍니다.", "img": "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=600"},
    "ESTP": {"n": "스투키", "d": "어떤 환경이든 적응력 만렙! 트렌디하고 활동적인 에너자이저입니다. 말보다는 행동으로 직접 부딪히는 것을 선호합니다.", "img": "https://images.unsplash.com/photo-1598592232741-5747bcc2436a?w=600"},
    "INFP": {"n": "마리모", "d": "조용히 물속에서 자신만의 소중한 낭만과 꿈을 키워가는 귀여운 몽상가. 내면의 정서가 깊고 이상적인 세상을 꿈꿉니다.", "img": "https://images.unsplash.com/photo-1605364448408-0902c525167b?w=600"},
    "ESFJ": {"n": "제라늄", "d": "화사한 꽃들로 교실 전체의 분위기를 따뜻하게 활성화시키는 친절한 소통가. 조화로운 인간관계와 정을 소중히 여깁니다.", "img": "https://images.unsplash.com/photo-1615852503254-ca7924d6739f?w=600"},
    "ISTJ": {"n": "산세베리아", "d": "한결같은 모습으로 굳건하게 자리를 지키는 신뢰의 상징. 약속을 철저히 지키며 매사에 책임감이 넘치는 정직한 가드너입니다.", "img": "https://images.unsplash.com/photo-1593433551532-c13f64567756?w=600"},
    "ENTJ": {"n": "인도고무나무", "d": "단단한 잎과 대범한 줄기로 공간을 압도하는 카리스마 전문가. 명확한 비전을 제시하고 목표 달성을 위해 대담하게 전진합니다.", "img": "https://images.unsplash.com/photo-1616400619175-50ac0f7eba7c?w=600"},
    "INTP": {"n": "네펜데스", "d": "독창적인 구조와 원리를 끊임없이 분석하고 탐구하는 교실의 생각하는 가이드. 논리적이고 객관적인 진실을 추구합니다.", "img": "https://images.unsplash.com/photo-1599144365312-f28876a4ee0f?w=600"}
}

# 3. 공식 궁합 관계망
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

# 4. 정식 심화 문항 데이터 구성
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

# 5. 가상 DB 저장소 실시간 활성화
if "class_data_store" not in st.session_state:
    st.session_state.class_data_store = [
        {"반": "101", "이름": "김민준", "MBTI": "ENTJ", "식물": "인도고무나무"},
        {"반": "101", "이름": "이서연", "MBTI": "INFP", "식물": "마리모"},
        {"반": "101", "이름": "박지우", "MBTI": "INFJ", "식물": "라벤더"},
        {"반": "101", "이름": "최동현", "MBTI": "ISTJ", "식물": "산세베리아"}
    ]

# 6. 메인 타이틀 레이아웃
st.title("🌿 우리 반 실시간 식물 MBTI 정원")
st.write("질문에 솔직하게 답하여 소울 식물을 찾고, 우리 반 전체 친구들과의 정밀 케미 지도를 완성해 보세요!")

st.markdown("### 🔑 학급 입장 정보 입력")
col_user1, col_user2 = st.columns(2)
with col_user1:
    class_code = st.text_input("학급 코드 (예: 101)", "101").strip()
with col_user2:
    gamer_name = st.text_input("본인 이름 입력 (정확하게 입력하세요)", "").strip()

st.divider()

if not gamer_name:
    st.info("💡 위 입력창에 본인 이름을 작성하면 맞춤형 18문항 검사지가 즉시 활성화됩니다.")
else:
    tab_run, tab_view = st.tabs(["📝 소울 식물 테스트 진입", "📊 우리 반 실시간 가드닝 대시보드"])

    with tab_test_panel := tab_run:
        st.subheader(f"🌱 {gamer_name} 학생을 위한 전용 문항")
        user_selections = {}
        
        # 화면 깨짐 현상을 원천 방지하는 안전한 순회 렌더링
        for idx, item in enumerate(QUESTIONS):
            user_selections[idx] = st.radio(
                f"**Q{idx+1}. {item['q']}**", 
                [item["A"], item["B"]], 
                key=f"safe_flow_q_{idx}"
            )
            st.write("")

        # 폼 제한을 우회하여 무조건 작동하는 안전 단독 버튼
        if st.button("🌿 나의 소울 식물 분석 및 결과 제출"):
            totals = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
            for idx, item in enumerate(QUESTIONS):
                if user_selections[idx] == item["A"]:
                    totals[item["type"]] += 1
                else:
                    totals[item["type"]] -= 1
            
            final_mbti = (
                ("E" if totals["E/I"] >= 0 else "I") +
                ("S" if totals["S/N"] >= 0 else "N") +
                ("F" if totals["F/T"] >= 0 else "T") +
                ("P" if totals["P/J"] >= 0 else "J")
            )
            
            extracted_plant = PLANT_DB[final_mbti]
            
            # 중복 데이터 실시간 오버라이트 처리
            st.session_state.class_data_store = [row for row in st.session_state.class_data_store if not (row["반"] == class_code and row["이름"] == gamer_name)]
            st.session_state.class_data_store.append({
                "반": class_code,
                "이름": gamer_name,
                "MBTI": final_mbti,
                "식물": extracted_plant["n"]
            })
            
            st.balloons()
            st.success("🎉 분석 완료! 결과가 대시보드 정원에 실시간 반영되었습니다. [📊 우리 반 실시간 가드닝 대시보드] 탭을 확인해 보세요!")
            
            # 대망의 시각적 카드 영역 복구 완료
            panel_left, panel_right = st.columns([1, 1.4])
            with panel_left:
                st.image(extracted_plant["img"], caption=f"나의 소울 식물: {extracted_plant['n']}", use_container_width=True)
            with panel_right:
                st.header(f"당신은 **[{extracted_plant['n']}]** 입니다!")
                st.subheader(f"유형 파악: {final_mbti}")
                st.info(extracted_plant["d"])
                st.divider()
                st.write(f"✨ 환상의 짝꿍 식물: **{PLANT_DB[MATCH_RULES[final_mbti]['b']]['n']}** ({MATCH_RULES[final_mbti]['b']})")
                st.write(f"⚡ 환장의 짝꿍 식물: **{PLANT_DB[MATCH_RULES[final_mbti]['w']]['n']}** ({MATCH_RULES[final_mbti]['w']})")

    with tab_view_panel := tab_view:
        st.subheader(f"📊 {class_code}반 실시간 가드너 대시보드")
        master_df = pd.DataFrame(st.session_state.class_data_store)
        current_class_df = master_df[master_df["반"] == class_code]
        
        if not current_class_df.empty:
            layout_left, layout_right = st.columns([1.4, 1])
            
            with layout_left:
                st.write("#### 📈 우리 반 성향 분포 현황")
                st.bar_chart(current_class_df["식물"].value_counts())
                
                st.divider()
                st.write("#### 🤝 우리 반 타겟 케미 매칭 상황")
                
                viewer_row = current_class_df[current_class_df["이름"] == gamer_name]
                if not viewer_row.empty:
                    v_mbti = viewer_row.iloc[0]["MBTI"]
                    best_target = MATCH_RULES[v_mbti]['b']
                    worst_target = MATCH_RULES[v_mbti]['w']
                    
                    matches_best = current_class_df[current_class_df["MBTI"] == best_target]
                    matches_worst = current_class_df[current_class_df["MBTI"] == worst_target]
                    
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        st.success("✨ 환상의 단짝 (네온 펄스)")
                        if matches_best.empty:
                            st.caption("아직 환상의 단짝 친구가 정원에 입장하지 않았습니다.")
                        for _, r in matches_best.iterrows():
                            if r["이름"] != gamer_name:
                                st.markdown(f"<div class='fantasy-card'>🎯 <b>{r['이름']}</b> ({r['식물']}) - 소울 가드너 콤비!</div>", unsafe_allow_html=True)
                    with sub_col2:
                        st.error("⚡ 환장의 상성")
                        if matches_worst.empty:
                            st.caption("정원에 나와 완전히 반대되는 성향의 친구가 없습니다.")
                        for _, r in matches_worst.iterrows():
                            if r["이름"] != gamer_name:
                                st.markdown(f"<div class='disaster-card'>💥 <b>{r['이름']}</b> ({r['식물']}) - 주의 깊은 대화 필요!</div>", unsafe_allow_html=True)
                else:
                    st.warning("🧐 본인의 매칭 현황을 보려면 먼저 [📝 소울 식물 테스트 진입] 탭에서 결과를 제출해 주세요.")
            
            with layout_right:
                st.write("#### 📋 가드너 명단 및 실시간 전체 궁합")
                viewer_row = current_class_df[current_class_df["이름"] == gamer_name]
                
                if not viewer_row.empty:
                    my_mbti_core = viewer_row.iloc[0]["MBTI"]
                    
                    for _, row in current_class_df.iterrows():
                        if row["이름"] == gamer_name:
                            continue
                        
                        # 고정된 로직 기반의 정밀 퍼센트 산출 지수
                        base_match = sum(1 for char_a, char_b in zip(my_mbti_core, row["MBTI"]) if char_a == char_b)
                        
                        if row["MBTI"] == MATCH_RULES[my_mbti_core]["b"]:
                            computed_pct = 99
                        elif row["MBTI"] == MATCH_RULES[my_mbti_core]["w"]:
                            computed_pct = 12
                        else:
                            computed_pct = 25 + (base_match * 15) + (int(len(row["이름"])) % 3 * 4)
                            computed_pct = min(88, max(30, computed_pct))
                        
                        st.markdown(f"""
                        <div class='chem-container'>
                            <b>{row['이름']}</b> 학생 ({row['식물']})<br>
                            궁합 지수: <b>{computed_pct}%</b>
                            <div class='chem-bar-bg'>
                                <div class='chem-bar-fill' style='width:{computed_pct}%'>{computed_pct}%</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.dataframe(current_class_df[["이름", "MBTI", "식물"]], use_container_width=True, hide_index=True)
        else:
            st.warning("아직 이 학급 코드에 등록된 데이터가 없습니다. 첫 가드너가 되어보세요!")
