with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

set_all_yes_questions = None

nb_yes_answer = 0
for line in content:
    if line == "":
        nb_yes_answer += len(set_all_yes_questions)
        set_all_yes_questions = None
        continue
    if set_all_yes_questions is None:
        set_all_yes_questions = set(line)
    else:
        set_all_yes_questions = set_all_yes_questions.intersection(set(line))


# for the last iteration not appended
nb_yes_answer += len(set_all_yes_questions)

print(nb_yes_answer)
