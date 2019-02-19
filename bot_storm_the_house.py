import state_helper

STATE_MANAGER = state_helper.StateHelper()

while True:
    STATE_MANAGER.handle_states()
