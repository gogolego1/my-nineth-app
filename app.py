import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="H.E.A.L. 탐구 질문 만들기",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 어부사시사 전문 ──────────────────────────────────────
EOBUSA_CHUNSA = [
    {
        "num": "춘사 제1수",
        "원문": "앞 강이 맑다 하되 연잎이 막혔어라\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n어촌에 해 저무니 어주를 돌리어라",
        "풀이": "앞 강물이 맑다고 하지만 연잎이 가득 막혀 있구나.\n배를 띄워라, 배를 띄워라.\n지국총 지국총 어사와 (노 젓는 소리)\n어촌에 해가 저물어 가니 고깃배를 돌려야겠다.",
    },
    {
        "num": "춘사 제2수",
        "원문": "우는 것이 뻐꾸기냐 푸른 것이 버들숲이냐\n이어라 이어라\n지국총 지국총 어사와\n어옹도 물을 잊고 나도 버들 잊을쏘냐",
        "풀이": "저 우는 것이 뻐꾸기냐, 푸른 것이 버드나무 숲이냐.\n노를 저어라, 노를 저어라.\n지국총 지국총 어사와\n노인 어부도 물을 잊고, 나도 버들을 잊겠느냐?",
    },
    {
        "num": "춘사 제3수",
        "원문": "동풍이 건듯 불어 물결을 헤쳐 오니\n돛 달아라 돛 달아라\n지국총 지국총 어사와\n앞 강에 안개 걷히니 경치가 새롭구나",
        "풀이": "동쪽 바람이 살짝 불어 물결을 헤치며 다가오니,\n돛을 달아라, 돛을 달아라.\n지국총 지국총 어사와\n앞 강에 안개가 걷히니 경치가 새롭고 아름답구나.",
    },
    {
        "num": "춘사 제4수",
        "원문": "우두커니 앉아 낚시질을 하노라니\n낚시 들어라 낚시 들어라\n지국총 지국총 어사와\n무심한 백구는 내 뜻을 아는구나",
        "풀이": "가만히 앉아서 낚시를 드리우고 있노라니,\n낚싯줄을 들어라, 들어라.\n지국총 지국총 어사와\n아무 욕심 없는 하얀 갈매기는 내 마음을 아는구나.",
    },
    {
        "num": "춘사 제5수",
        "원문": "청하에 반신을 씻고 녹수에 발을 씻어\n닻 들어라 닻 들어라\n지국총 지국총 어사와\n물외에 가장 청한 것이 어부 생애로다",
        "풀이": "맑은 강에 몸을 씻고 푸른 물에 발을 담그고,\n닻을 들어라, 들어라.\n지국총 지국총 어사와\n세상 밖에 가장 맑고 한가로운 것이 어부의 삶이로다.",
    },
    {
        "num": "춘사 제6수",
        "원문": "낙대를 둘러메고 깊은 탄에 혼자 가니\n배 매어라 배 매어라\n지국총 지국총 어사와\n세상의 티끌 세상이 얼마나 더럽더냐",
        "풀이": "낚싯대를 어깨에 메고 깊은 여울에 혼자 가니,\n배를 매어라, 매어라.\n지국총 지국총 어사와\n세상의 시끄러운 먼지 세계가 얼마나 더럽더냐.",
    },
    {
        "num": "춘사 제7수",
        "원문": "수국의 청광을 어디 두고 보느냐\n돛 내려라 돛 내려라\n지국총 지국총 어사와\n입은 옷 해질수록 나의 뜻이 가을 같아라",
        "풀이": "물 위에 펼쳐진 맑고 밝은 빛을 어디서 보겠느냐,\n돛을 내려라, 내려라.\n지국총 지국총 어사와\n입은 옷이 낡아 해질수록 나의 뜻은 가을 하늘처럼 맑아지는구나.",
    },
    {
        "num": "춘사 제8수",
        "원문": "산두에 한운이 일어나고 수중에 백로 난다\n이어라 이어라\n지국총 지국총 어사와\n무심코 다정한 것은 갈매기뿐이로다",
        "풀이": "산 위에 흰 구름이 피어오르고 물 위에 백로가 날아오르네,\n노를 저어라, 저어라.\n지국총 지국총 어사와\n욕심 없이 다정한 것은 갈매기뿐이구나.",
    },
    {
        "num": "춘사 제9수",
        "원문": "청강에 비 들고 녹수에 안개 끼니\n돛 달아라 돛 달아라\n지국총 지국총 어사와\n낚시줄 드리우고 잠깐 쉬어 바라보니",
        "풀이": "맑은 강에 비가 내리고 푸른 물에 안개가 끼니,\n돛을 달아라, 달아라.\n지국총 지국총 어사와\n낚싯줄을 드리우고 잠깐 쉬며 바라보니.",
    },
    {
        "num": "춘사 제10수",
        "원문": "고운 경이 무궁하여 흥이 절로 나는구나\n배 떼어라 배 떼어라\n지국총 지국총 어사와\n아름다운 이 강산에 뜻을 두고 늙으리라",
        "풀이": "아름다운 경치가 끝이 없어 흥이 저절로 나는구나,\n배를 떼어라, 떼어라.\n지국총 지국총 어사와\n이 아름다운 강산에 마음을 두고 늙어가리라.",
    },
]

