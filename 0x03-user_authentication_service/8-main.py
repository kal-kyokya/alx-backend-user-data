#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

session_id = auth.create_session(email)

print(session_id)
print(auth.create_session("unknown@email.com"))

print(auth.get_user_from_session_id(session_id))
