import streamlit as st # streamlit is a python library that allows us to create interactive web applications easily. 
from backend.retrieval import retrieve_chunks #importing the fxn to retrieve the relevant chunks froom VectorDB
from backend.llm import generate_response #importing the fxn to generate response using Gemini free model
from backend.quiz_generator import generate_quiz#importing the fxn to generate quiz from the context retrieved from VectorDB
import time
st.set_page_config(page_title="AI Chat", layout="wide")
st.title(" AI Tutor Chat")
if "chat_history" not in st.session_state:#it creates memory when the chat starts and it will be used to store the conversation history between the user and the AI.
    st.session_state.chat_history = [] # It will create empty memory chat_history[]--
if "quiz_questions" not in st.session_state: #it creates memory for quiz question when the chat starts and it will be used to store the generated quiz questions.
    st.session_state.quiz_questions = [] # It will create empty memory quiz_question[]--
if "current_answer" not in st.session_state: #it creates memory for answer when the chat starts and it will be used to store the generated answer for the user's question.
    st.session_state.current_answer = ""
if "last_question" not in st.session_state: #it creates memory for last question when the chat starts and it will be used to store the last question asked by the user which will be helpful in quiz generation because when user click on generate quiz button then we can use that last question to generate quiz questions based on that question and the context retrieved from VectorDB.
    st.session_state.last_question = ""
if "quiz_state" not in st.session_state:#it creates memory for quiz state when the chat starts and it will be used to store the current question index and score of the quiz.
    st.session_state.quiz_state = { # It will create a dictionary quiz_state with two keys: current_question and score. current_question will keep track of the index of the current quiz question being asked, and score will keep track of the user's score in the quiz.
        "current_question": 0,
        "score": 0,
        "answered": False
    }
    # '''
    # we have created 4 memories here:
    # 1. chat history: to store conversation history between user and AI
    # 2. quiz question: to store the generated quiz questions(5MCQs)
    # 3. quiz state: to store the current question index and score of the quiz
    # 4. One more memory is there for storing the answer which avoids regular re-generation of answer when user click on submit button for quiz question because when user click on submit button then also it triggers the code to generate answer and it will be time consuming process so to avoid that we are storing the generated answer in current_answer memory and when user click on submit button then instead of generating answer again we will get the answer from current_answer memory and display it to user which will save a lot of time and make the app more faster.
    # '''
    
user_question = st.text_input("Ask your question")


if user_question:
    results = retrieve_chunks(user_question)# Retrieve relevant chunks from the VectorDB based on the user's question
    retrieved_docs = results["documents"][0]

    context = "\n".join(retrieved_docs) # Combine retrieved chunks into a single context string
    chat_history = st.session_state.chat_history# get previous conversation from history memory---
    #answer = generate_response(context, user_question) # Generate answer using the context and user question // it was before adding memory in the next line we will add chathistory aswell
    
    if user_question != st.session_state.last_question: # Check if the current user question is different from the last question stored in memory. This condition is used to determine whether we need to generate a new answer or not. If the user asks the same question again, we can simply retrieve the answer from memory instead of generating it again, which will save time and computational resources.
        answer = generate_response(
            context,
            user_question,
            chat_history
        )
        st.session_state.current_answer = answer# Store the generated answer in current_answer memory so that we can use it later when user click on submit button for quiz question without generating the answer again.
        st.session_state.chat_history.append(
            {
                "user": user_question,
                "assistant": answer
            }
        )
        st.session_state.last_question = user_question# Update the last_question memory with the current user question so that we can compare it with the next user question in the future to decide whether to generate a new answer or not.

    st.subheader("AI Answer")
    placeholder = st.empty()
    streamed_text = ""
    for word in st.session_state.current_answer.split():
        streamed_text += word + " "
        placeholder.markdown(streamed_text)
        time.sleep(0.03)
    
    
    
    # answer=generate_response(context, user_question, chat_history)
    # st.subheader("AI Answer") 
    # placeholder = st.empty()
    # streamed_text = ""
    # for word in answer.split():
    #     streamed_text += word + " "
    #     placeholder.markdown(streamed_text)
    #     time.sleep(0.03)
    # Button to generate quiz from retrieved context
    if st.button("Generate Quiz"):# When the user clicks the "Generate Quiz" button, it will trigger the generation of quiz questions based on the retrieved context.
    # Generate 5 MCQs using retrieved context
        quiz_data = generate_quiz(context)# Generate quiz questions based on the retrieved context using the generate_quiz function imported from quiz_generator.py. The generated quiz data will be stored in the quiz_data variable.
        # Store generated quiz in memory
        st.session_state.quiz_questions = quiz_data#store the generated quiz ques in quiz_questions memory which we created at the beginning of the code
        st.session_state.quiz_state["current_question"] = 0
        st.session_state.quiz_state["score"] = 0
        st.session_state.quiz_state["answered"] = False
