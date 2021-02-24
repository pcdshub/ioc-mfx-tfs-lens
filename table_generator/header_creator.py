import sys
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')  # noqa

import matplotlib.pyplot as plt  # noqa

from config import read_spreadsheet


# Header file output settings:
ROW_FORMAT = "{{{energy:.6f}, {trip_min:.6f}, {trip_max:.6f}}}"
HEADER = """
/* WARNING: This file is auto-generated. Do not modify it. */
#ifndef _H_MFX_RANGE_TABLE
#define _H_MFX_RANGE_TABLE

#include <stdio.h>

typedef struct {
    double energy;
    double low;
    double high;
} RangeRow;

typedef struct {
    const char *table_name;
    const int num_rows;
    const RangeRow rows[];
} RangeTable;


/*
 * find_limits
 *
 * Returning interpolated lower- and upper- disallowed ranges for the given
 * table based on energy.
 *
 * Parameters:
 *  RangeRow *result
 *      The row to store the interpolated result in.  The energy will indicate
 *      the closest tabulated value.
 *  const RangeTable *table
 *      The table.
 *  double find_energy
 *      The energy to search for.
 *
 * Returns: bool
 *      False if arguments were invalid.
 *      True if result was set.
 */
bool find_limits(RangeRow *result, const RangeTable *table, double find_energy);

/*
 * print_row
 *
 * Print a single row from the table in a CSV-compatible format.
 *
 * Parameters:
 *  FILE *fp
 *      The file pointer to print to (stdout, stderr, etc.)
 *  const RangeRow row
 *      The row (by value, saving you from typing &).
 *  bool newline
 *      Add a newline at the end.
 */
void print_row(FILE *fp, const RangeRow row, bool newline);
"""

FOOTER = """
#endif // _H_MFX_RANGE_TABLE
"""

TABLE_FORMAT = """
const RangeTable static {table_name} = {{
    "{table_name}",
    {row_count},
    {{
        {rows}
    }}
}};
"""

pd.set_option('display.max_rows', 1000)


def generate_header(file=sys.stdout):
    """Generate the C header from the given spreadsheet."""
    print(HEADER.lstrip())

    data = {}
    for name, df in read_spreadsheet():
        data[name] = df

        rows = ',\n        '.join(
            ROW_FORMAT.format(**dict(row))
            for _, row in df.iterrows()
        )
        table_code = TABLE_FORMAT.format(
            table_name=f'TABLE_{name}',
            rows=rows,
            row_count=len(df)
        )
        print(table_code, file=file)

    print(FOOTER, file=file)
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
    data = generate_header(file=sys.stdout)

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
