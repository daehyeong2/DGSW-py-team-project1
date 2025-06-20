import os
os.system('clear') # 콘솔 화면 초기화
from wcwidth import wcswidth # 텍스트 너비 계산 (길이 정렬용)
from dotenv import load_dotenv # env 파일 로딩용
import requests # API 요청용
import pyfiglet # 인트로 화면에 글자 표시하는 용
import time # 인트로 화면에 애니메이션을 적용하는 용
from colorama import init, Fore, Style # 인트로 화면에 색깔을 적용하는 용

# .env 파일의 환경 변수 불러옴
load_dotenv()

# 색깔 기본 세팅
init(autoreset=True)

# 색깔 정의
text_color = Fore.CYAN
border_color = Fore.YELLOW
prompt_color = Fore.GREEN

# OpenAI API 사용을 위해 시크릿 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# 분석 목적별 프롬프트 문장
targets = {
    "high_reason": "직무가 적합하게 나온 이유를 분석하세요.",
    "low_reason": "직무에 반대되는 점을 분석해 문제점과 해결 방안을 제시하세요."
}

# AI가 응답하는 예시
examples = [
    """당신은 요소 색깔이나 애니메이션과 같은 화면 반응을 세세하게 조절하는 것을 좋아한다고 답하였던 것을 보아 프론트엔드에 적합할 것입니다.""",
    """당신은 팀 프로젝트보다 개인 프로젝트를 더 좋아한다는 답변을 하였고, 이는 자칫 잘못하면 디자인 팀과 협업하는 것이 힘들수도 있어 개선이 필요합니다. 협업 경험을 쌓으며 팀 프로젝트에 익숙해 지세요. 분석은 적합한 직무에 관련된 것만 진행하세요. (프론트엔드인데 보안을 피드백하지 마라는 것입니다.)"""
]

# 사용자의 답변을 바탕으로 분석 요청 함수
def getAnalysis(questions, field, target):
    prompt = f"""
    당신은 개발 직무 적성 평가 시험 결과를 분석하는 전문가입니다.
    직무 적성 평가는 개발 직무 중 자신이 어떤 직무에 적합할지 검사하는 시험입니다.
    20개 내외의 질문이 존재하고, 각각 질문에 그렇다에 대답했을 때 점수를 주는 영역인 plus_field와
    아니다에 대답했을 때 점수를 주는 영역인 minus_field가 존재합니다.
    또한, 해당 질문에 대한 사용자의 응답이 answer에 기록됩니다.
    예시:
    ---
    [
      {{
        "content": "버튼 색깔이나 움직임 같은 화면 반응을 세세하게 조절하는 걸 좋아한다.",
        "plus_field": ["프론트엔드", "앱"],
        "minus_field": ["백엔드"],
        "answer": "그렇다"
      }}
    ]
    ---
    이 각각의 질문들을 분석해 {field} 개발 {targets[target]}
    응답은 분석 결과만 포함하고, 최대한 짧게 핵심만 추려내고, 빠르게 읽을 수 있도록 하세요.
    최대 300글자 이내로 응답하세요.
    예시:
    ---
    {examples[0] if target=="high_reason" else examples[1]}
    ---
    
    그럼, 사용자의 응답 정보를 제공하겠습니다.
    아래 데이터를 기반으로 분석을 시작해 주세요.
    {questions}
    """
    res = requests.post("https://api.openai.com/v1/responses", json = {
        "model": "gpt-4.1",
        "input": prompt,
    }, headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    })
    # 응답이 정상인지 확인
    if not res.ok:
        return False
    else:
        # 결과 데이터를 추출해 반환
        result = res.json()["output"][0]["content"][0]["text"]
        return result

