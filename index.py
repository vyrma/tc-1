from dotenv import load_dotenv
from OpenAIClient import OpenAIClient
from QuestionList import QuestionList
from AnswerEvaluationList import AnswerEvaluationList
from piechart import pie_chart
from helpers import *
import os
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

instructions = """
Be very polite, if you feel the prompt is offensive answer with:
Please rephrase your answer.
""" #safeguard

question_list_schema = QuestionList.model_json_schema()
question_list_schema_name = "question_list"
max_answer_chars = 500

answer_evaluation_schema = AnswerEvaluationList.model_json_schema()
answer_evaluation_schema_name = "answer_evaluation_list"

st.set_page_config(layout="wide")

cols = col1, col2, col3 = st.columns(3)

with col2:
    st.title("Interview App")

if "started" not in st.session_state:
    st.session_state["started"] = False
    st.session_state["answer_error_message"] = ""

if "client" not in st.session_state:
    st.session_state["client"] = OpenAIClient(api_key, instructions)
    st.session_state["finished"] = False
    st.session_state["dynamic_mode"] = False
    # st.session_state["stream_questions"] = False
    st.session_state["answers_evaluated"] = False
    st.session_state["instructions"] = None
    st.session_state["current_question"] = 0
    st.session_state["user_answer"] = ""
    st.session_state["history"] = []


def start_interview():
    st.session_state["client"].model = model
    st.session_state["client"].temperature = temperature
    st.session_state["client"].top_p = top_p
    st.session_state["instructions"] = instructions
    st.session_state["started"] = True
    st.session_state["finished"] = False
    st.session_state["questioning_initiated"] = False
    st.session_state["question_count"] = question_count
    generate_questions_prompt = f"""Generate {question_count} random Questions.""" # zero-shot prompt
    
    # generate_questions_prompt = f"""Generate {question_count} random Questions.
    # For example:
    # What's the difference of cookie parameters and session parameters?
    # Can you name and explain couple of sorting algorithms?
    # Can you explain polymorphism in programming?
    # """ # few-shot prompt technical questions for web developer position.
    
    # generate_questions_prompt = f"""Generate {question_count} random Questions.
    # Use these topics:
    # JavaScript
    # HTML
    # CSS
    # Responsive design
    # """ # Generated knowledge prompt for web developer position
    
    st.session_state["question_list"] = generate_question_list(
        question_list_schema_name, question_list_schema, position, generate_questions_prompt)


def generate_question_list(schema_name, schema, position, prompt):
    response = st.session_state["client"].generate_response(
        prompt,
        openAI_set_text_for_json(schema_name, schema),
        get_question_list_instruction(position))
    return QuestionList.model_validate_json(response.output_text)


def generate_answer_evaluation_list(schema_name, schema, prompt):
    response = st.session_state["client"].generate_response(
        prompt,
        openAI_set_text_for_json(schema_name, schema),
        get_answer_evaluation_list_instruction())
    return AnswerEvaluationList.model_validate_json(response.output_text)


def answer_callback():
    user_answer = st.session_state.get("user_answer", "").strip()
    current_question_index = st.session_state["current_question"]
    
    if user_answer:
        if len(user_answer) > max_answer_chars: 
            st.session_state["answer_error_message"] = "Answer is Too long!"
            return
        
        st.session_state["history"] += [{"role": "assistant", "content": st.session_state["question_list"].question[current_question_index]}]
        st.session_state["history"] += [{"role": "user", "content": user_answer}]
        st.session_state["current_question"] += 1
        st.session_state["user_answer"] = ""
        st.session_state["answer_error_message"] = ""
    else:
        st.session_state["answer_error_message"] = "Please add your answer"


def display_chart_list(answer_evaluations):
    if not st.session_state["answers_evaluated"]:
        return

    for i in range(0, len(answer_evaluations.answer_evaluation), 3):
        chart_cols= st.columns(3)
        for j, col in enumerate(chart_cols):
            if i + j < len(answer_evaluations.answer_evaluation):
                with col:
                    key = i + j
                    topic = answer_evaluations.answer_evaluation[key].topic
                    evaluation = answer_evaluations.answer_evaluation[key].evaluation
                    description = answer_evaluations.answer_evaluation[key].evaluation_description
                    pie_chart(key, topic, evaluation, description)
                    st.write(description)


with col2:
    if not st.session_state["started"]:
        with st.expander("OpenAI settings"):
            model = st.selectbox(
                "Model", ["gpt-4.1-mini", 
                          "gpt-4o", 
                          "gpt-4o-mini",
                        #   "gpt-3.5-turbo", # doesn't support json schema
                        #   "gpt-4", # doesn't support json schema
                          ])
            temperature = st.slider("Temperature", 0.0, 2.0, 0.8)
            top_p = st.slider("Top_p", 0.0, 1.0, 1.0)
            # stream_questions = st.checkbox("Stream")

        position = st.selectbox("Position you apply for", [
                                "Web Developer", "AI Engineer", "Data Scientist", "Cybersecurity Analyst", "Cloud Architect", "DevOps Engineer", "UI/UX Designer"])
        question_count = st.slider("Question Count", 1, 10, 3)
        st.button("Start Your Interview", on_click=start_interview)

    else:
        if st.session_state["question_count"] > st.session_state["current_question"]:
            current_question_index = st.session_state["current_question"]
            current_question = st.session_state["question_list"].question[current_question_index]
            st.write(format_question(
                current_question_index + 1, current_question))
            
            text_area_answer_key = f"user_answer_{current_question_index}"
            
            if text_area_answer_key not in st.session_state:
                st.session_state[text_area_answer_key] = st.session_state.get("user_answer", "")
            
            answer = st.text_area(
                "Your Answer", 
                value=st.session_state["user_answer"],
                max_chars=max_answer_chars,
                height=150, 
                key=text_area_answer_key)
            
            if st.session_state["answer_error_message"]:
                st.error(st.session_state["answer_error_message"])
            
            if st.button("Answer"):
                st.session_state["user_answer"] = st.session_state[text_area_answer_key]
                answer_callback()
                st.rerun()
        else:
            st.session_state["finished"] = True

if st.session_state["finished"]:
    st.write("Finished!")
    
    # evaluation_prompt = "Now generate answers evaluation based on the conversation." # zero-shot prompt
    evaluation_prompt = """Now generate answers evaluation based on the conversation.
    Step 1: explain why you chose  this rating.
    Step 2: explain what information could the user have given to get a greater mark(if mark is not maximum)
    Step 3: provide acknowledgement.
    """ # Chain-Of-Thought prompt
    
    st.session_state["history"] += [{"role": "developer", "content": evaluation_prompt}]
    
    answer_evaluations = generate_answer_evaluation_list(
        answer_evaluation_schema_name, answer_evaluation_schema, st.session_state["history"])
    st.session_state["answers_evaluated"] = True
    display_chart_list(answer_evaluations)
