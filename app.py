import streamlit as st
from dotenv import load_dotenv
from langchain_experimental.agents import create_csv_agent  # Import create_csv_agent from langchain_experimental.agents
from langchain.llms import OpenAI  # Import OpenAI from langchain.llms

def load_prompt(context, question):
    prompt_template = """ 
        You need to answer the question in the sentence as same as in the  pdf content. 
        Given below is the context and question of the user.
        context = {}
        question = {}
        if the answer is not in the pdf answer "I don't have an answer for your query."
    """
    prompt = prompt_template.format(context, question)
    return prompt

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Talk to CSV FILES", layout="wide")

def main():
    # Load environment variables
    load_dotenv()

    # Display markdown content
    st.markdown("""
    ### CSV  : Get instant insights from your Files
    ### How It Works
    Follow these simple steps to interact with the chatbot:
    1. **Enter Your API Key**
    2. **Upload Your Files**
    3. **Ask a Question**
    """)

    # Ask user for their OpenAI API Key
    api_key = st.text_input("Enter your Open API Key:", type="password", key="api_key_input")

    # Check if API key is provided
    if api_key:
        # Assuming OpenAI is a class from which you create an instance
        openai_instance = OpenAI(api_key=api_key, temperature=0)
        
        # Your Streamlit UI code follows...
        st.header("Ask your CSV 📈")

        csv_file = st.file_uploader("Upload a CSV file", type="csv")
        if csv_file is not None:
            # Opt-in to allow dangerous code execution
            agent = create_csv_agent(openai_instance, csv_file, allow_dangerous_code=True, verbose=True)

            user_question = st.text_input("Ask a question about your CSV: ")

            if user_question is not None and user_question != "":
                prompt = load_prompt("Your context goes here", user_question)
                with st.spinner(text="In progress..."):
                    response = agent.run(prompt)
                    if response.strip().lower() == "i don't know the answer. can you ask another question?":
                        st.warning("I don't know the answer. Can you ask another question?")
                    else:
                        st.write(response)

if __name__ == "__main__":
    main()
