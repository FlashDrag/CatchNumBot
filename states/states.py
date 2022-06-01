from aiogram.dispatcher.filters.state import State, StatesGroup


class Bug(StatesGroup):
    get_bug = State() 


class Num(StatesGroup):
    # st_random_num = State() 
    st_number = State() 
    # st_attempt = State()
    # st_user_attempt = State()
