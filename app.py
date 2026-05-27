import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="H.E.A.L. 탐구 질문 및 활동 설계 도우미",
    page_icon="📝",
    layout="wide"
)

APP_TITLE = "H.E.A.L. 탐구 질문 및 활동 설계 도우미"
MODEL_NAME = "gemini-2.0-flash"

# -----------------------------
# 샘플 작품 데이터
# 필요하면 여기 계속 추가 가능
# -----------------------------
POEM_DATA = {
    "봄": [
        {
            "num": "춘사 1수",
            "original": "앞개예 안개 걷고 뒷뫼희 해 비췬다\n배 띄워라 배 띄워라\n밤물은 거의 지고 낮물이 밀려온다\n강촌에 온갖 꽃이 먼 빛이 더욱 좋다",
            "modern": "앞바다에 안개 걷히고 뒷산에 해 비친다\n배 띄워라 배 띄워라\n밤물은 거의 지고 낮물이 밀려온다\n강마을의 온갖 꽃이 멀리서 보니 더욱 좋다"
        },
        {
            "num": "춘사 2수",
            "original": "날이 덥도다 물 위에 고기 뜬다\n닻 들어라 닻 들어라\n갈매기 둘씩 셋씩 오락가락 하는구나\n낚싯대 쥐어 있다 탁주병은 실었느냐",
            "modern": "날이 덥구나 물 위에 고기가 떠오른다\n닻 들어라 닻 들어라\n갈매기가 둘씩 셋씩 오락가락 하는구나\n낚싯대 쥐고 있는데 탁주병은 실었느냐"
        }
    ],
    "여름": [
        {
            "num": "하사 1수",
            "original": "짙은 바람이 물결을 흔든다\n노 저어라 노 저어라\n맑은 여울에 비친 하늘빛이 시원하다",
            "modern": "짙은 바람이 물결을 흔든다\n노 저어라 노 저어라\n맑은 여울에 비친 하늘빛이 시원하다"
        }
    ],
    "가을": [
        {
            "num": "추사 1수",
            "original": "서늘한 바람에 물결이 맑아진다\n돛 달아라 돛 달아라\n가을빛 비친 강촌 풍경이 한층 깊어 보인다",
            "modern": "서늘한 바람에 물결이 맑아진다\n돛 달아라 돛 달아라\n가을빛이 비친 강마을 풍경이 한층 깊어 보인다"
        },
        {
            "num": "추사 2수",
            "original": "강촌에 가을이 드니 고기마다 살쪄 있다\n닻 들어라 닻 들어라\n넓고 맑은 물에 마음껏 즐겨보자\n인간세상을 돌아보니 멀수록 더욱 좋다",
            "modern": "강마을에 가을이 드니 고기마다 살쪄 있구나\n닻 들어라 닻 들어라\n넓고 맑은 물결에 마음껏 즐겨보자\n인간 세상을 돌아보니 멀수록 더욱 좋다"
        }
    ],
    "겨울": [
        {
            "num": "동사 1수",
            "original": "눈 덮인 강가에 고요함이 깃든다\n배 매어라 배 매어라\n차가운 바람 속에도 마음은 맑아진다",
            "modern": "눈 덮인 강가에 고요함이 깃든다\n배 매어라 배 매어라\n차가운 바람 속에서도 마음은 맑아진다"
        }
    ]
}

QUESTION_TYPES = {
    "봄": ["감성 질문", "탐구 질문", "창작 질문", "연결 질문"],
    "여름": ["관계 질문", "갈등 질문", "설득 질문", "실천 질문"],
    "가을": ["문제 질문", "데이터 질문", "해결 질문", "실천 질문"],
    "겨울": ["성찰 질문", "비교 질문", "상상 질문", "표현 질문"]
}

DESIGN_HINTS = {
    "봄": "예) 나는 [자연물]을 탐구해서 시조로 쓰고 [독자]에게 보여주고 싶어.",
    "여름": "예) 나는 [갈등 주제]를 탐구해서 [방법]으로 [대상]에게 알리고 싶어.",
    "가을": "예) 나는 [생태 문제]를 해결하는 [도구]를 만들어 [대상]에게 나눠주고 싶어.",
    "겨울": "예) 나는 [겨울의 느낌]을 담아 [형식]으로 표현해 [대상]과 나누고 싶어."
}

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = []

if "generated_activity" not in st.session_state:
    st.session_state.generated_activity = ""

