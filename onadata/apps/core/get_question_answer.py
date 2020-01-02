import json


def get_questions_and_answers(ques_json, ans_json):
    question_answer = []
    quest_ans_dict = {}

    for question in ques_json['children']:
        if question['name'] == 'meta':
            pass

        if question['type'] == 'group':
            pass
        
        if question['type'] == 'repeat':
            pass

        else:
            quest_ans_dict[question['name']] = ans_json[question['name']]
    question_answer.append(quest_ans_dict)


def parse_group(prev_groupname, g_object):
    group_questions = []
    g_question = prev_groupname+g_object['name']

    for first_children in g_object['children']:
        question_type = first_children['type']
        
        if question_type == "group":
            parse_group(g_question+"/",first_children)

        elif question_type == "integer":
            question = g_question+"/"+first_children['name']

            group_questions.append({"question":question, "label":first_children.get("label", question), "type":first_children.get("type", '')})
    return group_questions

def get_questions(ques_json):
    questions = []
    questions_json = json.loads(ques_json)

    for question in questions_json['children']:
        if question['name'] == 'meta':
            pass
            
        elif question["type"] == "group":
            group_questions = parse_group("", question)
            for item in group_questions:
                questions.append(item)
            
        elif question['type'] == "repeat":
            pass

        elif question['type'] == "integer":
            questions.append({"question": question.get("name"), "label": question.get("label", question), "type":question.get("type", '')})
    unique = set()
    for d in questions:
        t = tuple(d.iteritems())
        unique.add(t)
    question_lists = []
    question_lists = [dict(x) for x in unique] 
    return question_lists