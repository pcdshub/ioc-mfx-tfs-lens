import sys
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')  # noqa

import matplotlib.pyplot as plt  # noqa


# Configuration for reading the spreadsheet:
EXCEL_SHEET = 'Results'
ROW_START = 16
REGIONS = {
    'NO_LENS': {'usecols': 'B:D'},
    'LENS3_333': {'usecols': 'F:H'},
    'LENS2_428': {'usecols': 'J:L'},
    'LENS1_750': {'usecols': 'N:P'},
}

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

# Lens information
# Radii in micron:
xrt_lenses_radii = [750.0, 428.6, 333.3]
tfs_lens_radii = [
    # 0.0,
    500.0,
    300.0,
    250.0,
    200.0,
    125.0,
    62.5,
    50.0,
    50.0,
    50.0,
]


# Min effective radius is when all lenses are inserted:
MIN_RADIUS = 1 / sum(1 / radius for radius in tfs_lens_radii)
# Max radius is when the largest is inserted:
MAX_RADIUS = max(tfs_lens_radii)
# print("Min radius", MIN_RADIUS)
# print("Max radius", MAX_RADIUS)

# In these ranges, a transfocator lens MUST be inserted
REQUIRES_LENS_RANGE = {
    "no_prefocus": None,
    "xrt_lens3": (9.50, 11.11),
    "xrt_lens2": (8.28, 10.02),
    "xrt_lens1": (5.96, 8.02),
}

pd.set_option('display.max_rows', 1000)


def generate_header(spreadsheet, *, file=sys.stdout):
    """Generate the C header from the given spreadsheet."""
    print(HEADER.lstrip())

    data = {}
    for name, read_kw in REGIONS.items():
        df = pd.read_excel(
            spreadsheet,
            engine='openpyxl',
            sheet_name=EXCEL_SHEET,
            skiprows=ROW_START - 1,
            header=None,
            **read_kw
        )
        df.columns = ['energy', 'trip_min', 'trip_max']
        df.energy *= 1e3  # keV -> eV
        df = df.dropna()
        df = df.set_index(df.energy)
        df.loc[df.trip_max > 1e4, 'trip_max'] = 1e4
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
    data = generate_header('MFX_EnergyLensInterlock_Tables_Transposed.xlsx',
                           file=sys.stdout)

    _, axes = plt.subplots(ncols=2, nrows=2, constrained_layout=True,
                           dpi=120, figsize=(11, 8))
    # plt.ion()
    keys = list(REGIONS)
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