# ── 어부사시사 하사 전문 ─────────────────────────────────
EOBUSA_HASA = [
    {
        "num": "하사 제1수",
        "원문": "구름이 무심탄 말이 아마도 허랑하다\n이어라 이어라\n지국총 지국총 어사와\n중봉에 비 오기 전에 물 아래 내려온다",
        "풀이": "구름이 아무 생각 없다는 말이 아마도 거짓말인가 보다.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n산봉우리에 비 내리기 전에 물 아래로 내려온다.",
    },
    {
        "num": "하사 제2수",
        "원문": "산은 옛 산이로되 물은 옛 물이 아니로다\n돛 달아라 돛 달아라\n지국총 지국총 어사와\n주야에 흐르나니 옛 물이 있을소냐",
        "풀이": "산은 예전 그 산이지만 물은 예전 그 물이 아니로다.\n돛을 달아라, 달아라.\n지국총 지국총 어사와\n밤낮으로 흘러가니 예전 물이 어디 있겠느냐.",
    },
    {
        "num": "하사 제3수",
        "원문": "고기 낚기는 낚시질은 잊어 버린 듯하구나\n낚시 들어라 낚시 들어라\n지국총 지국총 어사와\n좋은 일이 많아 무엇을 가릴소냐",
        "풀이": "고기를 낚는 낚시질은 잊어버린 것 같구나.\n낚싯줄을 들어라, 들어라.\n지국총 지국총 어사와\n좋은 일이 너무 많아 무엇을 가려 하겠느냐.",
    },
    {
        "num": "하사 제4수",
        "원문": "삿갓 비 빗기 쓰고 도롱이 옷을 입어\n배 매어라 배 매어라\n지국총 지국총 어사와\n어와 이 몸이 한가하기도 할사로다",
        "풀이": "삿갓을 비스듬히 쓰고 도롱이 옷을 걸치고,\n배를 매어라, 매어라.\n지국총 지국총 어사와\n아, 이 몸이 정말 한가롭기도 하구나.",
    },
    {
        "num": "하사 제5수",
        "원문": "만경 창파에 혼자 앉아 낚시질을 하니\n배 떼어라 배 떼어라\n지국총 지국총 어사와\n내 마음에 맞는 일이 이뿐인가 하노라",
        "풀이": "넓고 넓은 푸른 바다에 혼자 앉아 낚시를 하니,\n배를 떼어라, 떼어라.\n지국총 지국총 어사와\n내 마음에 꼭 맞는 일이 이것뿐인가 싶구나.",
    },
    {
        "num": "하사 제6수",
        "원문": "청하에 홀로 서서 물결을 굽어보니\n닻 들어라 닻 들어라\n지국총 지국총 어사와\n백구야 날지 마라 너를 잡으려 하노라",
        "풀이": "맑은 강가에 홀로 서서 물결을 내려다보니,\n닻을 들어라, 들어라.\n지국총 지국총 어사와\n흰 갈매기야 날아가지 마라, 너를 벗 삼으려 한다.",
    },
    {
        "num": "하사 제7수",
        "원문": "솔 아래 굽은 길이 자연이 그림이로다\n이어라 이어라\n지국총 지국총 어사와\n무릉이 어디오 여기가 그인가 하노라",
        "풀이": "소나무 아래 굽어진 길이 그 자체로 그림 같구나.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n무릉도원이 어디냐, 여기가 바로 그곳인가 하노라.",
    },
    {
        "num": "하사 제8수",
        "원문": "년년이 기약하여 오늘이야 만났으니\n돛 내려라 돛 내려라\n지국총 지국총 어사와\n반갑고 기쁜 뜻을 어디다가 비길소냐",
        "풀이": "해마다 약속하여 오늘에야 만났으니,\n돛을 내려라, 내려라.\n지국총 지국총 어사와\n이 반갑고 기쁜 마음을 어디에 비교할 수 있겠느냐.",
    },
    {
        "num": "하사 제9수",
        "원문": "게를 잡아 구워 먹고 술 먹기를 즐기노라\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n고기국에 밥을 먹어 배부르게 하여라",
        "풀이": "게를 잡아 구워 먹고 술 마시기를 즐기는구나.\n배를 띄워라, 띄워라.\n지국총 지국총 어사와\n생선국에 밥을 먹어 배불리 먹어 보아라.",
    },
    {
        "num": "하사 제10수",
        "원문": "아까운 이 강산을 뉘라서 차지할고\n이어라 이어라\n지국총 지국총 어사와\n우리 것으로 차지하고 늙도록 놀리라",
        "풀이": "아깝고 소중한 이 강산을 누가 차지하겠는가.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n우리 것으로 차지하고 늙도록 즐겁게 놀리라.",
    },
]

# ── 어부사시사 추사 전문 ─────────────────────────────────
EOBUSA_CHUSA = [
    {
        "num": "추사 제1수",
        "원문": "물외에 벋은 길이 뉘 아니 부러워하리\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n어옹의 사생이 이도곤 나을소냐",
        "풀이": "세상 밖으로 뻗은 이 길을 누가 부러워하지 않겠는가.\n배를 띄워라, 띄워라.\n지국총 지국총 어사와\n늙은 어부의 삶이 이보다 더 좋을 수 있겠는가.",
    },
    {
        "num": "추사 제2수",
        "원문": "수국의 청광이 긔 더욱 반갑도다\n이어라 이어라\n지국총 지국총 어사와\n어부의 청흥이 이로다가 다 하리라",
        "풀이": "물 위 나라의 맑고 밝은 빛이 더욱 반갑구나.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n어부의 맑은 흥취가 여기서 다 이루어지리라.",
    },
    {
        "num": "추사 제3수",
        "원문": "낙엽이 지거든 물에 씻어 보내노라\n닻 들어라 닻 들어라\n지국총 지국총 어사와\n어초에 봄빛이 언제나 가는고",
        "풀이": "낙엽이 떨어지거든 물에 씻어 보내노라.\n닻을 들어라, 들어라.\n지국총 지국총 어사와\n낚시터와 초가에 봄빛이 언제나 가는 것인가.",
    },
    {
        "num": "추사 제4수",
        "원문": "어와 저 구름이 어디어디 가고 싶은고\n돛 달아라 돛 달아라\n지국총 지국총 어사와\n날 저물거든 동쪽으로 가려무나",
        "풀이": "아, 저 구름이 어디어디 가고 싶은 것인가.\n돛을 달아라, 달아라.\n지국총 지국총 어사와\n날이 저물거든 동쪽으로 가려무나.",
    },
    {
        "num": "추사 제5수",
        "원문": "옥을 다듬는 듯 맑은 소리는 어디서 나는고\n배 매어라 배 매어라\n지국총 지국총 어사와\n바위 아래 흐르는 물이 졸졸 굴러 오누나",
        "풀이": "옥을 다듬는 듯 맑은 소리는 어디서 나는 것인가.\n배를 매어라, 매어라.\n지국총 지국총 어사와\n바위 아래 흐르는 물이 졸졸 굴러 오는구나.",
    },
    {
        "num": "추사 제6수",
        "원문": "낚싯대 드리우고 가로 베고 누워 있으니\n낚시 들어라 낚시 들어라\n지국총 지국총 어사와\n진세에 번지 아니 하기는 어부뿐이로다",
        "풀이": "낚싯대를 드리우고 팔베개하고 누워 있으니,\n낚싯줄을 들어라, 들어라.\n지국총 지국총 어사와\n세상 먼지에 더럽혀지지 않기는 어부뿐이로다.",
    },
    {
        "num": "추사 제7수",
        "원문": "물결이 가는 곳에 바람이 건듯 부니\n돛 내려라 돛 내려라\n지국총 지국총 어사와\n갈대꽃 깊은 곳에 배를 매어두어라",
        "풀이": "물결이 흘러가는 곳에 바람이 살짝 부니,\n돛을 내려라, 내려라.\n지국총 지국총 어사와\n갈대꽃 무성한 깊은 곳에 배를 매어두어라.",
    },
    {
        "num": "추사 제8수",
        "원문": "물며 멧기러기는 어디서 자고 오느냐\n이어라 이어라\n지국총 지국총 어사와\n서풍이 쌀쌀하니 가을이 다 되었구나",
        "풀이": "물가의 기러기는 어디서 자고 오는 것이냐.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n서풍이 쌀쌀하게 부니 가을이 다 되었구나.",
    },
    {
        "num": "추사 제9수",
        "원문": "고기도 살져 있고 물도 맑고 깨끗하다\n배 떼어라 배 떼어라\n지국총 지국총 어사와\n낚시질 하며 낚은 고기로 배불리 먹어 보자",
        "풀이": "고기도 살이 올라 있고 물도 맑고 깨끗하구나.\n배를 떼어라, 떼어라.\n지국총 지국총 어사와\n낚시질하며 낚은 고기로 배불리 먹어 보자.",
    },
    {
        "num": "추사 제10수",
        "원문": "호호탕탕한 바다에 달이 밝아 오니\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n아름다운 이 경치를 어디다가 비길소냐",
        "풀이": "넓고 넓은 큰 바다에 달이 밝게 떠오르니,\n배를 띄워라, 띄워라.\n지국총 지국총 어사와\n이 아름다운 경치를 어디에 비교할 수 있겠느냐.",
    },
]

