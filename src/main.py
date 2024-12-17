import streamlit as st
from src.services.state_service import StateService
from src.services.openai_service import OpenAIService
from src.components.sidebar import render_sidebar
from src.components.chat import render_group_chat
import logging

def setup_logging():
    # Set up root logger
    logging.basicConfig(
        level=logging.DEBUG,  # Default to INFO level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set our app's logger to DEBUG
    logger = logging.getLogger('src')
    logger.setLevel(logging.DEBUG)
    
    # Quiet down noisy loggers
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)

def main():
    setup_logging()
    st.set_page_config(
        page_title="Audience Builder",
        page_icon="🎯",
        layout="wide"
    )
    
    state_service = StateService()
    openai_service = OpenAIService()
    
    state_service.initialize_state()
    render_sidebar(state_service, openai_service)
    render_group_chat(openai_service)

if __name__ == "__main__":
    main() 