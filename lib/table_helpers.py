import streamlit as st


class CombactRecord:

    @staticmethod
    def newCombat(name, endurance, combat):
        record = st.session_state.combatRecord_edited

        ratio = st.session_state.lw_current_combat - combat
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

        st.session_state.combatRecord = st.session_state.combatRecord_edited

    @property
    def ratio(self):
        if self.current is not None:
            return self.current.ratio
        return None

    @property
    def enemy(self):
        if self.current is not None:
            return self.current["name"]
        return None

    @property
    def current(self):
        if (len(st.session_state.combatRecord_edited) == 0 or
                st.session_state.combatRecord_edited.iloc[0].ratio == "" or
                st.session_state.combatRecord_edited.iloc[0].enemy_endurance <= 0):
            return None
        return st.session_state.combatRecord_edited.iloc[0]

    @staticmethod
    def editor():
        ret = st.data_editor(st.session_state.combatRecord, use_container_width=True, hide_index=True,
                             num_rows="dynamic",
                             column_config={
                                 'ratio': "Combact Ratio",
                                 'lw_endurance': "Endurance Points",
                                 'name': "Enemy Name",
                                 'enemy_endurance': "Enemy Endurance Points"
                             })
        st.session_state.combatRecord_edited = ret  # Replaced here
        return ret

    def applyDamage(self, lw_delta_endurance, enemy_delta_endurance):
        current = self.current
        current.lw_endurance = max(current.lw_endurance + lw_delta_endurance, 0)
        current.enemy_endurance = max(current.enemy_endurance + enemy_delta_endurance, 0)

        st.session_state.combatRecord.iloc[0] = current
        st.session_state["lw_endurance"] = current.lw_endurance
