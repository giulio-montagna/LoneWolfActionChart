import random

import streamlit as st

from lib.combat import damage
from lib.editors import Editors
from lib.data import combatRecord, setupState

st.set_page_config(
    layout="wide"
)


def actionChart():
    st.markdown("# Action Chart")
    c1, c2 = st.columns([4, 5])
    with c1:
        st.markdown("#### Kai Disciplines")
        Editors.disciplines()
        st.markdown("#### Backpack")
        c11, c12 = st.columns([2, 1])
        with c11:
            Editors.backPack()
        with c12:
            st.text_area("Meals")
            st.text_area("BeltPouch")
        st.markdown("#### Weapons")
        Editors.weapons()

    with (c2):
        c21, c22 = st.columns([1, 1])
        with c21:
            st.markdown("**Combat Skill**")
            st.number_input("Base", key="lw_combat", step=1)

            edited_df = Editors.combatModifiers()
            edited_df = edited_df.dropna()
            bonus = (sum([int(i) for i in edited_df[edited_df.active].modifier]))
            st.session_state["lw_current_combat"] = st.session_state["lw_combat"] + bonus
            st.markdown(f"**current**:  {st.session_state['lw_current_combat']}")
        with c22:
            st.markdown("**Endurance Point**")
            st.number_input("Current", key="lw_endurance", step=1)
            st.number_input("Max", key="lw_endurance_max", step=1)
        Editors.combatRecord()
        st.markdown("#### Special Items List")
        Editors.specialItems()


def sidebar():
    with st.sidebar:
        menu = st.radio("Select Action",
                        ("New Combat", "Roll/Combat"))
        st.divider()
        st.markdown("### " + menu)
        if menu == "New Combat":
            st.markdown("#### Enemy")
            name = st.text_input("Name")
            endurance = st.number_input("Endurance", value=12)
            combat = st.number_input("Combat", value=12)
            if st.button("Add"):
                combatRecord.newCombat(name, endurance, combat)
        if menu == "Roll/Combat":
            if st.button("Roll"):
                st.session_state.randomNumber = random.randint(0, 9)
            placeholder = st.empty()
            with placeholder.container():
                if "randomNumber" in st.session_state:
                    randomNumber = st.session_state.randomNumber
                    st.markdown(f"#### Random Number: {randomNumber}")
                    if combatRecord.current is not None:
                        dam = damage(combatRecord.ratio, randomNumber)
                        lw_delta_endurance = st.number_input("Lone Wolf Endurace", value=dam.loneWolf,
                                                             key="lw_delta_endurance")
                        enemy_delta_endurance = st.number_input(f"{combatRecord.enemy} Endurace", value=dam.enemy,
                                                                key="enemy_delta_endurance")
                        if st.button("Apply"):
                            combatRecord.applyDamage(lw_delta_endurance, enemy_delta_endurance)
                            del st.session_state.randomNumber
                            placeholder.empty()

        else:
            if "randomNumber" in st.session_state:
                del st.session_state.randomNumber


setupState()
sidebar()
actionChart()