if "starter_text" not in st.session_state:
    st.session_state.starter_text = ""

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
}
.card {
    border: 1px solid #d9d9d9;
    border-radius: 12px;
    padding: 16px;
    background: #ffffff;
    margin-bottom: 12px;
}
.small-label {
    font-size: 0.88rem;
    color: #555;
    margin-bottom: 6px;
}
.big-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.helper {
    color: #666;
    font-size: 0.92rem;
}
.poem-box {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 14px;
    background: #fafafa;
    white-space: pre-wrap;
    line-height: 1.6;
}
.highlight-box {
    border-left: 4px solid #4f46e5;
    background: #f8f8ff;
    padding: 12px;
    border-radius: 8px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 유틸
# -----------------------------
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return st.session_state.get("manual_api_key", "")

def reset_chat():
    st.session_state.chat = []

def reset_all():
    st.session_state.chat = []
    st.session_state.generated_questions = []
    st.session_state.generated_activity = ""
    st.session_state.starter_text = ""

def build_system_prompt():
    return """
당신은 초등 또는 중등 학습자를 돕는 친절한 국어·탐구 활동 도우미입니다.
다음 원칙을 지켜 답변하세요.

1. 학생 눈높이에 맞는 쉬운 한국어를 사용하세요.
2. 답을 단정적으로 주기보다, 생각을 넓히는 질문을 함께 제안하세요.
3. 활동 아이디어는 실제로 수행 가능해야 합니다.
4. 폭력적, 혐오적, 성적 표현은 피하고 바른 언어로 안내하세요.
5. 결과는 되도록 번호 목록과 짧은 문단으로 정리하세요.
6. 필요하면 예시를 1~2개만 간단히 드세요.
"""

def make_starter(area_num, title, title_real, season, goal, theme, poem_num):
    return f"""안녕하세요. 저는 {season} 주제탐구를 준비하고 있습니다.
현재 탐구 영역은 {area_num} {title} ({title_real}) 입니다.
선택한 작품은 {poem_num}입니다.
탐구 목표는 "{goal}"이고, 탐구 주제는 "{theme}"입니다.
이 주제에 맞는 탐구 질문과 활동 아이디어를 학생 눈높이로 함께 생각해 주세요."""

def build_chat_payload(chat_messages):
    """대화 히스토리를 Gemini API contents 형식으로 변환.
    반드시 user 로 시작하고, user/model 이 교대로 와야 함.
    """
    contents = []
    for msg in chat_messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    # 첫 번째가 model 이면 제거 (API 규칙)
    while contents and contents[0]["role"] != "user":
        contents.pop(0)
    return contents

def call_gemini(chat_messages, api_key):
    if not api_key:
        return False, "API 키가 설정되지 않았어요. Streamlit Secrets를 확인해주세요."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {
            "parts": [{"text": build_system_prompt()}]
        },
        "contents": build_chat_payload(chat_messages),
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxOutputTokens": 1200
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=60)

        try:
            data = response.json()
        except Exception:
            return False, f"응답 해석 실패: HTTP {response.status_code}\n{response.text}"

        if response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "알 수 없는 오류")
            return False, f"Gemini API 오류 ({response.status_code}): {error_msg}"

        candidates = data.get("candidates", [])
        if not candidates:
            return False, "모델이 응답 후보를 반환하지 않았습니다."

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts).strip()

        if not text:
            return False, "응답 텍스트가 비어 있습니다."

        return True, text

    except requests.exceptions.Timeout:
        return False, "요청 시간이 초과되었습니다. 잠시 후 다시 시도하세요."
    except requests.exceptions.RequestException as e:
        return False, f"네트워크 오류: {e}"
    except Exception as e:
        return False, f"예상하지 못한 오류: {e}"

def ask_once(prompt):
    api_key = get_api_key()
    messages = [{"role": "user", "content": prompt}]
    return call_gemini(messages, api_key)

def generate_question_suggestions(season, poem_num, poem_text, theme, qtypes):
    prompt = f"""
다음 정보를 바탕으로 학생용 탐구 질문 4개를 만들어 주세요.

[계절]
{season}

[작품]
{poem_num}

[작품 내용]
{poem_text}

[탐구 주제]
{theme}

[질문 유형]
{", ".join(qtypes)}

조건:
1. 질문 유형마다 1개씩, 총 4개를 제시하세요.
2. 초등 또는 중등 학생이 이해하기 쉬운 문장으로 쓰세요.
3. 각 질문 아래에 '왜 이 질문이 좋은지'를 한 줄 설명하세요.
4. 결과 형식은 번호 목록으로 정리하세요.
"""
    return ask_once(prompt)

