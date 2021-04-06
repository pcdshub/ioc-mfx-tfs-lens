table_generator
===============

Scripts in this directory will generate either IOC-compatible or
TwinCAT-compatible tables.

``MFX_EnergyLensInterlock_Tables_Transposed.xlsx``: source for the tables.
``config.py``: shared configuration.
``header_creator.py``: C header table.
``plc_energy_table_update.py``: PLC code generator
``FB_EnergyTables.TcPOU``: PLC code generator output (should be copied to PLC repo)

Additionally, there are checkout-focused scripts contained here that rely on this
same data.

Performing a checkout
=====================

First, load an IPython session with ``checkout.py``:

    # Note: replace the IOC directory with the currently deployed version.
    $ cd /reg/g/pcds/epics-dev/klauer/ioc-mfx-tfs-lens/table_generator
    $ ipython -i checkout.py


If the above times out, re-run the script.  It's ophyd related and will be
resolved eventually.  Otherwise, continue on and perform some scans.

To perform a scan for a single XRT lens, use:

    sweep_and_plot_xrt(xrt_lens, num_steps=100)

To perform a scan for _all_ XRT lenses, use:

    sweep_and_plot_xrt_all(num_steps=100)

When finished, run:

    $ python generate_report.py

To generate a report from the latest results, see the following section.

Report generation
=================

Checkout results can be aggregated into a report using ``generate_report.py``.
It has some additional requirements (in ``requirements.txt``) - primarily
``reportlab``.

If unavailable in the current pcds Python environment, you may consider creating
your own conda environment, or using ``pip`` to install it just for yourself.
From psbuild-rhel7, run ``pip install --user reportlab``.

``generate_report.py``: Generate ``report.pdf`` from the checkout-generated
``pre_focus*.{pdf,xlsx}``.