# ── 어부사시사 동사 전문 ─────────────────────────────────
EOBUSA_DONGSA = [
    {
        "num": "동사 제1수",
        "원문": "구름 빛이 좋다 하나 검기를 자주 한다\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n바람 소리 맑다 하나 그칠 때가 없도다",
        "풀이": "구름 빛이 좋다고 하지만 자주 검어지는구나.\n배를 띄워라, 띄워라.\n지국총 지국총 어사와\n바람 소리가 맑다고 하지만 그칠 때가 없구나.",
    },
    {
        "num": "동사 제2수",
        "원문": "간밤에 눈 갠 후에 경치가 달랐어라\n이어라 이어라\n지국총 지국총 어사와\n앞에는 옥이요 뒤에는 은이로다",
        "풀이": "간밤에 눈이 그친 뒤에 경치가 완전히 달라졌구나.\n노를 저어라, 저어라.\n지국총 지국총 어사와\n앞에는 옥처럼 빛나고 뒤에는 은처럼 빛나는구나.",
    },
    {
        "num": "동사 제3수",
        "원문": "천지가 가득하여 뉘 눈이 3 4 자\n돛 달아라 돛 달아라\n지국총 지국총 어사와\n산은 높고 구름이 험한 곳에 어이 갈꼬",
        "풀이": "하늘과 땅이 가득 차서 눈이 서너 자나 쌓였구나.\n돛을 달아라, 달아라.\n지국총 지국총 어사와\n산은 높고 구름이 험한 곳에 어찌 가겠느냐.",
    },
    {
        "num": "동사 제4수",
        "원문": "물가에 외로이 서서 낚시를 드리우니\n낚시 들어라 낚시 들어라\n지국총 지국총 어사와\n고기는 아니 무나 내 뜻만 시원하다",
        "풀이": "물가에 혼자 서서 낚싯줄을 드리우니,\n낚싯줄을 들어라, 들어라.\n지국총 지국총 어사와\n고기는 물지 않지만 내 마음만은 시원하고 맑다.",
    },
    {
        "num": "동사 제5수",
        "원문": "유리 갈아 뵈이는 빗발이 다 섰구나\n닻 들어라 닻 들어라\n지국총 지국총 어사와\n강산을 그린 병풍이 엄제나 덮었구나",
        "풀이": "유리처럼 맑게 보이는 빗물이 다 얼어붙었구나.\n닻을 들어라, 들어라.\n지국총 지국총 어사와\n강산을 그린 병풍이 사방을 덮고 있구나.",
    },
    {
        "num": "동사 제6수",
        "원문": "낚시를 걷어 들고 배를 빨리 모니\n배 매어라 배 매어라\n지국총 지국총 어사와\n석양이 내려 비치며 경치가 새롭구나",
        "풀이": "낚시를 거두어 들고 배를 빨리 저어가니,\n배를 매어라, 매어라.\n지국총 지국총 어사와\n석양이 내려 비치며 경치가 다시 새롭구나.",
    },
    {
        "num": "동사 제7수",
        "원문": "삿갓 비 빗기 쓰고 호미 메고 거니니\n돛 내려라 돛 내려라\n지국총 지국총 어사와\n강촌에 들어가니 흥이 나지 아니하랴",
        "풀이": "삿갓을 비스듬히 쓰고 호미를 메고 거니니,\n돛을 내려라, 내려라.\n지국총 지국총 어사와\n강가 마을에 들어가니 흥이 나지 않겠느냐.",
    },
    {
        "num": "동사 제8수",
        "원문": "빈 배에 혼자 앉아 낚싯대를 잡아 가니\n이어라 이어라\n지국총 지국총 어사와\n파랑이 일어 오는 것은 고기 노는 곳이로다",
        "풀이": "빈 배에 혼자 앉아 낚싯대를 잡고 가니,\n노를 저어라, 저어라.\n지국총 지국총 어사와\n물결이 일어나는 곳은 고기가 노는 곳이구나.",
    },
    {
        "num": "동사 제9수",
        "원문": "낚싯대를 흔들어라 고기 잡기가 어렵구나\n배 떼어라 배 떼어라\n지국총 지국총 어사와\n이 강산이 좋거니와 갈 줄을 모르겠다",
        "풀이": "낚싯대를 흔들어보지만 고기 잡기가 어렵구나.\n배를 떼어라, 떼어라.\n지국총 지국총 어사와\n이 강산이 너무 좋아서 어디로 갈 줄을 모르겠구나.",
    },
    {
        "num": "동사 제10수",
        "원문": "낚시터도 좋거니와 배 안에 누워 있어\n배 띄워라 배 띄워라\n지국총 지국총 어사와\n이런 즐거움을 임금도 부럽지 않도다",
        "풀이": "낚시터도 좋지만 배 안에 누워 있으니,\n배를 띄워라, 띄워라.\n지국총 지국총 어사와\n이런 즐거움이 있으니 임금도 부럽지 않구나.",
    },
]

