# This file handles the raw background operations away from the user interface

def compute_server_load(active_users):
    """Calculates the estimated infrastructure resource load."""
    base_load = active_users * 12.5
    return base_load

def get_system_greeting(name):
    """Generates a custom welcome message for the operator."""
    return f"Welcome back, Operator {name}. Secure terminal established."
