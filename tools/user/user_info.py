ANON = "Anonymous"

def extract_account_name() -> str:
    """
    Extracts the first part of an email address.
    
    Returns:
        The account name of the user
    """
    import streamlit as st
    email = st.user.email
    if email:
        idx = email.find('@')
        return email[:idx]
    return ANON

def extract_user_email() -> str:
    """
    Extracts the email of the user

    Returns:
        The email of the user
    """
    import streamlit as st
    if st.user.email:
        return st.user.email
    return ANON


def extract_full_name() -> str:
    """
    Extracts the full name of the user from the oauth user
    
    Returns:
        The full name of the user
    """
    import streamlit as st
    if st.user.name:
        return st.user.name
    return ANON

def get_user_credentials():
    """
    Gets the user credentials from the session state
    Returns:
        the user token or None if not logged in
    """
    import streamlit as st
    if st.session_state.token:
        return st.session_state.token
    return None