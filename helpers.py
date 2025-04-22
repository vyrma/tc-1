def openAI_set_text_for_json(name, schema):
    return {
        "format": {
            "type": "json_schema",
            "name": name,
            "schema": schema,
            "strict": True
        }
    }


def get_question_list_instruction(position):
    return f"""
        A person is applying for {position} position, you are an employer
        you are an expert in this position
        Please ask questions regarding this topic.
    """


def get_answer_evaluation_list_instruction():
    return """
        Evaluate all answers provide how good was the answer as evaluation from 0.00(0%) to 1.00(100%)
        also provide give a semi detailed evaluation_description.
        Provide Topic What was the question about. This data will be used to produce a chart.
        Take a role of and interviewer, and explain like he is a person applying to your company.
    """


def format_question(index, question):
    return str(index) + ". " + question