# ── 영역 데이터 ──────────────────────────────────────────
AREAS = {
    "H": {
        "emoji": "🌸",
        "num": "1영역",
        "title": "고운 경이 무궁하여",
        "title_real": "어부사시사 춘사(春詞)",
        "season": "봄(春) · 나에게 묻다",
        "goal": "생태 감수성",
        "stage": "H단계 1차시",
        "theme": "나와 자연의 관계",
        "color": "#2E75B6",
        "bg": "#DEEAF1",
        "poem_data": EOBUSA_CHUNSA,
        "starter": (
            "안녕! 나는 완도에 사는 6학년이야.\n"
            "방금 어부사시사 춘사를 읽었어.\n"
            "'고운 경이 무궁하여 흥이 절로 나는구나'라는 구절이 마음에 남았어.\n"
            "내가 자연과 나의 관계에 대해 스스로 생각하고,\n"
            "이번 프로젝트에서 뭘 탐구하고 만들지 찾을 수 있도록\n"
            "답을 알려주지 말고 나에게 질문만 던져줘.\n"
            "준비됐어? 시작할게."
        ),
        "system": (
            "너는 완도 초등학교 6학년 학생의 프로젝트 설계를 돕는 AI야.\n"
            "학생이 방금 어부사시사 춘사(봄, 10수)를 읽었어.\n\n"
            "【이 대화의 두 가지 목표】\n"
            "① 학생이 자연과 나의 관계를 발견하여 스스로 탐구 질문을 만든다.\n"
            "② 학생이 H→E→A→L 프로젝트 활동 방향을 스스로 설계한다.\n\n"
            "【H·E·A·L 단계 활동 정보 (학생이 모르는 정보 — AI만 알고 있음)】\n"
            "H단계(지금): 어부사시사 읽기, 탐구 질문 생성\n"
            "E단계(탐구): 완도 자연물을 AI 이미지로 시각화 → 색채로 감성 표현 → AI 감정분석 데이터 수집\n"
            "A단계(제작): 완도 자연물을 담은 나만의 시조 창작 → AI로 고쳐쓰기\n"
            "L단계(공유): 시조·감상문을 카드뉴스로 만들어 패들렛 디지털 전시회\n\n"
            "【대화 흐름 — 이 순서대로 질문해줘】\n"
            "1단계(시→나 연결): '춘사 10수에서 흥이 절로 났던 장면이 있어? "
            "너는 완도에서 흥이 절로 난 순간이 언제였어?'\n"
            "2단계(감성 탐색→E단계 씨앗): '그 장면을 색깔로 표현한다면 어떤 색이야? "
            "왜 그 색이 떠올랐어?'\n"
            "3단계(현실 인식→탐구 씨앗): '그런데 지금 그 장소에 가면 윤선도가 느낀 것처럼 "
            "흥이 절로 날 것 같아? 왜 그렇게 생각해?'\n"
            "4단계(창작 방향→A단계 씨앗): '만약 네가 지금 완도 바다를 시조로 쓴다면 "
            "뭘 가장 담고 싶어? 어떤 자연물이나 장소를 표현하고 싶어?'\n"
            "5단계(공유 대상→L단계 씨앗): '그 시조를 완성하면 누구에게 가장 먼저 보여주고 싶어? "
            "왜 그 사람이야?'\n"
            "6단계(활동 설계 정리): '자, 지금까지 대화한 내용을 정리해봐. "
            "이 프로젝트에서 네가 탐구하고 싶은 질문 1개, 만들고 싶은 것 1개, "
            "나눠주고 싶은 사람 1명을 각각 써봐.'\n\n"
            "【말투 지침】\n"
            "- 초등학교 6학년 눈높이에 맞게 쉽고 친근하게 말해줘.\n"
            "- '~야', '~어?', '~해봐' 같은 편한 말투.\n"
            "- 어려운 한자어나 고어는 쉬운 말로 바꿔서 설명해줘.\n"
            "- 한 번에 질문 1개만. 학생 답변 듣고 나서 다음 질문으로 넘어가줘.\n"
            "- 절대 정답을 말하지 마. 학생이 스스로 생각하도록 유도해.\n\n"
            "【생활지도 지침】\n"
            "욕설·비속어·성적 표현·혐오 표현 사용 시:\n"
            "1. 그 표현을 절대 반복하지 마.\n"
            "2. 따뜻하게: '어! 그 말은 다른 친구들이 들으면 기분이 나쁠 수 있어. "
            "고운 말로 다시 써볼까요? 😊'\n"
            "3. 반복 시: '선생님께 이 내용을 보여드릴 수 있어. 바른 말로 대화해줘.'"
        ),
        "steps": [
            ("1", "춘사 1수~10수 읽기", "모르는 단어는 '풀이 보기'를 눌러봐요"),
            ("2", "시작 문장 복사 → 채팅창에 붙여넣기", "그대로 붙여넣고 전송!"),
            ("3", "AI 질문에 내 생각으로 솔직하게 대답하기", "맞고 틀리고 없어요 — 내 생각이 정답이에요"),
            ("4", "탐구 질문·만들 것·나눌 사람 완성하기", "이게 이번 프로젝트의 나만의 설계도예요"),
        ],
        "qtypes": ["감성 질문", "탐구 질문", "창작 질문", "연결 질문"],
        "example": "예) 윤선도가 느낀 완도의 아름다움이 지금도 남아 있을까?",
    },
    "E": {
        "emoji": "☀️",
        "num": "2영역",
        "title": "우리 것으로 차지하고",
        "title_real": "어부사시사 하사(夏詞)",
        "season": "여름(夏) · 함께 듣다",
        "goal": "공동체 의식",
        "stage": "H단계 1차시",
        "theme": "나와 공동체의 관계",
        "color": "#375623",
        "bg": "#E2EFDA",
        "poem_data": EOBUSA_HASA,
        "starter": (
            "안녕! 나는 완도에 사는 6학년이야.\n"
            "방금 어부사시사 하사를 읽었어.\n"
            "'우리 것으로 차지하고 늙도록 놀리라'라는 구절이 인상 깊었어.\n"
            "내가 공동체와 바다의 관계에 대해 스스로 생각하고,\n"
            "이번 프로젝트에서 뭘 탐구하고 만들지 찾을 수 있도록\n"
            "답을 알려주지 말고 나에게 질문만 던져줘.\n"
            "준비됐어? 시작할게."
        ),
        "system": (
            "너는 완도 초등학교 6학년 학생의 프로젝트 설계를 돕는 AI야.\n"
            "학생이 방금 어부사시사 하사(여름, 10수)를 읽었어.\n\n"
            "【이 대화의 두 가지 목표】\n"
            "① 학생이 공동체와 바다의 관계를 발견하여 스스로 탐구 질문을 만든다.\n"
            "② 학생이 H→E→A→L 프로젝트 활동 방향을 스스로 설계한다.\n\n"
            "【H·E·A·L 단계 활동 정보 (AI만 알고 있음)】\n"
            "H단계(지금): 하사 읽기, 탐구 질문 생성\n"
            "E단계(탐구): 완도 어르신 면담 → 세대 간 바다 경험 데이터 수집·그래프 작성 → 미디어 자료 신뢰성 평가\n"
            "A단계(제작): 바다 보존 vs 개발 토론 → 공동체 합의안 작성 → 생태 애니메이션 제작\n"
            "L단계(공유): 캠페인 홍보 동영상 제작 → 공동체 성찰 선언문 발표\n\n"
            "【대화 흐름 — 이 순서대로 질문해줘】\n"
            "1단계(시→공동체 연결): '하사에서 어부들이 다 함께 \"지국총\"을 외치며 노를 젓잖아. "
            "너는 완도에서 어른들이랑 아이들이 함께 뭔가를 하는 장면을 본 적 있어?'\n"
            "2단계(세대 탐색→E단계 씨앗): '그 어른들이랑 너 사이에 바다에 대해서 "
            "생각이 다른 것 같은 게 있어? 어른들은 바다에 대해 뭘 더 알고 있을 것 같아?'\n"
            "3단계(갈등 인식→A단계 씨앗): '완도 바다를 더 잘 지켜야 한다는 사람들이랑, "
            "바다 주변을 개발해서 더 발전시키자는 사람들이 있어. "
            "너는 어떻게 생각해? 왜 그렇게 생각해?'\n"
            "4단계(해결 방법→A단계 씨앗): '그 갈등을 해결하려면 누가, 어떻게 대화해야 할까? "
            "너라면 어떤 방식으로 사람들을 설득하고 싶어?'\n"
            "5단계(공유 방법→L단계 씨앗): '그 생각을 완도 사람들에게 알리고 싶다면 "
            "어떤 방법이 가장 효과적일 것 같아? 영상? 글? 노래? 왜 그걸 선택했어?'\n"
            "6단계(활동 설계 정리): '자, 이제 정리해봐. "
            "이 프로젝트에서 탐구하고 싶은 질문 1개, 만들고 싶은 것 1개, "
            "알리고 싶은 사람 1명을 각각 써봐.'\n\n"
            "【말투 지침】\n"
            "- 초등학교 6학년 눈높이에 맞게 쉽고 친근하게 말해줘.\n"
            "- '~야', '~어?', '~해봐' 같은 편한 말투.\n"
            "- 어려운 한자어나 고어는 쉬운 말로 바꿔서 설명해줘.\n"
            "- 한 번에 질문 1개만. 학생 답변 듣고 나서 다음 질문으로 넘어가줘.\n"
            "- 절대 정답을 말하지 마. 학생이 스스로 생각하도록 유도해.\n\n"
            "【생활지도 지침】\n"
            "욕설·비속어·성적 표현·혐오 표현 사용 시:\n"
            "1. 그 표현을 절대 반복하지 마.\n"
            "2. 따뜻하게: '어! 그 말은 다른 친구들이 들으면 기분이 나쁠 수 있어. "
            "고운 말로 다시 써볼까요? 😊'\n"
            "3. 반복 시: '선생님께 이 내용을 보여드릴 수 있어. 바른 말로 대화해줘.'"
        ),
        "steps": [
            ("1", "하사 1수~10수 읽기", "'지국총' 소리를 함께 내봐도 좋아요"),
            ("2", "시작 문장 복사 → 채팅창에 붙여넣기", "그대로 붙여넣고 전송!"),
            ("3", "AI 질문에 내 생각으로 솔직하게 대답하기", "맞고 틀리고 없어요 — 내 생각이 정답이에요"),
            ("4", "탐구 질문·만들 것·알릴 사람 완성하기", "이게 이번 프로젝트의 나만의 설계도예요"),
        ],
        "qtypes": ["관계 질문", "갈등 질문", "설득 질문", "실천 질문"],
        "example": "예) 어르신들이 지키려는 바다와 내가 즐기는 바다가 어떻게 다를까?",
    },
    "A": {
        "emoji": "🍂",
        "num": "3영역",
        "title": "수국의 청광이 반갑도다",
        "title_real": "어부사시사 추사(秋詞)",
        "season": "가을(秋) · 바다에 묻다",
        "goal": "생태적 실천력",
        "stage": "H단계 1차시",
        "theme": "나와 자연 문제의 관계",
        "color": "#833C00",
        "bg": "#FCE4D6",
        "poem_data": EOBUSA_CHUSA,
        "starter": (
            "안녕! 나는 완도에 사는 6학년이야.\n"
            "방금 어부사시사 추사를 읽었어.\n"
            "'수국의 청광이 더욱 반갑도다'라는 구절이 마음에 남았어.\n"
            "내가 지금 완도 바다의 생태 문제를 스스로 탐구하고,\n"
            "이번 프로젝트에서 뭘 만들고 실천할지 찾을 수 있도록\n"
            "답을 알려주지 말고 나에게 질문만 던져줘.\n"
            "준비됐어? 시작할게."
        ),
        "system": (
            "너는 완도 초등학교 6학년 학생의 프로젝트 설계를 돕는 AI야.\n"
            "학생이 방금 어부사시사 추사(가을, 10수)를 읽었어.\n\n"
            "【이 대화의 두 가지 목표】\n"
            "① 학생이 완도 바다의 생태 문제를 스스로 발견하여 탐구 질문을 만든다.\n"
            "② 학생이 H→E→A→L 프로젝트 활동 방향을 스스로 설계한다.\n\n"
            "【H·E·A·L 단계 활동 정보 (AI만 알고 있음)】\n"
            "H단계(지금): 추사 읽기, 탐구 질문 생성\n"
            "E단계(탐구): 완도 해안 쓰레기 데이터 수집 → 비율·백분율로 오염도 계산 → AI로 오염 밀도 지도 시각화\n"
            "A단계(제작): 해양쓰레기 분류 AI 에코봇 설계(엔트리) → 탄소중립 실천 가이드북 초고 작성\n"
            "L단계(공유): 가이드북을 Canva로 소책자 디자인 → 지역 어촌계 배포 → 생태 실천 선서\n\n"
            "【대화 흐름 — 이 순서대로 질문해줘】\n"
            "1단계(시→현실 연결): '추사에서 가을 바다가 얼마나 맑고 풍요로운지 나왔잖아. "
            "지금 완도 바다에서 그 맑은 빛을 볼 수 있을 것 같아? 왜 그렇게 생각해?'\n"
            "2단계(문제 인식→E단계 씨앗): '완도 바다가 달라졌다면 뭐가 달라진 것 같아? "
            "직접 본 것, 들은 것 중에 하나만 말해봐.'\n"
            "3단계(데이터 연결→E단계 씨앗): '그 문제가 얼마나 심각한지 숫자로 알 수 있을까? "
            "어떤 데이터를 모으면 좋을 것 같아?'\n"
            "4단계(해결 도구→A단계 씨앗): '그 문제를 해결하는 데 AI나 디지털 기술을 "
            "쓸 수 있을까? 어떤 도구나 방법을 만들고 싶어?'\n"
            "5단계(실천 대상→L단계 씨앗): '그 해결 방법을 가장 먼저 알려주고 싶은 사람이 있어? "
            "완도 사람들이 이걸 알면 뭐가 달라질 것 같아?'\n"
            "6단계(활동 설계 정리): '자, 이제 정리해봐. "
            "이 프로젝트에서 해결하고 싶은 생태 문제 1개, 만들고 싶은 것 1개, "
            "나눠주고 싶은 대상 1명을 각각 써봐.'\n\n"
            "【말투 지침】\n"
            "- 초등학교 6학년 눈높이에 맞게 쉽고 친근하게 말해줘.\n"
            "- '~야', '~어?', '~해봐' 같은 편한 말투.\n"
            "- 어려운 한자어나 고어는 쉬운 말로 바꿔서 설명해줘.\n"
            "- 한 번에 질문 1개만. 학생 답변 듣고 나서 다음 질문으로 넘어가줘.\n"
            "- 절대 정답을 말하지 마. 학생이 스스로 생각하도록 유도해.\n\n"
            "【생활지도 지침】\n"
            "욕설·비속어·성적 표현·혐오 표현 사용 시:\n"
            "1. 그 표현을 절대 반복하지 마.\n"
            "2. 따뜻하게: '어! 그 말은 다른 친구들이 들으면 기분이 나쁠 수 있어. "
            "고운 말로 다시 써볼까요? 😊'\n"
            "3. 반복 시: '선생님께 이 내용을 보여드릴 수 있어. 바른 말로 대화해줘.'"
        ),
        "steps": [
            ("1", "추사 1수~10수 읽기", "가을 바다의 맑은 빛을 상상해봐요"),
            ("2", "시작 문장 복사 → 채팅창에 붙여넣기", "그대로 붙여넣고 전송!"),
            ("3", "AI 질문에 내 생각으로 솔직하게 대답하기", "맞고 틀리고 없어요 — 내 생각이 정답이에요"),
            ("4", "생태 문제·만들 것·나눌 대상 완성하기", "이게 이번 프로젝트의 나만의 설계도예요"),
        ],
        "qtypes": ["문제 질문", "데이터 질문", "해결 질문", "실천 질문"],
        "example": "예) 완도 해안 쓰레기를 AI로 자동 분류할 수 있을까?",
    },
    "L": {
        "emoji": "❄️",
        "num": "4영역",
        "title": "천지가 가득하여",
        "title_real": "어부사시사 동사(冬詞)",
        "season": "겨울(冬) · 세계를 품다",
        "goal": "세계시민성",
        "stage": "H단계 1차시",
        "theme": "나와 세계의 관계",
        "color": "#4C3163",
        "bg": "#EAE0F0",
        "poem_data": EOBUSA_DONGSA,
        "starter": (
            "안녕! 나는 완도에 사는 6학년이야.\n"
            "방금 어부사시사 동사를 읽었어.\n"
            "'천지가 가득하여' 온 세상이 눈으로 덮인 것처럼,\n"
            "우리 완도 이야기가 세상 가득 퍼지면 어떨까 생각했어.\n"
            "내가 완도와 세계의 연결에 대해 스스로 생각하고,\n"
            "이번 프로젝트에서 뭘 탐구하고 만들지 찾을 수 있도록\n"
            "답을 알려주지 말고 나에게 질문만 던져줘.\n"
            "준비됐어? 시작할게."
        ),
        "system": (
            "너는 완도 초등학교 6학년 학생의 프로젝트 설계를 돕는 AI야.\n"
            "학생이 방금 어부사시사 동사(겨울, 10수)를 읽었어.\n\n"
            "【이 대화의 두 가지 목표】\n"
            "① 학생이 완도와 세계의 연결 지점을 스스로 발견하여 탐구 질문을 만든다.\n"
            "② 학생이 H→E→A→L 프로젝트 활동 방향을 스스로 설계한다.\n\n"
            "【H·E·A·L 단계 활동 정보 (AI만 알고 있음)】\n"
            "H단계(지금): 동사 읽기, 탐구 질문 생성\n"
            "E단계(탐구): 구글어스로 기후위기 직면 세계 해안도시 탐색 → 완도와 연결점 찾기 → AI 다국어 번역 도구 탐구\n"
            "A단계(제작): 세계 시민에게 보내는 다국어 연대 서한 작성 → 글로벌 캠페인 영상 제작 → 생태자치헌장 의결\n"
            "L단계(공유): 패들렛 글로벌 온라인 전시회 → 세계 학교·환경단체와 공유 → 지구에게 보내는 편지\n\n"
            "【대화 흐름 — 이 순서대로 질문해줘】\n"
            "1단계(시→세계 연결): '동사에서 \"천지가 가득하여\" 눈이 온 세상을 덮었잖아. "
            "완도 바다 이야기가 세상 가득 퍼진다면 누가 들었으면 좋겠어?'\n"
            "2단계(글로벌 연결→E단계 씨앗): '세계 어딘가에 완도랑 비슷한 바다 문제를 겪는 "
            "곳이 있을까? 있다면 어디일 것 같아? 왜 그곳이 떠올랐어?'\n"
            "3단계(연대 방식→E단계 씨앗): '그 나라 학생들이랑 함께 뭔가를 한다면 "
            "어떤 것이 가능할 것 같아? 말이 달라도 함께할 수 있을까?'\n"
            "4단계(표현 방법→A단계 씨앗): '완도 바다 이야기를 세계 사람들에게 전달하려면 "
            "어떤 언어로, 어떤 방식으로 해야 할까? AI를 어떻게 활용할 수 있을까?'\n"
            "5단계(헌장 가치→A단계 씨앗): '우리 학급이 생태시민으로서 세계와 함께 "
            "지킬 수 있는 약속을 만든다면 뭐가 꼭 들어가야 할까?'\n"
            "6단계(활동 설계 정리): '자, 이제 정리해봐. "
            "이 프로젝트에서 세계와 연결하고 싶은 주제 1개, 만들고 싶은 것 1개, "
            "연결하고 싶은 나라나 대상 1개를 각각 써봐.'\n\n"
            "【말투 지침】\n"
            "- 초등학교 6학년 눈높이에 맞게 쉽고 친근하게 말해줘.\n"
            "- '~야', '~어?', '~해봐' 같은 편한 말투.\n"
            "- 어려운 한자어나 고어는 쉬운 말로 바꿔서 설명해줘.\n"
            "- 한 번에 질문 1개만. 학생 답변 듣고 나서 다음 질문으로 넘어가줘.\n"
            "- 절대 정답을 말하지 마. 학생이 스스로 생각하도록 유도해.\n\n"
            "【생활지도 지침】\n"
            "욕설·비속어·성적 표현·혐오 표현 사용 시:\n"
            "1. 그 표현을 절대 반복하지 마.\n"
            "2. 따뜻하게: '어! 그 말은 다른 친구들이 들으면 기분이 나쁠 수 있어. "
            "고운 말로 다시 써볼까요? 😊'\n"
            "3. 반복 시: '선생님께 이 내용을 보여드릴 수 있어. 바른 말로 대화해줘.'"
        ),
        "steps": [
            ("1", "동사 1수~10수 읽기", "겨울 바다의 고요함을 느껴봐요"),
            ("2", "시작 문장 복사 → 채팅창에 붙여넣기", "그대로 붙여넣고 전송!"),
            ("3", "AI 질문에 내 생각으로 솔직하게 대답하기", "맞고 틀리고 없어요 — 내 생각이 정답이에요"),
            ("4", "세계 주제·만들 것·연결할 대상 완성하기", "이게 이번 프로젝트의 나만의 설계도예요"),
        ],
        "qtypes": ["연결 질문", "연대 질문", "표현 질문", "헌장 질문"],
        "example": "예) 완도 어부들의 지혜로 다른 나라 바다 문제를 해결할 수 있을까?",
    },
}

