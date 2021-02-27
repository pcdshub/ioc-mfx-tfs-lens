table_generator
===============

Scripts in this directory will generate either IOC-compatible or
TwinCAT-compatible tables.

``MFX_EnergyLensInterlock_Tables_Transposed.xlsx``: source for the tables.
``config.py``: shared configuration.
``header_creator.py``: C header table.
``plc_energy_table_update.py``: PLC code generator
``FB_EnergyTables.TcPOU``: PLC code generator output (should be copied to PLC repo)


Report generation
=================

Checkout results can be aggregated into a report using ``generate_report.py``.
It has some additional requirements (in ``requirements.txt``) - primarily
``reportlab``.

``generate_report.py``: Generate ``report.pdf`` from the checkout-generated
``pre_focus*.{pdf,xlsx}``.