def generate_activity_idea(season, poem_num, theme, goal):
    prompt = f"""
다음 정보를 바탕으로 학생이 실제로 할 수 있는 활동 설계안을 작성해 주세요.

[계절] {season}
[작품] {poem_num}
[탐구 주제] {theme}
[탐구 목표] {goal}

조건:
1. 활동 이름
2. 활동 목적
3. 준비물
4. 진행 방법 1~4단계
5. 완성 결과물
6. 누구와 나눌지
7. 발표 또는 공유 방법

위 순서대로 간단하고 또렷하게 작성하세요.
학생 눈높이에 맞는 쉬운 한국어를 사용하세요.
"""
    return ask_once(prompt)

def make_log_text(meta, starter_text, chat, generated_questions, generated_activity):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "H.E.A.L. 탐구 질문 및 활동 설계 기록",
        "=" * 60,
        f"저장 시각: {now}",
        f"영역: {meta['area_num']} {meta['title']} ({meta['title_real']})",
        f"계절: {meta['season']}",
        f"선택 작품: {meta['poem_num']}",
        f"탐구 목표: {meta['goal']}",
        f"탐구 주제: {meta['theme']}",
        "=" * 60,
        "",
        "[시작 문장]",
        starter_text,
        "",
        "[자동 생성 질문]",
    ]

    if generated_questions:
        for q in generated_questions:
            lines.append(q)
    else:
        lines.append("없음")

    lines += ["", "[자동 생성 활동 설계]"]

    if generated_activity:
        lines.append(generated_activity)
    else:
        lines.append("없음")

    lines += ["", "[대화 기록]"]

    if chat:
        for i, msg in enumerate(chat, start=1):
            speaker = "사용자" if msg["role"] == "user" else "AI"
            lines.append(f"{i}. {speaker}: {msg['content']}")
    else:
        lines.append("대화 기록 없음")

    return "\n".join(lines)

# -----------------------------
# 헤더
# -----------------------------
st.title(APP_TITLE)
st.caption("학생이 작품을 읽고, 질문을 만들고, 활동을 설계하도록 돕는 Streamlit 기반 학습 도우미")

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("설정")

    area_num = st.selectbox("영역 번호", ["1", "2", "3", "4", "5"], index=0)
    title = st.text_input("영역 이름", value="자연과 인간")
    title_real = st.text_input("세부 영역", value="생태와 환경")
    season = st.selectbox("계절 선택", ["봄", "여름", "가을", "겨울"], index=2)

    season_poems = POEM_DATA.get(season, [])
    poem_labels = [p["num"] for p in season_poems] if season_poems else ["작품 없음"]
    selected_poem_label = st.selectbox("작품 선택", poem_labels)

    selected_poem = next((p for p in season_poems if p["num"] == selected_poem_label), None)

    goal = st.text_input("탐구 목표", value="작품을 바탕으로 생태 문제를 이해하고 해결 방법을 생각한다")
    theme = st.text_input("탐구 주제", value="우리 지역의 해안 쓰레기 문제")
    student_name = st.text_input("학생 이름(선택)", value="")

    st.divider()
    st.subheader("API 설정")
    manual_api_key = st.text_input("Gemini API Key", type="password", key="manual_api_key")
    st.write("API 상태:", "설정됨" if get_api_key() else "없음")

    st.divider()
    if st.button("대화만 초기화", use_container_width=True):
        reset_chat()
        st.rerun()

    if st.button("전체 내용 초기화", use_container_width=True):
        reset_all()
        st.rerun()

# -----------------------------
# 선택 작품 정보
# -----------------------------
poem_num = selected_poem["num"] if selected_poem else "작품 없음"
poem_original = selected_poem["original"] if selected_poem else ""
poem_modern = selected_poem["modern"] if selected_poem else ""

starter_text = make_starter(area_num, title, title_real, season, goal, theme, poem_num)
st.session_state.starter_text = starter_text

meta = {
    "area_num": area_num,
    "title": title,
    "title_real": title_real,
    "season": season,
    "poem_num": poem_num,
    "goal": goal,
    "theme": theme,
    "student_name": student_name
}

# -----------------------------
# 상단 3단 구성
# -----------------------------
top1, top2, top3 = st.columns([1.05, 1.1, 1.25])