# ── 세션 상태 초기화 ─────────────────────────────────────
def init_state():
    for key in AREAS:
        if f"chat_{key}" not in st.session_state:
            st.session_state[f"chat_{key}"] = []
        if f"questions_{key}" not in st.session_state:
            st.session_state[f"questions_{key}"] = []
        if f"final_q_{key}" not in st.session_state:
            st.session_state[f"final_q_{key}"] = ""
    if "current_area" not in st.session_state:
        st.session_state.current_area = "H"
    if "show_poem_num" not in st.session_state:
        st.session_state.show_poem_num = None

init_state()

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] { background: #1C1A18; }
[data-testid="stSidebar"] * { color: #E8E4DF !important; }

.user-msg { display:flex; justify-content:flex-end; margin:6px 0; }
.user-bubble {
    color:#fff; padding:10px 15px;
    border-radius:18px 4px 18px 18px;
    max-width:78%; font-size:14px; line-height:1.65; word-break:break-word;
}
.ai-msg { display:flex; justify-content:flex-start; margin:6px 0; gap:8px; }
.ai-avatar {
    width:28px; height:28px; border-radius:50%;
    background:#F0EDE8; border:1px solid #E0DDD8;
    display:flex; align-items:center; justify-content:center;
    font-size:13px; flex-shrink:0; margin-top:2px;
}
.ai-bubble {
    background:#F7F5F0; color:#1C1A18;
    padding:10px 15px; border-radius:4px 18px 18px 18px;
    max-width:78%; font-size:14px; line-height:1.65;
    border:1px solid #E0DDD8; word-break:break-word;
}
.guide-bubble {
    background:#FFF8E7; color:#7A5800;
    padding:10px 15px; border-radius:4px 18px 18px 18px;
    max-width:78%; font-size:14px; line-height:1.65;
    border:1px solid #FFD966; word-break:break-word;
}

.poem-card {
    background:#FAFAF7; border-radius:12px;
    padding:16px 18px; margin-bottom:8px;
    border:1px solid #E8E4DD;
}
.poem-num {
    font-size:11px; font-weight:500; color:#9B9591;
    letter-spacing:.06em; margin-bottom:6px;
    text-transform:uppercase;
}
.poem-text {
    font-family:'Nanum Myeongjo', serif;
    font-size:14px; line-height:2.1; color:#1C1A18;
    white-space:pre-line; margin-bottom:10px;
    padding-bottom:10px; border-bottom:1px dashed #E0DDD8;
}
.poem-meaning {
    font-size:12.5px; color:#6B6560; line-height:1.75;
    white-space:pre-line;
}

.step-row { display:flex; gap:10px; align-items:flex-start; padding:7px 0; border-bottom:1px solid #F0EDE8; }
.step-dot {
    width:22px; height:22px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:11px; font-weight:700; color:#fff; flex-shrink:0;
}
.step-text { font-size:13.5px; line-height:1.5; }
.step-tip { font-size:11px; color:#9B9591; font-style:italic; margin-top:2px; }

.area-banner {
    border-radius:14px; padding:20px 24px;
    margin-bottom:16px; color:white;
}
.banner-season { font-size:12px; opacity:.85; margin-bottom:4px; letter-spacing:.06em; }
.banner-title { font-family:'Nanum Myeongjo', serif; font-size:22px; font-weight:700; margin-bottom:2px; }
.banner-subtitle { font-size:13px; opacity:.75; margin-bottom:4px; font-style:italic; }
.banner-sub { font-size:13px; opacity:.8; }
.banner-badge {
    display:inline-block; margin-top:10px;
    background:rgba(255,255,255,.2); color:white;
    font-size:11px; padding:3px 12px; border-radius:20px;
}

.q-item {
    display:flex; align-items:flex-start; gap:8px;
    padding:10px 14px; border-radius:10px;
    border:1px solid #E0DDD8; background:#F7F5F0;
    font-size:13px; margin-bottom:6px;
}
.q-badge { font-size:10px; font-weight:500; padding:2px 8px; border-radius:10px; white-space:nowrap; flex-shrink:0; }
.chat-container { max-height:380px; overflow-y:auto; padding:8px 4px; }
.notice-box {
    background:#FFF3CD; border:1px solid #FFD966;
    border-radius:10px; padding:10px 14px;
    font-size:12.5px; color:#7A5800; margin-bottom:10px;
    line-height:1.6;
}
</style>
""", unsafe_allow_html=True)


# ── 사이드바 ─────────────────────────────────────────────
# API 키: Streamlit Secrets에서 자동으로 읽어옴
api_key = st.secrets.get("GOOGLE_API_KEY", "")

with st.sidebar:
    st.markdown("## 🌿 H.E.A.L.")
    st.markdown("**어부사시사 탐구 질문 만들기**")
    st.markdown("---")

    if api_key:
        st.success("✓ AI 연결됨")
    else:
        st.error("API 키 설정이 필요해요\nStreamlit Secrets를 확인해주세요")

    st.markdown("---")
    st.markdown("**영역 선택**")
    for k, v in AREAS.items():
        label = f"{v['emoji']} {v['num']}\n{v['title']}"
        active = st.session_state.current_area == k
        if st.button(label, key=f"tab_{k}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.current_area = k
            st.session_state.show_poem_num = None
            st.rerun()

    st.markdown("---")
    cur = st.session_state.current_area
    q_count = len(st.session_state[f"questions_{cur}"])
    chat_count = len([m for m in st.session_state[f"chat_{cur}"] if m["role"] == "user"])
    c1, c2 = st.columns(2)
    c1.metric("대화 횟수", chat_count)
    c2.metric("기록한 질문", q_count)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:11px;color:#6B6560;line-height:1.7">'
        '📖 어부사시사(漁父四時詞)<br>'
        '윤선도(尹善道, 1587~1671)<br>'
        '창작: 1651년, 전남 완도 보길도<br>'
        '봄·여름·가을·겨울 각 10수</div>',
        unsafe_allow_html=True,
    )


# ── 메인 ─────────────────────────────────────────────────
cur = st.session_state.current_area
area = AREAS[cur]
color = area["color"]

# 배너
st.markdown(
    f'<div class="area-banner" style="background:linear-gradient(135deg,{color}DD,{color})">'
    f'<div class="banner-season">{area["emoji"]} {area["season"]}</div>'
    f'<div class="banner-title">{area["num"]} {area["title"]}</div>'
    f'<div class="banner-subtitle">{area["title_real"]}</div>'
    f'<div class="banner-sub">{area["stage"]} · 목표: {area["goal"]}</div>'
    f'<span class="banner-badge">탐구 주제: {area["theme"]}</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── 2단 레이아웃 ─────────────────────────────────────────
col_left, col_right = st.columns([1, 1.1], gap="medium")


# ── 왼쪽: 안내 + 시 ─────────────────────────────────────
with col_left:

    # 시 전문 — 4개 영역 모두 표시
    season_emoji = {"H":"🌸","E":"☀️","A":"🍂","L":"❄️"}
    expander_label = f"📖 {area['title_real']} 1수~10수 전문 보기"
    if area["poem_data"]:
        with st.expander(expander_label, expanded=False):
            st.markdown(
                f'<div style="font-size:12px;color:#9B9591;margin-bottom:12px">'
                f'원문과 현대어 풀이를 함께 볼 수 있어요. '
                f'후렴 <b>「지국총 지국총 어사와」</b>는 노 젓는 소리를 흉내 낸 표현이에요.</div>',
                unsafe_allow_html=True,
            )
            for poem in area["poem_data"]:
                st.markdown(
                    f'<div class="poem-card">'
                    f'<div class="poem-num">{season_emoji[cur]} {poem["num"]}</div>'
                    f'<div class="poem-text">{poem["원문"]}</div>'
                    f'<div class="poem-meaning">💬 {poem["풀이"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # 안내사항
    st.markdown(
        '<div class="notice-box">'
        '💡 <b>AI 대화 안내</b><br>'
        'AI는 탐구 질문을 만드는 것을 도와줘요.<br>'
        '바른 말을 사용하고, 솔직하게 내 생각을 써봐요!'
        '</div>',
        unsafe_allow_html=True,
    )

    # 활동 순서
    st.markdown("**활동 순서**")
    steps_html = ""
    for num, text, tip in area["steps"]:
        steps_html += (
            f'<div class="step-row">'
            f'<div class="step-dot" style="background:{color}">{num}</div>'
            f'<div><div class="step-text">{text}</div>'
            f'<div class="step-tip">{tip}</div></div>'
            f'</div>'
        )
    st.markdown(steps_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 시작 문장
    st.markdown("**💬 시작 문장** — 복사해서 채팅창에 붙여넣기")
    st.code(area["starter"], language=None)
    st.caption("위 텍스트를 선택 → 복사(Ctrl+C) → 채팅창에 붙여넣기(Ctrl+V)")


# ── 오른쪽: AI 채팅 ─────────────────────────────────────
with col_right:
    st.markdown("**🤖 AI와 대화하기**")
    st.caption("AI가 질문을 던지면 내 생각을 솔직하게 써봐요. 맞고 틀리고가 없어요!")

    chat_msgs = st.session_state[f"chat_{cur}"]

    # ── st.chat_message 사용 (HTML 충돌 완전 방지) ──
    chat_container = st.container(height=380)
    with chat_container:
        if not chat_msgs:
            st.info("💬 왼쪽 시작 문장을 복사해서 아래 채팅창에 붙여넣어 보세요")
        else:
            for msg in chat_msgs:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                else:
                    is_guide = any(kw in msg["content"] for kw in
                                   ["고운 말", "바른 말", "선생님께", "기분이 나쁠"])
                    with st.chat_message("assistant"):
                        if is_guide:
                            st.warning(msg["content"])
                        else:
                            st.write(msg["content"])

    # 입력창
    user_input = st.chat_input(
        "내 생각을 여기에 써봐요 (Enter = 전송)",
        key=f"chat_input_{cur}",
    )

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("🗑 대화 초기화", key=f"clear_{cur}", use_container_width=True):
            st.session_state[f"chat_{cur}"] = []
            st.rerun()
    with btn_col2:
        guide_count = sum(
            1 for m in chat_msgs
            if m["role"] == "assistant"
            and any(kw in m["content"] for kw in ["고운 말", "바른 말", "선생님께"])
        )
        if guide_count > 0:
            st.warning(f"📢 지도 {guide_count}회", icon=None)

    # API 호출
    if user_input:
        if not api_key:
            st.error("API 키가 설정되지 않았어요. Streamlit Secrets를 확인해주세요.")
        else:
            st.session_state[f"chat_{cur}"].append(
                {"role": "user", "content": user_input}
            )
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=area["system"],
                )
                history = []
                msgs_so_far = st.session_state[f"chat_{cur}"]
                for m in msgs_so_far[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    history.append({"role": role, "parts": [m["content"]]})

                chat_session = model.start_chat(history=history)
                with st.spinner("AI가 생각하는 중..."):
                    response = chat_session.send_message(user_input)
                reply = response.text
                st.session_state[f"chat_{cur}"].append(
                    {"role": "assistant", "content": reply}
                )
            except Exception as e:
                err = str(e)
                st.session_state[f"chat_{cur}"].pop()
                if "API_KEY_INVALID" in err or "API key not valid" in err:
                    st.error("❌ API 키가 올바르지 않아요.")
                elif "QUOTA_EXCEEDED" in err or "quota" in err.lower():
                    st.error("❌ 무료 사용량 한도를 초과했어요. 잠시 후 다시 시도해주세요.")
                elif "SAFETY" in err or "safety" in err.lower():
                    st.error("❌ 안전 필터에 걸렸어요. 다른 내용으로 다시 시도해주세요.")
                elif "not found" in err.lower() or "404" in err:
                    st.error("❌ 모델을 찾을 수 없어요. 잠시 후 다시 시도해주세요.")
                else:
                    st.error(f"❌ 오류: {err}")
                st.stop()
            st.rerun()


# ── 탐구 질문 기록 ───────────────────────────────────────
st.markdown("---")
st.markdown("### 📝 탐구 질문 기록")
st.caption("대화하면서 떠오른 질문을 유형별로 기록해봐요")

q_c1, q_c2, q_c3 = st.columns([3, 1, 0.7])
with q_c1:
    new_q = st.text_input("질문", placeholder="대화 중 떠오른 질문을 적어봐요",
                          label_visibility="collapsed", key=f"q_input_{cur}")
with q_c2:
    q_type = st.selectbox("유형", area["qtypes"],
                          label_visibility="collapsed", key=f"q_type_{cur}")
with q_c3:
    if st.button("➕ 추가", key=f"add_q_{cur}", use_container_width=True):
        if new_q.strip():
            st.session_state[f"questions_{cur}"].append(
                {"type": q_type, "text": new_q.strip()})
            st.rerun()
        else:
            st.warning("질문을 입력해주세요!")

q_list = st.session_state[f"questions_{cur}"]
if q_list:
    for i, q in enumerate(q_list):
        qa, qb = st.columns([11, 1])
        with qa:
            st.markdown(
                f'<div class="q-item">'
                f'<span class="q-badge" style="background:{area["bg"]};color:{color}">{q["type"]}</span>'
                f'<span style="flex:1">{q["text"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with qb:
            if st.button("✕", key=f"del_{cur}_{i}"):
                st.session_state[f"questions_{cur}"].pop(i)
                st.rerun()
else:
    st.caption("아직 기록한 질문이 없어요. AI와 대화하면서 떠오른 질문을 추가해봐요!")


# ── 나의 프로젝트 설계 정리 ────────────────────────────
st.markdown("---")
st.markdown("### ⭐ 나의 프로젝트 설계 정리")
st.caption("AI와의 대화를 마치고 아래 두 가지를 완성해봐요 — 이게 이번 영역의 나만의 설계도예요!")

area_design_hints = {
    "H": "예) 나는 [자연물]을 탐구해서 시조로 쓰고 [독자]에게 보여주고 싶어.",
    "E": "예) 나는 [갈등 주제]를 탐구해서 [방법]으로 [대상]에게 알리고 싶어.",
    "A": "예) 나는 [생태 문제]를 해결하는 [도구]를 만들어 [대상]에게 나눠주고 싶어.",
    "L": "예) 나는 완도의 [주제]를 [방법]으로 만들어 세계 [대상]과 연결하고 싶어.",
}

design_col1, design_col2 = st.columns(2)
with design_col1:
    st.markdown(f"**① 탐구 질문** | {area['example']}")
    final_q = st.text_area(
        "탐구 질문",
        value=st.session_state[f"final_q_{cur}"],
        placeholder=f"이 영역에서 가장 탐구하고 싶은 질문 1개\n{area['example']}",
        height=110,
        label_visibility="collapsed",
        key=f"final_q_input_{cur}",
    )
    st.session_state[f"final_q_{cur}"] = final_q

with design_col2:
    hint = area_design_hints[cur]
    st.markdown(f"**② 활동 설계 한 문장** | {hint}")
    activity_key = f"activity_design_{cur}"
    if activity_key not in st.session_state:
        st.session_state[activity_key] = ""
    activity_design = st.text_area(
        "활동 설계",
        value=st.session_state[activity_key],
        placeholder=hint,
        height=110,
        label_visibility="collapsed",
        key=f"activity_input_{cur}",
    )
    st.session_state[activity_key] = activity_design


# ── 저장 ─────────────────────────────────────────────────
st.markdown("---")

def make_record():
    now = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    q_list  = st.session_state[f"questions_{cur}"]
    f_q     = st.session_state[f"final_q_{cur}"]
    act_key = f"activity_design_{cur}"
    act     = st.session_state.get(act_key, "")
    msgs    = st.session_state[f"chat_{cur}"]
    guide_cnt = sum(1 for m in msgs if m["role"] == "assistant"
                    and any(kw in m["content"] for kw in ["고운 말","바른 말","선생님께"]))

    lines = [
        "H.E.A.L. 프로젝트 탐구 질문 및 활동 설계 기록",
        "=" * 48,
        f"영역: {area['num']} {area['title']} ({area['title_real']})",
        f"계절: {area['season']}",
        f"탐구 목표: {area['goal']} | 탐구 주제: {area['theme']}",
        f"저장 시각: {now}",
        "=" * 48, "",
    ]
    if f_q:
        lines += ["[ ⭐ 탐구 질문 ]", f"  {f_q}", ""]
    if act:
        lines += ["[ 🗺 활동 설계 ]", f"  {act}", ""]
    if q_list:
        lines.append(f"[ 대화 중 기록한 질문 ({len(q_list)}개) ]")
        for i, q in enumerate(q_list, 1):
            lines.append(f"  {i}. [{q['type']}] {q['text']}")
        lines.append("")
    if guide_cnt:
        lines += [f"[ 📢 생활지도 기록 ]",
                  f"  부적절한 표현 사용으로 AI 지도 {guide_cnt}회 발생", ""]
    user_msgs = [m for m in msgs if m["role"] == "user"]
    if msgs:
        lines.append(f"[ AI 대화 기록 ({len(user_msgs)}회) ]")
        for m in msgs:
            speaker = "학생" if m["role"] == "user" else "AI"
            lines.append(f"\n{speaker}: {m['content']}")
    return "\n".join(lines)


s1, s2 = st.columns([3, 1])
with s1:
    today = datetime.now().strftime("%Y%m%d")
    st.download_button(
        label="💾 기록 파일로 저장 (선생님께 제출용)",
        data=make_record().encode("utf-8"),
        file_name=f"HEAL_{area['num'].replace('영역','')}영역_탐구질문_{today}.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary",
    )
with s2:
    if st.button("🗑 전체 초기화", key=f"clear_all_{cur}", use_container_width=True):
        st.session_state[f"chat_{cur}"] = []
        st.session_state[f"questions_{cur}"] = []
        st.session_state[f"final_q_{cur}"] = ""
        st.rerun()
