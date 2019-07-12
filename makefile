.PHONY: clean rmatch_analysis bats_man_analysis

match_analysis: 
	bokeh serve --show match_analysis.py

bats_man_analysis: 
	bokeh serve --show bats_man_perf.py