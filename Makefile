../playnite_to_depressurizer_1_1.pext: *.yaml *.psm1 *.md *.py
	-../../Toolbox.exe verify addon giovanh_playnite_to_depressurizer.yaml
	../../Toolbox.exe pack ./ ../