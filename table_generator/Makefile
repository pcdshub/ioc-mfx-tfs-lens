all: FB_EnergyTables.TcPOU ../lensApp/src/interlockTables.h dump_tables plot

../lensApp/src/interlockTables.h: MFX_EnergyLensInterlock_Tables_Transposed.xlsx header_creator.py config.py
	TRANSFOCATOR_SPREADSHEET=$${PWD}/MFX_EnergyLensInterlock_Tables_Transposed.xlsx \
		python -c "import transfocate; print(transfocate.table.create_ioc_header())" > $@
	# Some info for the README:
	mv interlock_regions.png ../

FB_EnergyTables.TcPOU: MFX_EnergyLensInterlock_Tables_Transposed.xlsx config.py plc_energy_table_update.py
	TRANSFOCATOR_SPREADSHEET=$${PWD}/MFX_EnergyLensInterlock_Tables_Transposed.xlsx \
		python -c "import transfocate; print(transfocate.table.create_plc_code())" > $@


dump_tables: ../lensApp/src/interlockTables.h plot.py
	gcc -o dump_tables -Wall -I../lensApp/src dump_tables.c ../lensApp/src/interlockTables.c
	./dump_tables


plot: dump_tables
	python plot.py TABLE_*

clean:
	rm -f TABLE_LENS1_750 TABLE_LENS2_428 TABLE_LENS3_333 \
		TABLE_NO_LENS TABLE_LENS1_750.pdf TABLE_LENS2_428.pdf TABLE_LENS3_333.pdf \
		TABLE_NO_LENS.pdf dump_tables


.PHONY: dump_tables plot clean
