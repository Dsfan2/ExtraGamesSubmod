default persistent._extragames_unlocked = False
default persistent._extragames_lore_status = 0
default persistent._exg_millionaire_firsttime = True
default persistent._exg_millionaire_last_win = False
init -990 python in mas_submod_utils:
    h_submod = Submod(
        author="Dsfan2",
        name="Extra Games Submod",
        description="A submod that adds brand new games for you and Monika to play!",
        version="0.1.0"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Extra Games Submod",
            user_name="Dsfan2",
            repository_name="ExtraGamesSubmod"
    )