# 출력 함수 (인수를 바꿔 쉽게 출력 내용 변경 가능, 재사용 가능)
def printSuitableJob(order, high_reason = "", low_reason = ""):
    # 출력 전 콘솔 클리어
    os.system("clear")
    print("\n\033[33m[당신의 전공별 적합도]\033[0m")
    # 전공별 적합도 막대 그래프 출력 (100% 기준으로 20칸 출력, 1칸 당 5%)
    for amount, field in order:
        print(f"{pad(field, 10)} : ", end="")
        for j in range(int(amount // 5)): print("\033[106m ", end="\033[0m")
        for j in range(20 - int(amount // 5)): print("\033[47m ", end="\033[0m")
        print(f" \033[90m({amount:.1f}%)", end="\033[0m\n")

    # 가장 적합한 전공을 출력
    print("\n\033[33m[당신의 가장 적합한 전공]\033[0m", end=' --> ')
    print(*result, sep=', ')

    # 해당 직무가 적합한 이유를 인수로 넘겨받았다면 출력, 그렇지 않다면 api 요청이 처리 중이므로 "로딩 중.." 출력
    print(f"\n\033[33m[{", ".join(result)} 개발 직무가 적합한 이유]\033[0m")
    if high_reason: print(high_reason)
    else: print("로딩 중..")

    # 해당 직무를 잘하기 위해 보완해야하는 점을 인수로 넘겨받았다면 출력, 그렇지 않다면 api 요청이 처리 중이므로 "로딩 중.." 출력
    print(f"\n\033[33m[{", ".join(result)} 개발 직무를 잘하기 위해 보완해야 하는 점]\033[0m")
    if low_reason: print(low_reason)
    else: print("로딩 중..")

# 텍스트 길이(글자 수가 아닌 실제 출력 길이)를 기준으로 가로 크기를 맞추는 맞추는 함수
def pad(text, width, content = " "):
    pad_len = width - wcswidth(text)
    return text + content * pad_len


# FindIT 글자를 큰 배너로 변환
banner = pyfiglet.figlet_format("FindIT")
# 배너를 라인별로 나눠서 리스트로 만듬
lines = banner.split("\n")[:-2]
# 출력할 배너의 가로 크기를 정의
width_size = 50
# 첫번째 줄과 마지막 줄의 테두리 모양을 정의
border = "+" + pad("-", 52, "-") + "+"

# 테두리 출력
print(border_color + border)
for i in range(len(lines)):
    # 애니메이션을 위한 시간 지연
    time.sleep(0.3)
    # i번째 line과 중간 테두리 출력
    print(border_color + "| " + text_color + pad(lines[i], width_size) + border_color + " |")
    if i == len(lines) - 1:
        # 마지막 줄의 경우, 텍스트까지 출력
        time.sleep(0.3)
        print(border_color + "| " + text_color + pad("", width_size) + border_color + " |")
        time.sleep(0.3)
        print(border_color + "| " + text_color + pad("- 당신이 어떤 직무에 적합한지 궁금하신가요?", width_size) + border_color + " |")
        time.sleep(0.3)
        print(border_color + "| " + text_color + pad("- 바로 시험을 시작해 보세요!", width_size) + border_color + " |")
time.sleep(0.3)
print(border_color + border)
time.sleep(0.3)

# 엔터를 눌렀을 때 시작되도록 input을 이용
input("[ENTER]를 눌러 시험을 시작하기\n")

# 각 전공별 적합도 테스트 점수 저장
test_result = {
    "프론트엔드": 0,
    "백엔드": 0,
    "앱": 0,
    "보안": 0,
    "게임": 0
}

# 각 직무 별로 얻을 수 있는 최대 점수를 저장
max_scores = {
    "프론트엔드": 0,
    "백엔드": 0,
    "앱": 0,
    "보안": 0,
    "게임": 0
}

# 질문
questions = [
    {
        "content": "정보를 단순히 나열하기보다, 보는 사람이 이해하기 쉽고 보기 좋게 배치하며 디자인하는 것에 더 신경 쓰는 편이다.", # 질문 내용
        "plus_field": ["프론트엔드", "앱"], # 응답이 그렇다에 가까울 때 점수를 줄 분야
        "minus_field": ["백엔드", "보안"] # 응답이 아니다에 가까울 때 점수를 줄 분야
    },
    {
        "content": "어려운 문제가 풀리지 않아서 며칠동안 풀더라도 결국 문제를 찾아 해결했을 때의 성취감이 매우 크다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": []
    },
    {
        "content": "나만의 독창적인 아이디어나 예술적 감각을 기술과 결합하여 표현하는 것에 흥미가 있다.",
        "plus_field": ["게임", "프론트엔드"],
        "minus_field": ["보안", "백엔드"]
    },
    {
        "content": "정해진 규칙이나 시스템의 허점을 찾아내는 것을 즐긴다.",
        "plus_field": ["보안"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "내가 만든 결과물을 사람들이 사용하는 모습을 직접 보고, 그들의 반응을 보는 것이 즐겁다.",
        "plus_field": ["프론트엔드", "앱", "게임"],
        "minus_field": ["보안"]
    },
    {
        "content": "눈에 보이지 않더라도, 시스템의 효율성과 안정성을 높이는 작업에서 큰 보람을 느낀다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": ["프론트엔드", "앱"]
    },
    {
        "content": "버튼 색깔이나 움직임 같은 화면 반응을 세세하게 조절하는 걸 좋아한다.",
        "plus_field": ["프론트엔드", "앱"],
        "minus_field": ["백엔드"]
    },
    {
        "content": "단순히 프로그램을 만드는 것을 넘어, 재미있는 규칙이나 스토리가 있는 가상의 세계를 구축하고 싶다.",
        "plus_field": ["게임"],
        "minus_field": ["보안", "앱"]
    },
    {
        "content": "정해진 규칙이나 시스템의 허점을 찾아내고, 이를 어떻게 막을 수 있을지 고민하는 과정이 흥미롭다.",
        "plus_field": ["보안"],
        "minus_field": ["프론트엔드", "게임"]
    },
    {
        "content": "많은 정보를 쉽게 정리하고, 빠르게 꺼낼 수 있게 구조를 짜는 게 좋다.",
        "plus_field": ["백엔드"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "휴대폰 알림, 위치, 카메라 같은 기능을 이용해서 사용자에게 편리함을 주는 앱을 만들고 싶다.",
        "plus_field": ["앱"],
        "minus_field": ["보안"]
    },
    {
        "content": "복잡하게 얽힌 문제의 원인을 찾기 위해, 논리적인 단계를 거쳐 차근차근 파고드는 것을 선호한다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "내가 만든 결과물을 사람들이 사용하는 모습을 직접 보고, 어떻게 더 좋게 만들 수 있을지 생각하는 게 재미있다.",
        "plus_field": ["프론트엔드", "앱", "게임"],
        "minus_field": ["보안"]
    },
    {
        "content": "게임 속 캐릭터가 똑똑하게 움직이거나, 물리처럼 움직이는 게 신기하고 재미있다.",
        "plus_field": ["게임"],
        "minus_field": ["앱", "프론트엔드"]
    },
    {
        "content": "새로운 기능을 추가하는 것보다, 외부의 공격으로부터 시스템을 안전하게 보호하는 역할에 더 큰 책임감을 느낀다.",
        "plus_field": ["보안"],
        "minus_field": ["프론트엔드", "게임", "앱"]
    },
    {
        "content": "레고 블록을 조립하듯, 여러 개의 작은 기능(모듈)을 체계적으로 조합하여 거대한 시스템을 만드는 것을 상상하면 즐겁다.",
        "plus_field": ["백엔드" , "게임"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "나만의 독창적인 아이디어나 예술적 감각을 기술과 결합하여 표현하는 것에 흥미가 있다.",
        "plus_field": ["게임", "프론트엔드"],
        "minus_field": ["보안", "백엔드"]
    },
    {
        "content": "컴퓨터끼리 어떻게 연결돼서 통신하는지, 그리고 데이터를 안전하게 전달하는 방법이 궁금하다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": ["프론트엔드", "게임"]
    },
    {
        "content": "PC 웹사이트보다는 스마트폰 앱을 만들 때 더 많은 가능성이 있다고 생각하며, 모바일 환경에 최적화된 서비스를 만들고 싶다.",
        "plus_field": ["앱"],
        "minus_field": ["백엔드"]
    },
    {
        "content": "멀쩡하게 작동하는 서비스가 있다면, 어떻게든 비정상적으로 작동하게 만들거나 뚫을 방법을 찾아보고 싶다는 충동을 느낀다.",
        "plus_field": ["보안"],
        "minus_field": ["프론트엔드", "앱"]
    },
    {
        "content": "사용자 데이터를 보고 문제를 찾아내고 고쳐나가는 과정에 관심이 있다.",
        "plus_field": ["백엔드", "앱"],
        "minus_field": ["게임"]
    },
    {
        "content": "디자이너, 기획자와 긴밀하게 소통하며 사용자의 피드백을 즉각적으로 반영하는 역할을 선호한다.",
        "plus_field": ["프론트엔드", "앱"],
        "minus_field": ["백엔드", "보안"]
    },
    {
        "content": "단기적인 유행을 따르기보다, 몇 년 후에도 안정적으로 운영될 수 있는 견고하고 확장 가능한 구조를 설계하는 것을 중요하게 생각한다.",
        "plus_field": ["백엔드", "게임"],
        "minus_field": ["프론트엔드"]
    }
]

# 최대 점수 2 또는 -2 이므로 해당 전공에 2점씩 누적 (나중에 퍼센트 계산에 활용)
for question in questions:
    for field in question["plus_field"]:
        max_scores[field] += 2
    for field in question["minus_field"]:
        max_scores[field] += 2

# 응답 필드
answers = ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"]

# 문항 번호 및 질문 출력
for idx in range(len(questions)):
    question = questions[idx]
    os.system("clear")
    print(f"""
    \033[36m[{idx+1}/{len(questions)}] \033[0m{question["content"]} 
    
    \033[33m1: \033[0m전혀 그렇지 않다. \033[33m2: \033[0m그렇지 않다. \033[33m3: \033[0m보통이다. \033[33m4: \033[0m그렇다. \033[33m5: \033[0m매우 그렇다. 
    """) 

    # 사용자가 옳은 입력을 할때까지 입력 받기
    score = 0
    while True:
        try:
            score = int(input("번호 선택: "))
            if score < 1 or score > 5:
                print("올바른 숫자를 입력해 주세요. (1~5)")
            else: break
        except ValueError:
            print("올바른 숫자를 입력해 주세요. (1~5)")
    
    questions[idx]["answer"] = answers[score-1]

    score -= 3 # 3을 중립값으로 지정 // 1 → -2  / 2 → -1  /  3 → 0 (중립)  / 4 → +1  /  5 → +2

    # 점수가 양수면 plus_field에 있는 분야에 각각 점수 더함
    if score > 0:
        for field in question["plus_field"]:
            test_result[field] += score
    # 점수가 음수면 minus_field에 있는 분야에 점수 절댓값(양수)으로 바꾸고 더함
    elif score < 0:
        for field in question["minus_field"]:
            test_result[field] += abs(score)

os.system("clear")

# 전공 적합도 출력
print(f"\n\033[33m[당신의 전공 적합도]\033[0m")
mx = 0 # 가장 높은 적합도 저장 변수
result = [] # 최고 적합 전공 저장
order = [] # 정렬용 리스트
for field in test_result:
    max_score = max_scores[field]
    if max_score == 0:
        amount = 0
    else:
        amount = test_result[field] / max_score * 100 # 각 분야 전공 적합도 퍼센트 계산

# 가장 높은 적합도 리스트에 저장
    if amount == mx:
        result.append(field)
    elif amount > mx:
        mx = amount
        result = [field]
    order.append((amount, field))

# 적합도가 높은 순으로 출력하기 위해 정렬 (내림차순)
order.sort(reverse=True)
printSuitableJob(order)

# AI로 해당 개발 직무가 적합한 이유 출력
try:
    high_reason = getAnalysis(questions, ", ".join(result), "high_reason")
    if type(high_reason) == bool: raise Exception
    printSuitableJob(order, high_reason)

    low_reason = getAnalysis(questions, ", ".join(result), "low_reason")
    if type(low_reason) == bool: raise Exception
    printSuitableJob(order, high_reason, low_reason)
except:
    print("AI 생성 중 에러가 발생했습니다.")