with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

set_answered_questions = set()

nb_yes_answer = 0
for line in content:
    if line == "":
        nb_yes_answer += len(set_answered_questions)
        set_answered_questions = set()
        continue
    for char in line:
        set_answered_questions.add(char)

# for the last iteration not appended
nb_yes_answer += len(set_answered_questions)

# 6518 too low
print(nb_yes_answer)
