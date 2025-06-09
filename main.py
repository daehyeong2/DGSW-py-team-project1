import os
os.system('clear')

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

questions = [
    {
        "content": "체스와 같이 머리 쓰는 게임을 좋아한다.",
        "field": ["백엔드", "보안"]
    },
    {
        "content": "어떤 일을 진행할 때 그 일에 대해서 다양한 관점으로 생각한다.",
        "field": ["보안"]
    },
    {
        "content": "과정보다 결과를 중시한다.",
        "field": ["프론트엔드", "앱"]
    },
    {
        "content": "게임하는 것을 좋아한다.",
        "field": ["게임"]
    },
    {
        "content": "다른 사람에게 많이 사용되는 것을 만들고 싶다.",
        "field": ["앱"]
    },
    {
        "content": "어려운 문제를 해결하기 위해 포기하지 않고 노력했던 적이 있다.",
        "field": ["백엔드"]
    },
    {
        "content": "예술적인 소질이 어느정도 있다고 생각한다.",
        "field": ["프론트엔드", "앱"]
    },
    {
        "content": "직접 만든 것으로 돈을 벌어보고 싶다.",
        "field": ["게임"]
    },
    {
        "content": "논리적이고 체계적으로 무언가를 설계하는 것이 좋다.",
        "field": ["게임"]
    },
    {
        "content": "내가 만든 것을 다른 사람이 즐겨줬으면 좋겠다.",
        "field": ["게임"]
    },
    {
        "content": "만들어진 무언가를 꼼꼼하게 개선시키고 발전시키고 싶다.",
        "field": ["보안"]
    },
    {
        "content": "해커가 멋있다고 생각한다.",
        "field": ["보안"]
    },
    {
        "content": "노력의 결과가 바로 눈에 보이는 것이 좋다.",
        "field": ["프론트엔드", "앱"]
    },
    {
        "content": "프로젝트에서 핵심 임무를 맡는것이 좋다.",
        "field": ["백엔드"]
    },
    {
        "content": "상상한 세계를 직접 제작하는것이 즐겁다.",
        "field": ["프론트엔드", "게임"]
    },
    {
        "content": "디자인과 무언가를 만드는 것을 즐긴다.",
        "field": ["프론트엔드", "앱"]
    },
    {
        "content": "어떤 문제가 발생했을때 그 문제를 해결해 가는 과정이 즐겁다.",
        "field": ["백엔드", "보안"]
    },
    {
        "content": "기획에 따라서 만드는것이 자유롭게 만드는것보다 즐겁다.",
        "field": ["앱", "프론트엔드", "백엔드"]
    },
    {
        "content": "보안과 관련된 문제를 보고 어떻게 하는건지 흥미가 생긴다.",
        "field": ["보안"]
    },
    {
        "content": "기계로만 개발하는것보다 사용자와 소통하면서 제작하는것이 좋다.",
        "field": ["프론트엔드", "앱"]
    },
]

for idx in range(len(questions)):
    question = questions[idx]
    os.system("clear")
    print(f"""
    \033[36m[{idx+1}/{len(questions)}] \033[0m{question["content"]}
    
    \033[31m1: \033[0m전혀 그렇지 않다. \033[31m2: \033[0m그렇지 않다. \033[31m3: \033[0m보통이다. \033[31m4: \033[0m그렇다. \033[31m5: \033[0m매우 그렇다. 
    """)
    score = 0
    while True:
        try:
            score = int(input("번호 선택: ")) - 1
            if score < 0 or score > 4:
                print("올바른 숫자를 입력해 주세요. (1~5)")
            else: break
        except ValueError:
            print("올바른 숫자를 입력해 주세요. (1~5)")
    for field in question["field"]:
        test_result[field] += score

print(test_result)