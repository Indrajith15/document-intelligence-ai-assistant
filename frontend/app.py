
import requests
import streamlit as st

st.set_page_config(
    page_title="Document Intelligence AI Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Intelligence AI Assistant")

st.write(
    "Upload your PDF documents and ask questions about their content."
)


st.header("Upload your document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process Document"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()

                st.success("Document processed successfully!")

                st.write("Filename:", result["filename"])
                st.write("Total pages:", result["total_pages"])
                st.write("Total chunks:", result["total_chunks"])
                st.write("Stored chunks:", result["total_stored"])

            else:
                st.error(
                    f"Document processing failed. "
                    f"Server returned status code: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the backend. "
                "Please check whether the FastAPI server is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The document processing request timed out. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"An error occurred: {error}")


st.header("Chat with your document")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept a new question
question = st.chat_input("Ask something about your document...")

if question:

    # Display the user's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Send the question to FastAPI
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={"question": question},
                    timeout=60
                )

                if response.status_code == 200:

                    result = response.json()
                    answer = result["answer"]

                    st.write(answer)

                    # Save the AI response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:
                    st.error(
                        f"Something went wrong. "
                        f"Server returned status code: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Please check whether the FastAPI server is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"An error occurred: {error}")