with top1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">선택 작품</div>', unsafe_allow_html=True)
    st.markdown(f"**{poem_num}**")
    st.markdown('<div class="small-label">원문</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="poem-box">{poem_original}</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-label" style="margin-top:10px;">풀이</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="poem-box">{poem_modern}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with top2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">탐구 설계 정보</div>', unsafe_allow_html=True)
    st.write(f"**영역**: {area_num} {title} ({title_real})")
    st.write(f"**계절**: {season}")
    st.write(f"**탐구 목표**: {goal}")
    st.write(f"**탐구 주제**: {theme}")
    if student_name.strip():
        st.write(f"**학생 이름**: {student_name}")
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.write("**질문 유형**")
    for q in QUESTION_TYPES.get(season, []):
        st.write(f"- {q}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"**설계 힌트**: {DESIGN_HINTS.get(season, '')}")
    st.markdown('</div>', unsafe_allow_html=True)

with top3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">시작 문장</div>', unsafe_allow_html=True)
    st.code(starter_text, language="text")
    st.caption("이 문장을 복사해 대화를 시작하거나, 아래 버튼으로 바로 질문과 활동을 생성할 수 있습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 자동 생성 도구
# -----------------------------
st.subheader("자동 생성 도구")
tool1, tool2 = st.columns(2)

with tool1:
    if st.button("탐구 질문 4개 자동 생성", use_container_width=True):
        if not selected_poem:
            st.warning("먼저 작품을 선택하세요.")
        else:
            with st.spinner("탐구 질문을 생성하는 중입니다..."):
                ok, result = generate_question_suggestions(
                    season=season,
                    poem_num=poem_num,
                    poem_text=poem_modern,
                    theme=theme,
                    qtypes=QUESTION_TYPES.get(season, [])
                )
                if ok:
                    chunks = [x.strip() for x in result.split("\n") if x.strip()]
                    st.session_state.generated_questions = chunks
                    st.success("탐구 질문을 생성했습니다.")
                else:
                    st.error(result)

with tool2:
    if st.button("활동 설계안 자동 생성", use_container_width=True):
        if not selected_poem:
            st.warning("먼저 작품을 선택하세요.")
        else:
            with st.spinner("활동 설계안을 생성하는 중입니다..."):
                ok, result = generate_activity_idea(
                    season=season,
                    poem_num=poem_num,
                    theme=theme,
                    goal=goal
                )
                if ok:
                    st.session_state.generated_activity = result
                    st.success("활동 설계안을 생성했습니다.")
                else:
                    st.error(result)

auto1, auto2 = st.columns(2)

with auto1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">자동 생성 질문</div>', unsafe_allow_html=True)
    if st.session_state.generated_questions:
        for item in st.session_state.generated_questions:
            st.write(item)
    else:
        st.markdown('<div class="helper">아직 생성된 질문이 없습니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with auto2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">자동 생성 활동 설계</div>', unsafe_allow_html=True)
    if st.session_state.generated_activity:
        st.write(st.session_state.generated_activity)
    else:
        st.markdown('<div class="helper">아직 생성된 활동 설계안이 없습니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 채팅 영역
# -----------------------------
st.subheader("AI와 대화하기")

if not st.session_state.chat:
    st.info("아래 입력창에 질문을 쓰거나, 시작 문장을 바탕으로 대화를 시작해 보세요.")

for msg in st.session_state.chat:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

user_input = st.chat_input("질문, 생각, 활동 아이디어를 입력하세요")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI가 답변을 작성하는 중입니다..."):
            ok, reply = call_gemini(st.session_state.chat, get_api_key())

            if ok:
                st.markdown(reply)
                st.session_state.chat.append({"role": "assistant", "content": reply})
            else:
                st.error(reply)

# -----------------------------
# 저장 / 다운로드
# -----------------------------
st.subheader("기록 저장")

log_text = make_log_text(
    meta=meta,
    starter_text=st.session_state.starter_text,
    chat=st.session_state.chat,
    generated_questions=st.session_state.generated_questions,
    generated_activity=st.session_state.generated_activity
)

down1, down2 = st.columns([1, 1])

with down1:
    st.download_button(
        label="TXT로 다운로드",
        data=log_text,
        file_name="heal_project_log.txt",
        mime="text/plain",
        use_container_width=True
    )

with down2:
    st.text_area("저장될 기록 미리보기", value=log_text, height=280)

st.caption("배포 시에는 Gemini API 키를 브라우저에 노출하지 말고 Streamlit secrets로 관리하세요.")