if st.session_state.quiz_questions: # If there are quiz questions stored in memory, it will display the current quiz question and options to the user.
    current_index = st.session_state.quiz_state["current_question"]#que index is stored in quiz_state memory and we are accessing it here to get the current question index
    st.write("Current Index:", current_index)
    if current_index >= len(st.session_state.quiz_questions): #when index number is greater than or equal to the number of mcqsthen it it'll show quiz is completed
        st.success("🎉Quiz Completed🎉")
        st.write(# after completing the quiz it will show the final score of the user based on the number of correct answers they got in the quiz. The score is calculated by comparing the user's answers with the correct answers
        f"Final Score: {st.session_state.quiz_state['score']} / {len(st.session_state.quiz_questions)}"
        )
        st.stop()
    current_question = st.session_state.quiz_questions[current_index]# acc to index number get quiz ques from quiz_questions memory
    st.subheader(
        f"Question {current_index + 1} of {len(st.session_state.quiz_questions)}" #display the current que number and total number of ques in the quiz
    )
    st.write(current_question["question"])#display the current quiz question
    selected_option = st.radio(#displaying the option for the current question and radio button to select the option
        "Choose your answer",
        [
            #"Select an option",
            f"A. {current_question['optionA']}",
            f"B. {current_question['optionB']}",
            f"C. {current_question['optionC']}",
            f"D. {current_question['optionD']}"
        ],
        # key=f"question_{current_index}"
        index=None 
    )
    #for submit button
    if st.button("Submit Answer"):
        if selected_option is None:
            st.warning("Please select an option before submitting.")# if user click on submit button without selecting any option then it will show a warning message
        else:
            user_answer = selected_option[0] # Get the selected option (A, B, C, or D) from the user's selection.
            correct_answer = current_question["answer"]# Get the correct answer for the current question from the quiz data
            if user_answer == correct_answer:
                st.success("Correct Answer ")
                st.session_state.quiz_state["score"] += 1
            else:
                st.error(f"Wrong Answer ")
                st.write(f"Correct Answer: {correct_answer}")# Display the correct answer if the user's answer is wrong
            st.info(
                f"Explanation: {current_question['explanation']}"#for explanation
            )
        st.session_state.quiz_state["answered"] = True
    if st.session_state.quiz_state["answered"]:#after getting answer for the previous quuestions the user can select the next qesstopn button
        if st.button("Next Question"):#next question button will be visible only after the user has answered the current question. When the user clicks the "Next Question" button, it will move to the next quiz question by updating the current question index in the quiz_state memory and resetting the answered state to False for the next question.
            st.write(
            "New Index:",
            st.session_state.quiz_state["current_question"]
            )
            st.session_state.quiz_state["current_question"] += 1 #incrementning the next question
            st.session_state.quiz_state["answered"] = False
            st.rerun()
        #st.write(st.session_state.quiz_questions)   only for checking the quiz is in proper JSON structure or not
        
        #below code is for displaying the generated quiz ques in streamlit app
        
    #     st.subheader("Generated Quiz")# Display the generated quiz questions
    # # Display all generated questions
    #     for i, question in enumerate(quiz_data): # Loop through each generated quiz question and display it in the Streamlit app. The enumerate function is used to get both the index (i) and the question data (question) for each quiz question.
    #         st.markdown(f"### Question {i+1}")#display the question numbver
    #         st.write(question["question"]) #display the question
    #         st.write("A.", question["optionA"])#display option A
    #         st.write("B.", question["optionB"])
    #         st.write("C.", question["optionC"])
    #         st.write("D.", question["optionD"])
    #         st.divider()# it means to add a visual divider between each question for better readability in the Streamlit app.
    # #after generating the answer we'll update the chat history with new question and answer
