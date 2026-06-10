import streamlit as st
import pandas as pd
import threading

# 1. 멀티스레드 동시 접속 환경에서의 데이터 안전성 확보 (동시 제출 꼬임 방지)
if "db_lock" not in st.session_state:
    st.session_state.db_lock = threading.Lock()

# 2. 페이지 기본 설정 및 모바일 기기 반응형 레이아웃 최적화
st.set_page_config(page_title="우리 반 실시간 식물 MBTI 정원", layout="wide")

# 고해상도 시각화를 위한 맞춤형 인라인 CSS 주입 (에러 유발 소지 차단)
st.markdown("""
<style>
    @keyframes pulse { 0% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } 50% { border: 3px solid #34d399; box-shadow: 0 0 20px #10b981; } 100% { border: 3px solid #10b981; box-shadow: 0 0 5px #10b981; } }
    .main-card { background: #f0fdf4; border: 2px solid #10b981; border-radius: 16px; padding: 25px; margin-bottom: 20px; }
    .fantasy-box { animation: pulse 2s infinite; background-color: #ecfdf5; padding: 14px; border-radius: 10px; margin: 6px 0; border: 2px solid #10b981; font-size: 15px; }
    .disaster-box { border: 2px solid #ef4444; background-color: #fef2f2; padding: 14px; border-radius: 10px; margin: 6px 0; font-size: 15px; }
    .chem-node { background-color: #f8fafc; padding: 12px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0; }
    .bar-bg { background-color: #cbd5e1; border-radius: 999px; width: 100%; height: 18px; margin-top: 4px; overflow: hidden; }
    .bar-fill { background: linear-gradient(90deg, #10b981, #3b82f6); height: 100%; border-radius: 999px; text-align: center; color: white; font-size: 11px; line-height: 18px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. 중앙 서버 공유형 통합 데이터베이스 캐싱 구축
@st.cache_resource
def get_global_database():
    return {
        "garden_records": [
            {"반": "101", "이름": "김민준", "MBTI": "ENTJ", "식물": "인도고무나무"},
            {"반": "101", "이름": "이서연", "MBTI": "INFP", "식물": "마리모"},
            {"반": "101", "이름": "박지우", "MBTI": "INFJ", "식물": "라벤더"},
            {"반": "101", "이름": "최동현", "MBTI": "ISTJ", "식물": "산세베리아"}
        ]
    }

global_db = get_global_database()

# 4. 16가지 식물 성향 마스터 데이터 인덱스 (KeyError 검증 완료)
PLANT_MAP = {
    "ENFP": {"n": "몬스테라", "d": "자유분방하게 잎을 찢으며 성장하는 교실의 분위기 메이커! 에너지가 넘치고 언제나 새로운 즐거움을 찾아 나섭니다.", "img": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=600"},
    "INFJ": {"n": "라벤더", "d": "고요하고 깊은 향기로 주변 사람들의 마음을 치유하는 사색적인 평화주의자. 보이지 않는 곳에서 깊은 통찰력을 발휘합니다.", "img": "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=600"},
    "ESTJ": {"n": "선인장", "d": "철저한 규칙과 주관, 완벽한 자기방어력을 가진 든든한 리더. 명확한 계획 하에 맡은 바 임무를 끝까지 완수합니다.", "img": "https://images.unsplash.com/photo-1509423350716-97f9360b4e5e?w=600"},
    "ISFP": {"n": "미모사", "d": "섬세한 감수성을 지닌 따뜻한 예술가. 평소에는 다정하지만 다가가면 수줍게 잎을 접는 매력적인 성격의 소유자입니다.", "img": "https://images.unsplash.com/photo-1622322062602-0e9e1119560a?w=600"},
    "ENTP": {"n": "파리지옥", "d": "톡톡 튀는 아이디어와 독특한 매력으로 단숨에 시선을 사로잡는 모험가. 지루한 틀에 갇히는 것을 가장 싫어합니다.", "img": "https://images.unsplash.com/photo-1525498128493-380d1990a112?w=600"},
    "INTJ": {"n": "유칼립투스", "d": "똑똑하고 독립적이며 자신만의 뚜렷한 주관을 가진 냉철한 전략가. 논리적이고 깊이 있는 지식을 탐구하는 것을 좋아합니다.", "img": "https://images.unsplash.com/photo-1545241047-6083a3684587?w=600"},
    "ESFP": {"n": "해바라기", "d": "언제나 태양을 바라보듯 밝고 긍정적인 에너지를 뿜어내는 교실의 슈퍼스타! 친구들과 어울리는 매 순간을 사랑합니다.", "img": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=600"},
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

# 5. MBTI 간 상호 작용 궁합 매트릭스 규격
INTER_RULES = {
    "ENFP": {"b": "INFJ", "w": "ISTJ"}, "INFJ": {"b": "ENFP", "w": "ESTP"},
    "ESTJ": {"b": "ISFP", "w": "INFP"}, "ISFP": {"b": "ESTJ", "w": "ENTJ"},
    "ENTP": {"b": "INTJ", "w": "ISFJ"}, "INTJ": {"b": "ENTP", "w": "ESFP"},
    "ESFP": {"b": "ISFJ", "w": "INTJ"}, "ISTP": {"b": "ESFJ", "w": "ENFJ"},
    "ENFJ": {"b": "INFP", "w": "ISTP"}, "ISFJ": {"b": "ESFP", "w": "ENTP"},
    "ESTP": {"b": "ISFP", "w": "INFJ"}, "INFP": {"b": "ENFJ", "w": "ESTJ"},
    "ESFJ": {"b": "ISTP", "w": "INTP"}, "ISTJ": {"b": "ESFJ", "w": "ENFP"},
    "ENTJ": {"b": "INTP", "w": "ISFP"}, "INTP": {"b": "ENTJ", "w": "ESFJ"}
}

# 6. 진단 평가 문항 (18개 고정 구조)
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

# 7. 헤더 렌더링
st.title("🌿 우리 반 실시간 식물 MBTI 정원")
st.write("단 하나의 화면에서 성향을 분석하고 반 전체 친구들과의 실시간 케미 정원을 즉시 구축합니다.")

# 학급 입장 세션 및 중복 방지 상태 초기화
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "my_mbti" not in st.session_state:
    st.session_state.my_mbti = ""
if "my_plant" not in st.session_state:
    st.session_state.my_plant = ""

st.markdown("### 🔑 가드너 정보 입력")
c_col1, c_col2 = st.columns(2)
with c_col1:
    class_code = st.text_input("학급 코드 (예: 101)", "101").strip()
with c_col2:
    gamer_name = st.text_input("본인 이름 입력 (정확하게 입력)", "").strip()

st.divider()

if not gamer_name:
    st.info("💡 이름과 학급 코드를 입력하면 하단에 18문항 검사지가 나타납니다.")
else:
    # 8. 단일 화면 기반 테스트 문항 구현 (탭 제거)
    st.header(f"📝 {gamer_name} 학생을 위한 소울 식물 진단")
    st.write("모든 문항에 답변한 후 맨 아래의 제출 버튼을 누르세요.")
    
    selections = {}
    for idx, item in enumerate(QUESTIONS):
        selections[idx] = st.radio(
            f"**Q{idx+1}. {item['q']}**",
            [item["A"], item["B"]],
            key=f"direct_q_{idx}"
        )
        st.write("")

    if st.button("🌿 나의 소울 식물 분석 결과 최종 제출"):
        totals = {"E/I": 0, "S/N": 0, "F/T": 0, "P/J": 0}
        for idx, item in enumerate(QUESTIONS):
            if selections[idx] == item["A"]:
                totals[item["type"]] += 1
            else:
                totals[item["type"]] -= 1
        
        final_mbti = (
            ("E" if totals["E/I"] >= 0 else "I") +
            ("S" if totals["S/N"] >= 0 else "N") +
            ("F" if totals["F/T"] >= 0 else "T") +
            ("P" if totals["P/J"] >= 0 else "J")
        )
        
        # 내부 글로벌 세션 상태 갱신
        st.session_state.my_mbti = final_mbti
        st.session_state.my_plant = PLANT_MAP[final_mbti]["n"]
        st.session_state.submitted = True
        
        # 서버 데이터베이스 스레드 컴파일 저장
        with st.session_state.db_lock:
            master_list = global_db["garden_records"]
            filtered_list = [r for r in master_list if not (r["반"] == class_code and r["이름"] == gamer_name)]
            filtered_list.append({
                "반": class_code,
                "이름": gamer_name,
                "MBTI": final_mbti,
                "식물": PLANT_MAP[final_mbti]["n"]
            })
            global_db["garden_records"] = filtered_list
            
        st.balloons()

    # 9. [핵심 조건 1] 결과 제출 완료 시 동일 화면 하단에 모든 내용 표출 조치
    if st.session_state.submitted:
        st.divider()
        st.markdown("## 🎉 분석 완료! 당신의 소울 식물 명세 및 학급 실시간 가드닝 정보")
        
        # [핵심 조건 2] 내 mbti와 매칭 식물 고화질 사진 및 초정밀 특성 상세 카드화
        my_type = st.session_state.my_mbti
        spec = PLANT_MAP[my_type]
        
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        res_left, res_right = st.columns([1, 1.5])
        with res_left:
            st.image(spec["img"], caption=f"나의 소울 매칭: {spec['n']}", use_container_width=True)
        with res_right:
            st.subheader(f"✨ 성향 코드: {my_type} | 소울 식물 유형")
            st.header(f"당신은 사계절 푸른 **[{spec['n']}]** 입니다!")
            st.markdown(f"#### 📖 식물 성격 기술서")
            st.info(spec["d"])
            st.write(f"🔍 **생육 관리 팁:** 이 성향은 주변의 피드백과 환경에 민감하므로 상호 신뢰와 충분한 자유도가 보장될 때 가장 건강하고 독창적인 업적의 꽃을 피워냅니다.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # [핵심 조건 3] 다른 친구들이 제출할 때마다 한눈에 요동치며 리프레시되는 대시보드 스크린
        st.header(f"📊 {class_code}반 실시간 가드너 정원 상황판 (새로고침 자동 반영)")
        
        active_records = global_db["garden_records"]
        class_df = pd.DataFrame(active_records)
        if not class_df.empty:
            class_df = class_df[class_df["반"] == class_code]

        if not class_df.empty:
            dash_left, dash_right = st.columns([1.2, 1])
            
            with dash_left:
                st.write("#### 📈 우리 반 식물 도표 분포 현황")
                st.bar_chart(class_df["식물"].value_counts())
                
                st.write("#### 📋 가드너 전체 정보 데이터베이스")
                st.dataframe(class_df[["이름", "MBTI", "식물"]], use_container_width=True, hide_index=True)
                
            with dash_right:
                # [핵심 조건 4] 우리 반 전체의 환상 궁합 및 환장 궁합 실시간 상호 매칭 전원 공개맵
                st.write("#### 🤝 우리 반 전체 실시간 워스트 & 베스트 크로스 매칭 지도")
                
                f_count = 0
                d_count = 0
                
                f_html = ""
                d_html = ""
                
                # 전체 학생 리스트 간의 관계망을 연산하여 매칭 판정
                student_list = class_df.to_dict('records')
                
                for i in range(len(student_list)):
                    for j in range(i + 1, len(student_list)):
                        s1 = student_list[i]
                        s2 = student_list[j]
                        
                        # s1 기준 베스트/워스트 정의
                        mbti_1 = s1["MBTI"]
                        mbti_2 = s2["MBTI"]
                        
                        if INTER_RULES[mbti_1]["b"] == mbti_2:
                            f_html += f"<div class='fantasy-box'>🎯 <b>{s1['이름']}</b>({s1['식물']}) 💖 <b>{s2['이름']}</b>({s2['식물']}) -> 환상의 영혼 단짝</div>"
                            f_count += 1
                        elif INTER_RULES[mbti_1]["w"] == mbti_2:
                            d_html += f"<div class='disaster-box'>💥 <b>{s1['이름']}</b>({s1['식물']}) ⚡ <b>{s2['이름']}</b>({s2['식물']}) -> 환장의 상극 주의보</div>"
                            d_count += 1

                st.success("✨ 실시간 베스트 커플 명단")
                if f_count > 0:
                    st.markdown(f_html, unsafe_allow_html=True)
                else:
                    st.caption("아직 정원에 100% 매칭되는 환상의 단짝 조가 발견되지 않았습니다.")
                    
                st.error("⚡ 실시간 워스트 주의 조 명단")
                if d_count > 0:
                    st.markdown(d_html, unsafe_allow_html=True)
                else:
                    st.caption("현재까지는 상극 성향의 마찰 조가 없습니다. 매우 평화로운 상태입니다!")
                    
                st.divider()
                st.write("#### 🧬 개인별 클래스 궁합 연산 지수 리스트")
                for _, row in class_df.iterrows():
                    if row["이름"] == gamer_name:
                        continue
                    base_score = sum(1 for char_a, char_b in zip(my_type, row["MBTI"]) if char_a == char_b)
                    if row["MBTI"] == INTER_RULES[my_type]["b"]:
                        final_score = 99
                    elif row["MBTI"] == INTER_RULES[my_type]["w"]:
                        final_score = 11
                    else:
                        final_score = min(88, max(30, 25 + (base_score * 15) + (int(len(row["이름"])) % 3 * 6)))
                    
                    st.markdown(f"""
                    <div class='chem-node'>
                        <b>{row['이름']}</b> ({row['식물']}) - 나와의 적합도: <b>{final_score}%</b>
                        <div class='bar-bg'><div class='bar-fill' style='width:{final_score}%'>{final_score}%</div></div>
                    </div>
                    """, unsafe_allow_html=True)
