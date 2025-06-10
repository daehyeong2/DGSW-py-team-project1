import os
os.system('clear')
from wcwidth import wcswidth

def pad(text, width):
    pad_len = width - wcswidth(text)
    return text + ' ' * pad_len

print("""
-----------------------------
- FindIT
- 당신의 전공을 찾아드립니다.
-----------------------------
""")
input("[ENTER]를 눌러 시험을 시작하세요!\n")

test_result = {
    "프론트엔드": 0,
    "백엔드": 0,
    "앱": 0,
    "보안": 0,
    "게임": 0
}

max_scores = {
    "프론트엔드": 0,
    "백엔드": 0,
    "앱": 0,
    "보안": 0,
    "게임": 0
}

questions = [
    {
        "content": "눈에 보이지 않더라도, 시스템의 효율성과 안정성을 높이는 작업에서 큰 보람을 느낀다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": ["프론트엔드", "앱"]
    },
    {
        "content": "사용자가 어떤 버튼을 눌렀을 때, 그 버튼의 색상이나 움직임 같은 시각적 피드백을 세밀하게 조정하는 것을 즐긴다.",
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
        "content": "대용량의 데이터를 효율적으로 정리하고, 필요할 때 빠르게 꺼내 쓸 수 있는 구조를 설계하는 것에 관심이 많다.",
        "plus_field": ["백엔드"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "스마트폰의 알림, 위치 정보, 카메라 같은 하드웨어 기능을 활용하여 사용자에게 편리함을 제공하는 아이디어를 내는 것을 좋아한다.",
        "plus_field": ["앱"],
        "minus_field": ["보안"]
    },
    {
        "content": "복잡하게 얽힌 문제의 원인을 찾기 위해, 논리적인 단계를 거쳐 차근차근 파고드는 것을 선호한다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "내가 만든 결과물을 사람들이 사용하는 모습을 직접 보고, 그들의 반응을 통해 개선점을 찾는 것이 즐겁다.",
        "plus_field": ["프론트엔드", "앱", "게임"],
        "minus_field": ["보안"]
    },
    {
        "content": "게임 속 캐릭터가 더 똑똑하게 움직이거나, 물리 법칙이 현실적으로 작동하도록 만드는 기술에 매력을 느낀다.",
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
        "plus_field": ["백엔드"],
        "minus_field": ["프론트엔드"]
    },
    {
        "content": "정보를 단순히 나열하기보다, 사용자가 이해하기 쉽고 보기 좋게 배치(레이아웃)하고 디자인하는 데 더 신경 쓰는 편이다.",
        "plus_field": ["프론트엔드", "앱"],
        "minus_field": ["백엔드", "보안"]
    },
    {
        "content": "하나의 버그를 잡기 위해 며칠 밤을 새우더라도, 결국 원인을 찾아 해결했을 때의 성취감이 매우 크다.",
        "plus_field": ["백엔드", "보안"],
        "minus_field": []
    },
    {
        "content": "나만의 독창적인 아이디어나 예술적 감각을 기술과 결합하여 표현하는 것에 흥미가 있다.",
        "plus_field": ["게임", "프론트엔드"],
        "minus_field": ["보안", "백엔드"]
    },
    {
        "content": "컴퓨터와 컴퓨터가 어떻게 서로 통신하는지, 그 과정에서 어떻게 데이터를 안전하게 주고받는지 원리가 궁금하다.",
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
        "content": "사용자 로그 데이터를 분석하여 서비스의 문제점을 찾아내고 개선 방향을 정하는 작업에 관심이 있다.",
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

for question in questions:
    for field in question["plus_field"]:
        max_scores[field] += 2
    for field in question["minus_field"]:
        max_scores[field] += 2

for idx in range(len(questions)):
    question = questions[idx]
    os.system("clear")
    print(f"""
    \033[36m[{idx+1}/{len(questions)}] \033[0m{question["content"]}
    
    \033[33m1: \033[0m전혀 그렇지 않다. \033[33m2: \033[0m그렇지 않다. \033[33m3: \033[0m보통이다. \033[33m4: \033[0m그렇다. \033[33m5: \033[0m매우 그렇다. 
    """)
    score = 0
    while True:
        try:
            score = int(input("번호 선택: "))
            if score < 1 or score > 5:
                print("올바른 숫자를 입력해 주세요. (1~5)")
            else: break
        except ValueError:
            print("올바른 숫자를 입력해 주세요. (1~5)")
    score -= 3
    if score > 0:
        for field in question["plus_field"]:
            test_result[field] += score
    elif score < 0:
        for field in question["minus_field"]:
            test_result[field] += abs(score)

os.system("clear")

print(f"\n\033[33m[당신의 전공 적합도]\033[0m")
mx = 0
result = []
order = []
for field in test_result:
    max_score = max_scores[field]
    if max_score == 0:
        amount = 0
    else:
        amount = test_result[field] / max_score * 100
    if amount == mx:
        result.append(field)
    elif amount > mx:
        mx = amount
        result = [field]
    order.append((amount, field))
order.sort(reverse=True)
for amount, field in order:
    print(f"{pad(field, 10)} : ", end="")
    for j in range(int(amount//5)): print("\033[106m ", end="\033[0m")
    for j in range(20-int(amount//5)): print("\033[47m ", end="\033[0m")
    print(f" \033[90m({amount:.1f}%)", end="\033[0m\n")

print("\n\033[33m[당신의 가장 적합한 전공]\033[0m",end=' --> ')
print(*result, sep=', ')