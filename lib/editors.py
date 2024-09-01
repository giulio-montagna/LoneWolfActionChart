import streamlit as st

from lib.data import combatRecord


class Editors:
    @staticmethod
    def disciplines():
        ret = st.data_editor(st.session_state.disciplines, use_container_width=True, hide_index=True,
                             column_config={"Discipline": st.column_config.Column(
                                 "Discipline",
                                 width="large",
                                 disabled=False),
                                 "Rank": st.column_config.Column(
                                     "Rank",
                                     width="small",
                                     disabled=True)})
        st.session_state.disciplines_edited = ret
        return ret

    @staticmethod
    def backPack():
        ret = st.data_editor(st.session_state.backPack, use_container_width=True, hide_index=True)
        st.session_state.backPack_edited = ret
        return ret

    @staticmethod
    def combatRecord():
        return combatRecord.editor()

    @staticmethod
    def combatModifiers():
        ret = st.data_editor(st.session_state.combatModifiers, use_container_width=True, hide_index=True,
                             num_rows="dynamic",
                             column_config={
                                 "name": "Name",
                                 "modifier": st.column_config.NumberColumn("Modifier", step=1),
                                 "active": "Active",
                             })
        st.session_state.combatModifiers_edited = ret
        return ret

    @staticmethod
    def weapons():
        ret = st.data_editor(st.session_state.weapons, use_container_width=True, hide_index=True)
        st.session_state.weapons_edited = ret
        return ret

    @staticmethod
    def specialItems():
        ret = st.data_editor(st.session_state.specialItems, use_container_width=True, hide_index=True,
                             num_rows="dynamic")
        st.session_state.specialItems_edited = ret
        return ret
