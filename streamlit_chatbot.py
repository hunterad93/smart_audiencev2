import streamlit as st
from openai import OpenAI
import json
import uuid

ASSISTANT_ID = "asst_KFSoUugvWdugdeLCrpNYlStD"

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

def create_new_group():
    group_id = str(uuid.uuid4())
    client = OpenAI()
    thread_id = client.beta.threads.create().id
    
    st.session_state.group_threads[group_id] = thread_id
    st.session_state.audience["data_groups"][group_id] = {
        "thread_id": thread_id,
        "status": "include",
        "group_name": "New Group",
        "segments": []
    }
    return group_id

def render_sidebar():
    with st.sidebar:
        st.title("Group Management")
        
        if st.button("Create New Group", use_container_width=True):
            new_group_id = create_new_group()
            st.session_state.active_group_id = new_group_id
            st.rerun()
        
        st.divider()
        
        for group_id, group in st.session_state.audience["data_groups"].items():
            with st.container():
                if st.button(
                    group["group_name"],
                    key=f"select_{group_id}",
                    use_container_width=True
                ):
                    st.session_state.active_group_id = group_id
                    st.rerun()
                
                col1, col2 = st.columns(2)
                with col1:
                    status = st.toggle(
                        "Include",
                        value=group["status"] == "include",
                        key=f"status_{group_id}"
                    )
                    group["status"] = "include" if status else "exclude"
                with col2:
                    if st.button(
                        "Delete",
                        key=f"delete_{group_id}",
                        use_container_width=True
                    ):
                        del st.session_state.audience["data_groups"][group_id]
                        del st.session_state.group_threads[group_id]
                        if st.session_state.active_group_id == group_id:
                            st.session_state.active_group_id = None
                        st.rerun()
                
                st.divider()

def render_group_chat():
    if not st.session_state.active_group_id:
        st.info("Select a group from the sidebar or create a new one")
        return
    
    group = st.session_state.audience["data_groups"][st.session_state.active_group_id]
    thread_id = group["thread_id"]
    
    st.subheader(f"Editing: {group['group_name']}")
    
    messages = get_thread_messages(thread_id)
    for message in messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_group_definition(message["content"])
            else:
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Describe the segments you want in this group"):
        handle_chat_input(prompt, thread_id, group)

def get_thread_messages(thread_id):
    client = OpenAI()
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return [{"role": m.role, "content": m.content[0].text.value} for m in messages.data]

def handle_chat_input(prompt, thread_id, group):
    client = OpenAI()
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    
    with st.chat_message("assistant"):
        response = get_assistant_response(client, thread_id)
        if response:
            group_data = display_group_definition(response)
            if group_data:
                group.update(group_data)

def display_group_definition(response_text):
    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        group_data = json.loads(json_str)
        
        st.markdown(f"### {group_data['group_name']}")
        for segment in group_data['segments']:
            st.markdown(f"**{segment['full_path'].split(' > ')[-1]}**")
            st.markdown(f"{segment['description']}")
            st.divider()
        
        return group_data
            
    except Exception as e:
        st.error(f"Error parsing response: {str(e)}")
        st.code(response_text)
        return None

def get_assistant_response(client, thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value
    else:
        st.error(f"Run failed with status: {run.status}")
        return None

def main():
    st.set_page_config(
        page_title="Audience Builder",
        page_icon="🎯",
        layout="wide"
    )
    
    initialize_state()
    render_sidebar()
    render_group_chat()

if __name__ == "__main__":
    main()