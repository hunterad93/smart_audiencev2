import streamlit as st
import uuid
from services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

class StateService:
    @staticmethod
    def initialize_state():
        if "audience" not in st.session_state:
            st.session_state.audience = {
                "audience_name": "New Audience",
                "data_groups": {}
            }
        if "active_group_id" not in st.session_state:
            st.session_state.active_group_id = None
        if "group_threads" not in st.session_state:
            st.session_state.group_threads = {}
        if 'selected_kpi' not in st.session_state:
            st.session_state.selected_kpi = None
        logger.info("=== Current State ===")
        logger.info(f"Audience: {st.session_state.audience}")
        logger.info(f"Active Group: {st.session_state.active_group_id}")
        logger.info(f"Group Threads: {st.session_state.group_threads}")
    
    @staticmethod
    def get_thread_for_group(group_id: str) -> str:
        return st.session_state.group_threads.get(group_id)

    @staticmethod
    def create_group(openai_service: OpenAIService):
        group_id = str(uuid.uuid4())
        thread_id = openai_service.create_thread()
        
        st.session_state.group_threads[group_id] = thread_id
        st.session_state.audience["data_groups"][group_id] = {
            "thread_id": thread_id,
            "status": "include",
            "group_name": "New Group",
            "segments": [],
            "assistant_id": None
        }
        return group_id 

    @staticmethod
    def set_group_assistant(group_id: str, assistant_id: str):
        if group_id in st.session_state.audience["data_groups"]:
            st.session_state.audience["data_groups"][group_id]["assistant_id"] = assistant_id

    @staticmethod
    def update_group_status(group_id: str, status: str):
        logger.info(f"Updating group {group_id} status to {status}")
        logger.info(f"Before update: {st.session_state.audience['data_groups'][group_id]}")
        st.session_state.audience["data_groups"][group_id]["status"] = status
        logger.info(f"After update: {st.session_state.audience['data_groups'][group_id]}")