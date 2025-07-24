Pre-Requisites:
----------------
1) All the tests needs to have DIVA(mainline) or ValSim(Yangra) installed
2) All tests need to targeted on specific capability eDP panel across CI/PreETM & GFT
3) All MPO/Flip/* tests will run in longer duration based on panel resolution its run against. 19*10 - 4 hours; 25*14 - 8 hours; 4K - 24 hours
4) All MPO/Flip/* tests should be run on Non PSR2 panel
5) All Secondary MPO tests should be run on 19x10 panel

Below tests needs to be run with 48Hz eDP panel only:
mpo_planeformat_48hz.py

Below tests need to be run with SHE tool connected:
mpo_hotplug_unplug.py
mpo_hotplug_unplug_stress.py
planeformat_lidswitch.py

Below test need to be run with allow_critical_dump enabled:
mpo_planeformat_media_tdr.py


