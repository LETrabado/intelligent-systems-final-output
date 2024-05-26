"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import google.generativeai as genai

import streamlit as st
import time

genai.configure(api_key="AIzaSyBMjvecoTaxlvKOMUb5UhBS3l9u_FCGm9o")

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You are a friendly and encouraging maid named Sally. You are a cooking assistant who answers questions about cooking and provides recipes for asked dishes. You address the user as mam/sir",
)

def app():

    # Initialize chat history
    # Initialize bot_response
    if 'bot_response' not in st.session_state:
      st.session_state['bot_response'] = ""
    if 'chat_history' not in st.session_state:
      st.session_state['chat_history'] = []

    #display logo and title
    st.image("Logo.png")

    #developer text
    text = """Luis Emil Trabado BSCS 3B-AI\n
    Developed as the final output for CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """

    with st.expander("Click to display developer information."):
        st.text(text)

    #introduction
    st.subheader("Improve your cooking with Cooking Assistant Sally")
    text = """Hello I'm Sally, your friendly and knowledgeable cooking assistant! 
    Powered by Gemini 1.5 Flash API, Sally is here to transform your kitchen experience.
    Whether you're a seasoned chef or a complete beginner, Sally is here to guide you every 
    step of the way. First please ask for a recipe you want to cook and I will provide. After
    you can ask me additional questions. Be careful not to remove the requested recipe or it
    will be overwritten."""
    st.write(text)

    #recipe request text_input and button
    dish = st.text_input("What dish will you cook today(include serving size)?", disabled = False)
    #create prompt for requesting recipe to be submitted to the model
    recipe_get = "Provide a recipe for [" + dish + "]... Please don't ask other questions and respond with the recipe only or if you cannot provide a recipe or the words inside the [] is not a dish please respond that the user needs to provide a dish"
    if st.button("Get recipe"):
        bot_response = "Please Enter a dish"
        progress_bar = st.progress(0, text="Sally is thinking, please wait...")
        if recipe_get:

            #always reset history for new recipes
            new_history = []

            # Add user message to chat history
            new_history.append({"role": "user", "parts": recipe_get})

            chat_session = model.start_chat(
              history=[
              ]
            )

            # Generate response from Gemma
            bot_response = chat_session.send_message(recipe_get,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            # Access the content of the response text
            bot_response = bot_response.text
            # Add bot response to chat history
            new_history.append({"role": "model", "parts": bot_response})

            #update session state
            st.session_state['chat_history'] = new_history
            st.session_state['bot_response'] = bot_response

        else:
            st.error("Please enter a dish.")
            return
        
        # update the progress bar
        for i in range(100):
            # Update progress bar value
            progress_bar.progress(i + 1)
            # Simulate some time-consuming task (e.g., sleep)
            time.sleep(0.01)
    # Display bot_response retrieved from session state (after button click)
    if st.session_state['bot_response']:
      st.write(st.session_state['bot_response'])


    #additional assistance text_input and button
    question = st.text_input("Need additional assistance?")
    if st.button("Ask Sally"):
    
        if question:
            if st.session_state['chat_history']:
               chat_history = st.session_state['chat_history']
            progress_bar = st.progress(0, text="Sally is thinking, please wait...")

            chat_session = model.start_chat(
              history = chat_history
            )

            # Add user message to chat history
            chat_history.append({"role": "user", "parts": question})

            # Generate response from Gemini with the prompt
            bot_response = chat_session.send_message(question,
                generation_config=generation_config,
                safety_settings=safety_settings
            )


            # Access the content of the response text
            bot_response = bot_response.text

            # Add bot response to chat history
            chat_history.append({"role": "model", "parts": bot_response})

            # Display chat history
            st.write(bot_response)

            # #If want to show History 
            # st.markdown("""---""")
            # st.subheader("chat_history")
            # for message in chat_history:
            #     st.write(f"{message['role']}: {message['parts']}")


            #update the progress bar
            for i in range(100):
                # Update progress bar value
                progress_bar.progress(i + 1)
                # Simulate some time-consuming task (e.g., sleep)
                time.sleep(0.01)
            # Progress bar reaches 100% after the loop completes
        else:
            st.error("Please enter a prompt.")

    
#run the app
if __name__ == "__main__":
  app()
