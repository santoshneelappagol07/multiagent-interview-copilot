from typing import Optional
import uuid

class SessionManager:
    def __init__(self):
        self.current_session_id = str(uuid.uuid4())

    def get_active_session_id(self) -> str:
        return self.current_session_id

    def create_new_session(self) -> str:
        self.current_session_id = str(uuid.uuid4())
        return self.current_session_id

session_manager = SessionManager()
