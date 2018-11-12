import src.stack as st


class Computation(object):

    def __init__(self, stack: st.Stack):
        self.stack = stack

    def clear_stack(self):
        self.stack.clear()
