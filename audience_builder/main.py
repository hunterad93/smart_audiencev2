import streamlit as st
from services.state_service import StateService
from services.openai_service import OpenAIService
from services.ttd_interface import TTDInterfaceService
from components.sidebar import render_sidebar
from components.chat import render_group_chat
import logging

def setup_logging():
    # Set up root logger
    logging.basicConfig(
        level=logging.DEBUG,  # Default to INFO level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set our app's logger to DEBUG
    logger = logging.getLogger('audience_builder')
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
    ttd_service = TTDInterfaceService(sandbox=False)  # Always use sandbox for safety
    
    state_service.initialize_state()
    render_sidebar(state_service, openai_service, ttd_service)
    render_group_chat(openai_service)

if __name__ == "__main__":
    main() 