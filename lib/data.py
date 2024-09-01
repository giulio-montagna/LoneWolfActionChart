import streamlit as st
import pandas as pd
from .table_helpers import CombactRecord

combatRecord = CombactRecord()


def setupState():
    if "setup" in st.session_state:
        return

    # properties
    st.session_state.lw_combat = 18
    st.session_state.lw_endurance_max = 23
    st.session_state.lw_endurance = 23

    # tables
    st.session_state.backPack = pd.DataFrame([[""], [""], [""], [""], [""], [""], [""], [""]], columns=["Item"])
    st.session_state.combatRecord = pd.DataFrame([["", "", "", ""]],
                                                 columns=['ratio', 'lw_endurance', 'name', 'enemy_endurance'])
    st.session_state.combatModifiers = pd.DataFrame([["", "", False]], columns=["name", "modifier", "active"])
    st.session_state.weapons = pd.DataFrame([[""], [""]], columns=["Weapon"])
    st.session_state.specialItems = pd.DataFrame([["", ""]], columns=["Description", "Effects"])
    st.session_state.disciplines = pd.DataFrame(
        [
            ["", "Novice"],
            ["", "Intuite"],
            ["", "Doan"],
            ["", "Acolyte"],
            ["", "Aspirant"],
            ["", "Guardian"],
            ["", "Warman"],
            ["", "Savant"],
        ], columns=["Discipline", "Rank"]
    )

    st.session_state.setup = True
