../playnite_to_depressurizer_1_2.pext: *.yaml *.psm1 *.md *.py
	$(LOCALAPPDATA)/Playnite/Toolbox.exe verify addon giovanh_playnite_to_depressurizer.yaml
	$(LOCALAPPDATA)/Playnite/Toolbox.exe pack ./ ../