# ChatCV

Welcome to ChatCV, an innovative and interactive tool designed to present your curriculum vitae (CV) in a unique and engaging format.

## Description

ChatCV leverages the power of Retrieval-Augmented Generation (RAG) and ChatGPT to create a dynamic, conversational experience for showcasing your professional profile. Unlike traditional personal webpages, ChatCV offers a distinctive approach to presenting your information, making your CV more interactive and accessible. This project features LangChain, LangServe, and LLama-index libraries.

## Features

1. **Interactive Chat Interface**: Engage viewers with a conversational format that can answer questions and provide detailed information about your career and qualifications.
2. **Enhanced Presentation**: Move beyond static text and typical layouts by offering a more engaging way to explore your professional background.
3. **Customizable Content**: Tailor the chat responses to highlight key aspects of your experience, skills, and accomplishments.
4. **User-Friendly**: Easy to set up and use, allowing you to focus on what matters most – your career journey.

## Benefits

1. **Stand Out**: Differentiate yourself from others by using a modern and interactive method to present your CV.
2. **Increased Engagement**: Potential employers and network connections are more likely to interact with and remember your profile.
3. **Accessibility**: Provide information in a conversational manner that can be more intuitive and accessible to a wider audience.

## Installation

To install ChatCV, follow these steps:

1. Clone the repository.
2. Add your CV, publications, etc., to the `chatcv/media` directory. These files will be used as retrieved context for the chat. All types of textual files can be uploaded.
3. Create a [GPT key](https://platform.openai.com/api-keys). You can create a `.env` file to use this key for debugging. Remember to keep this key private!
4. Deploy the app. This app can be easily deployed on [Railway](https://railway.app?referralCode=TAj8BK). Alternatives are suggested by [LangServe](https://python.langchain.com/v0.2/docs/langserve/).
5. Add the API URL to the `frontend/streamlit_frontend.py` file. Update the template questions of the frontend `template_questions = []`

## Usage

Here's how you can use ChatCV:

1. Process your media files and embed them for retrieval. To recalculate embeddings, use `https://API/compute_embeddings`.
2. Run the Streamlit chat with `streamlit run frontend/streamlit_frontend.py`. The Streamlit front-end can be deployed for free in [Streamlit](https://share.streamlit.io/deploy)
3. To add new files or update existing ones, upload new files to the `media` folder and reprocess the embeddings via the API.

## License

[Lorenzo Baraldi] © [2024]. [Apache 2.0 License].
