import json


questions = []

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
    g_question = prev_groupname+g_object['name']

    for first_children in g_object['children']:
        question_type = first_children['type']
        
        if question_type == 'group':
            parse_group(g_question+"/",first_children)
            continue

        question = g_question+"/"+first_children['name']

        questions.append({'question':question, 'label':first_children.get('label', question), 'type':first_children.get('type', '')})



def get_questions(ques_json):
    ques_json = json.loads(ques_json)
    question_dict = {}

    for question in ques_json['children']:
        if question['name'] == 'meta':
            pass
            
        if question['type'] == "group":
            parse_group("", question)
            
        if question['type'] == "repeat":
            pass

        else:
            if 'label' in question.keys():
                questions.append({'question': question['name'], 'label': question.get('label', question), 'type':question.get('type', '')})
    return questions