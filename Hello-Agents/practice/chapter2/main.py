import re
import random

# 定义规则库:模式(正则表达式) -> 响应模板列表
rules = {
    r"I need (.*)": [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?",
    ],
    r"Why don\'t you (.*)\?": [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?",
    ],
    r"Why can\'t I (.*)\?": [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?",
    ],
    r"I am (.*)": [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?",
    ],
    r".* mother .*": [
        "Tell me more about your mother, {name}.",
        "What was your relationship with your mother like,{name}?",
        "How do you feel about your mother?",
    ],
    r".* father .*": [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?",
    ],
    r".* study .*": [
        "What subjects do you like to study?",
        "Do you find studying enjoyable?",
        "What is your favorite thing to learn about?",
    ],
    r".*": [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?",
    ],
}

person_info = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "traveling", "cooking"],
    "profession": "software engineer",
}

# 定义代词转换规则
pronoun_swap = {
    "i": "you",
    "you": "i",
    "me": "you",
    "my": "your",
    "am": "are",
    "are": "am",
    "was": "were",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "yours": "mine",
    "mine": "yours",
}


def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)


def respond(user_input):
    """
    根据规则库生成响应
    """
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # 捕获匹配到的部分
            captured_group = match.group(1) if match.groups() else ""
            # 进行代词转换
            swapped_group = swap_pronouns(captured_group)
            # 从模板中随机选择一个并格式化
            response = random.choice(responses).format(
                swapped_group, name=person_info["name"]
            )
            return response
    # 如果没有匹配任何特定规则，使用最后的通配符规则
    return random.choice(rules[r".*"])


def save_user_info(user_input):
    """
    从用户输入中提取个人信息，并更新全局 person_info 字典。
    支持提取：姓名、年龄、职业、爱好（可追加新爱好）。
    """
    global person_info

    # 1. 提取姓名：my name is X, I'm X, call me X
    name_match = re.search(
        r"(?:my name is|i am|i'm|call me)\s+(\w+)", user_input, re.IGNORECASE
    )
    if name_match:
        person_info["name"] = name_match.group(1).capitalize()

    # 2. 提取年龄：I am X years old, I'm X
    age_match = re.search(
        r"(?:i am|i'm)\s+(\d+)\s*(?:years? old)?", user_input, re.IGNORECASE
    )
    if age_match:
        person_info["age"] = int(age_match.group(1))

    # 3. 提取职业：I am a X, I work as a X
    prof_match = re.search(
        r"(?:i am a|i'm a|i work as a)\s+(.+)", user_input, re.IGNORECASE
    )
    if prof_match:
        # 去除句尾标点符号
        profession = prof_match.group(1).strip().rstrip(",.!")
        person_info["profession"] = profession

    # 4. 提取爱好：I like X, I enjoy X, my hobbies include X
    hobby_match = re.search(
        r"(?:i like|i enjoy|my hobbies? include)\s+(.+)", user_input, re.IGNORECASE
    )
    if hobby_match:
        hobbies_str = hobby_match.group(1).strip().rstrip(",.!")
        # 分割爱好：可能用 "and" 或逗号分隔
        # 例如 "reading and traveling" -> ["reading", "traveling"]
        # 或 "reading, traveling, cooking" -> ["reading", "traveling", "cooking"]
        # 先按 " and " 分割，再按逗号分割
        parts = re.split(r"\s*,\s*|\s+and\s+", hobbies_str)
        new_hobbies = [part.strip().lower() for part in parts if part.strip()]
        # 追加到现有爱好列表中（避免重复，不区分大小写）
        existing_hobbies_lower = [h.lower() for h in person_info["hobbies"]]
        for hobby in new_hobbies:
            if hobby not in existing_hobbies_lower:
                person_info["hobbies"].append(hobby)
                existing_hobbies_lower.append(hobby)  # 更新本地快照，避免二次重复


# 主聊天循环
if __name__ == "__main__":
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        save_user_info(user_input)
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break
        response = respond(user_input)
        print(f"Therapist: {response}")
