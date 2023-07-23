import re
import time
from agents import house, moderator, house_specs, moderator_specs

# change the question and number of rounds
question = "Should AI be regulated?"
number_of_rounds = 2

# a quick function to get the name of file
def get_name_from_question(question):
    name = question.lower().replace(' ','-')
    name = re.sub(r'\W+', '', name)
    unix_time = int(time.time())
    last_four_digits = str(unix_time)[-4:]
    return name + "-" + last_four_digits

# storing the ongoing conversation
conversation = f"# {question}\n"
def add_to_conversation(who, response):
    global conversation
    conversation += f"## {who}\n{str(response)}\n\n"

print("\033[93mHouse starts!\033[0m\n")
print(f"\033[93m{question}\033[0m\n")

# start writing into the conversation file
name = get_name_from_question(question)
file = open(f"conversation-{name}.md", "a")
file.write(f"# {question}\n\n")

# introducing the participants
response = moderator.run(f"Introduce the participants of the debate: \
                {', '.join(str(spec.persona) for spec in house_specs)}")
file.write(response)

# going through the rounds with the participants
for _ in range(number_of_rounds):
    for i in range(len(house)):
        agent, spec = house[i], house_specs[i]
        so_far = moderator.run(f"Summarise the following conversation in \
            less than 200 words for the next participant, assuming the next \
            participant is {spec.persona}: {conversation}")
        file.write(f"\n\n## Moderator ({moderator_specs.provider} - {moderator_specs.model_name})\n")
        file.write(so_far)
        response = agent.run(so_far)
        file.write(f"\n\n## {spec.persona} ({spec.provider} - {spec.model_name})\n")
        file.write(response)
        print(f"\033[93m[{spec.persona}]\033[0m " + response + "\n\n")
        add_to_conversation(spec.persona, response)    

# wrapping up
wrapup = moderator.run("Wrap up the debate, thank the participants and provide a summary conclusion.")
file.write(f"\n\n## Moderator ({moderator_specs.provider} - {moderator_specs.model_name})\n")
file.write(wrapup)

# Also write a summary to the summary file
summary = moderator.run(f"Summarise the following output from a debate: {conversation}")
summary = f"# {question}\n\n" + summary
with open(f"summary-{name}.md", "w") as file:
    file.write(summary)