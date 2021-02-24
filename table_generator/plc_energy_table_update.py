import sys
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')  # noqa

import matplotlib.pyplot as plt  # noqa

from config import read_spreadsheet

# PLC file output settings:
DECLARATION_FORMAT = "{table_name} : ARRAY[0..{row_count}] OF ST_TableRow;"
ROW_FORMAT = (
    "{table_name}[{idx}].fEnergy := {energy:.6f}; "
    "{table_name}[{idx}].fLow := {trip_min:.6f}; "
    "{table_name}[{idx}].fHigh := {trip_max:.6f}; "
)
TABLE_FORMAT = """
    {rows}
"""

CODE_FORMAT = """\
<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4018.10">
  <POU Name="FB_EnergyTables" Id="{{3964a458-252f-4f9a-833e-ac7498f4c8f4}}" SpecialFunc="None">
    <Declaration><![CDATA[
(* WARNING: This file is auto-generated. Do not modify it.*)
FUNCTION_BLOCK FB_EnergyTables
VAR_INPUT
END_VAR
VAR_OUTPUT
    {declarations}
END_VAR
VAR
    bInitialized : BOOL := FALSE;
END_VAR
]]></Declaration>
    <Implementation>
      <ST><![CDATA[
(* WARNING: This file is auto-generated. Do not modify it.*)
IF NOT bInitialized THEN
    {tables}
    bInitialized := TRUE;
END_IF
]]></ST>
    </Implementation>
  </POU>
</TcPlcObject>
"""

pd.set_option('display.max_rows', 1000)


def generate_source(file=sys.stdout):
    """Generate the PLC code from the given spreadsheet."""
    declarations = []
    table_code = []

    data = {}
    for name, df in read_spreadsheet():
        data[name] = df
        table_name = f'st{name}'

        declarations.append(
            DECLARATION_FORMAT.format(
                table_name=table_name,
                row_count=len(df) - 1,
            )
        )
        rows = '\n    '.join(
            ROW_FORMAT.format(idx=idx, table_name=table_name, **dict(row))
            for idx, (_, row) in enumerate(df.iterrows())
        )
        table_code.append(
            TABLE_FORMAT.format(
                table_name=table_name,
                rows=rows,
                row_count=len(df)
            )
        )

    code = CODE_FORMAT.format(
        tables='\n'.join(table_code),
        declarations='\n    '.join(declarations),
    )

    print(code, file=file)
    return data


def plot_data(ax, key, data):
    ax.set_title(key)
    df = data[key]
    ax.fill_between(
        df.energy, df.trip_min, df.trip_max,
        where=(df.trip_max > df.trip_min),
        interpolate=True,
        color='red',
        alpha=0.2,
        hatch='/',
    )

    df.trip_min.plot(ax=ax, lw=1, color='black')
    df.trip_max.plot(ax=ax, lw=1, color='red')

    ax.legend(loc='best')
    ax.set_yscale('log')
    ax.set_ylabel('Reff')
    ax.set_xlabel('Energy [keV]')
    return df


def main():
    data = generate_source(file=sys.stdout)

    _, axes = plt.subplots(ncols=2, nrows=2, constrained_layout=True,
                           dpi=120, figsize=(11, 8))
    # plt.ion()
    keys = list(data)
    plot_data(axes[0, 0], keys[0], data)
    plot_data(axes[0, 1], keys[1], data)
    plot_data(axes[1, 0], keys[2], data)
    plot_data(axes[1, 1], keys[3], data)
    plt.suptitle("Disallowed Effective Radius Regions")
    plt.savefig('interlock_regions.png')
    # plt.ioff()
    return data


if __name__ == '__main__':
    data = main()
