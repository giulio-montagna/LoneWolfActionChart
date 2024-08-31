import random

import streamlit as st

import pandas as pd

from lib.combact import damage

st.set_page_config(
    layout="wide"
)


class CombactRecord:
    @staticmethod
    def create():
        if "_CombactRecord" not in st.session_state:
            st.session_state._CombactRecord = CombactRecord()
        return st.session_state._CombactRecord

    def __init__(self):
        self.combactRecord = pd.DataFrame([["", "", "", ""]], columns=[
            'ratio', 'lw_endurance',
            'name', 'enemy_endurance'])

    def newCombact(self, name, endurance, combact):
        record = self.combactRecord
        ratio = st.session_state.lw_current_combact - combact
        item = {
            "ratio": int(ratio),
            "lw_endurance": st.session_state.lw_endurance,
            "name": name,
            "enemy_endurance": int(endurance)
        }
        if len(record) > 0 and record.iloc[0].ratio == "":
            record.loc[0] = item
        else:
            record.loc[-1] = item
            record.sort_index(inplace=True)
            record.reset_index(drop=True, inplace=True)

    @property
    def ratio(self):
        return self.combactRecord.iloc[0].ratio

    @property
    def enemy(self):
        return self.combactRecord.iloc[0]["name"]

    @property
    def record(self):
        return self.combactRecord

    @property
    def current(self):
        return self.combactRecord.iloc[0]

    def editor(self):
        ret = st.data_editor(self.combactRecord, use_container_width=True, hide_index=True, num_rows="dynamic",
                             column_config={
                                 'ratio': "Combact Ratio",
                                 'lw_endurance': "Endurance Points",
                                 'name': "Enemy Name",
                                 'enemy_endurance': "Enemy Endurance Points"
                             })
        self.combactRecord = ret
        return ret

    def applyDamage(self, lw_delta_endurance, enemy_delta_endurance):
        current = self.current
        current.lw_endurance = max(current.lw_endurance + lw_delta_endurance, 0)
        current.enemy_endurance = max(current.enemy_endurance + enemy_delta_endurance, 0)
        st.session_state["lw_endurance"] = current.lw_endurance


disciplines = pd.DataFrame(
    [["", "Novice"],
     ["", "Intuite"],
     ["", "Doan"],
     ["", "Acolyte"],
     ["", "Aspirant"],
     ["", "Guardian"],
     ["", "Warman"],
     ["", "Savant"],
     ], columns=["Discipline", "Rank"]
)
backPack = pd.DataFrame([[""], [""], [""], [""], [""], [""], [""], [""], ], columns=["Item"])
combactRecord = CombactRecord.create()
combactModifiers = pd.DataFrame([["", "", False]], columns=["name", "modifier", "active"])
weapons = pd.DataFrame([[""], [""]], columns=["Weapon"])
specialItems = pd.DataFrame([["", ""]], columns=["Description", "Effects"])


def setupState():
    if "setup" in st.session_state:
        return

    st.session_state.lw_combact = 18
    st.session_state.lw_endurance_max = 23
    st.session_state.lw_endurance = 23

    st.session_state.setup = True


def actionChart():
    st.markdown("# Action Chart")
    c1, c2 = st.columns([4, 5])
    with c1:
        st.markdown("#### Kai Disciplines")
        st.data_editor(disciplines, use_container_width=True, hide_index=True,
                       column_config={"Discipline": st.column_config.Column(
                           "Discipline",
                           width="large",
                           disabled=False
                       ),
                           "Rank": st.column_config.Column(
                               "Rank",
                               width="small",
                               disabled=True
                           )})
        st.markdown("#### Backpack")
        c11, c12 = st.columns([2, 1])
        with c11:
            st.data_editor(backPack, use_container_width=True, hide_index=True)
        with c12:
            st.text_area("Meals")
            st.text_area("BeltPouch")
        st.markdown("#### Weapons")
        st.data_editor(weapons, use_container_width=True, hide_index=True)

    with c2:
        c21, c22 = st.columns([1, 1])
        with c21:
            st.markdown("**Combact Skill**")
            st.number_input("Base", key="lw_combact", step=1)
            edited_df = st.data_editor(combactModifiers, use_container_width=True, hide_index=True, num_rows="dynamic",
                                       column_config={
                                           "name": "Name",
                                           "modifier": st.column_config.NumberColumn("Modifier", step=1),
                                           "active": "Active",
                                       })
            edited_df = edited_df.dropna()
            bonus = (sum([int(i) for i in edited_df[edited_df.active].modifier]))
            st.session_state["lw_current_combact"] = st.session_state["lw_combact"] + bonus
            st.markdown(f"**current**:  {st.session_state['lw_current_combact']}")
        with c22:
            st.markdown("**Endurance Point**")
            st.number_input("Current", key="lw_endurance", step=1)
            st.number_input("Max", key="lw_endurance_max", step=1)
        combactRecord.editor()
        st.markdown("#### Special Items List")
        st.data_editor(specialItems, use_container_width=True, hide_index=True, num_rows="dynamic")


def sidebar():
    with st.sidebar:
        menu = st.radio("Select Action",
                        ("New Combact", "Combact Round"))
        st.divider()
        st.markdown("### " + menu)
        if menu == "New Combact":
            st.markdown("#### Enemy")
            name = st.text_input("Name")
            endurance = st.number_input("Endurance", value=12)
            combact = st.number_input("Combact", value=12)
            if st.button("Add"):
                combactRecord.newCombact(name, endurance, combact)
        if menu == "Combact Round":
            if st.button("Roll"):
                st.session_state.randomNumber = random.randint(0, 9)
            placeholder = st.empty()
            with placeholder.container():
                if "randomNumber" in st.session_state:
                    randomNumber = st.session_state.randomNumber
                    st.markdown(f"#### Random Number: {randomNumber}")
                    dam = damage(combactRecord.ratio, randomNumber)
                    lw_delta_endurance = st.number_input("Lone Wolf Endurace", value=dam.loneWolf,
                                                         key="lw_delta_endurance")
                    enemy_delta_endurance = st.number_input(f"{combactRecord.enemy} Endurace", value=dam.enemy,
                                                            key="enemy_delta_endurance")
                    if st.button("Apply"):
                        combactRecord.applyDamage(lw_delta_endurance, enemy_delta_endurance)
                        del st.session_state.randomNumber
                        placeholder.empty()

        else:
            if "randomNumber" in st.session_state:
                del st.session_state.randomNumber


setupState()
sidebar()
actionChart()
