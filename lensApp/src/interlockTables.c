#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "interlockTables.h"


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
void print_row(FILE *fp, const RangeRow row, bool newline) {
	if (!fp) {
		return;
	}
    fprintf(fp, "%.6f, %.6f, %.6f", row.energy, row.low, row.high);
	if (newline) {
		fprintf(fp, "\n");
	}
}

/*
 * _binsearch_energy
 *
 *  Binary search on energy from RangeRow.
 *
 * Parameters:
 *  int *_lower_idx
 *      The resulting lower index.
 *  int *_upper_idx
 *      The resulting upper index.
 *  const RangeRow rows[]
 *      Rows from the table.
 *  double find_energy
 *      The energy to search for.
 *
 * Returns: bool
 *      False if arguments were invalid.
 */
bool _binsearch_energy(int *_lower_idx, int *_upper_idx, const RangeRow rows[], double find_energy) {
    if (!_lower_idx || !_upper_idx)
        return false;

    int lower_idx = *_lower_idx;
    int upper_idx = *_upper_idx;
    int middle_idx;

    while (lower_idx < upper_idx) {
        middle_idx = (int)((lower_idx + upper_idx) / 2);
        if (find_energy == rows[lower_idx].energy) {
            upper_idx = lower_idx;
        } else if (find_energy == rows[middle_idx].energy) {
            upper_idx = middle_idx;
            lower_idx = middle_idx;
        } else if (find_energy == rows[upper_idx].energy) {
            lower_idx = upper_idx;
        } else if (find_energy < rows[middle_idx].energy) {
            if (upper_idx == middle_idx) {
                break;
            }
            upper_idx = middle_idx;
        } else {
            if (lower_idx == middle_idx) {
                break;
            }
            lower_idx = middle_idx;
        }
    }
    *_lower_idx = lower_idx;
    *_upper_idx = upper_idx;
    return true;
}


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
bool find_limits(RangeRow *result, const RangeTable *table, double find_energy) {
    if (!result || !table) {
        return false;
    }

    int lower_idx = 0;
    int upper_idx = table->num_rows - 1;
    const RangeRow *rows = table->rows;

	if (find_energy < rows[lower_idx].energy) {
		// For these tables, don't interpolate before data starts.
		return false;
	}

	if (find_energy > rows[upper_idx].energy) {
		// Interpolation beyond the last point works well enough, but let's not
		// assume anything beyond the data we're given.
		return false;
	}

    if (!_binsearch_energy(&lower_idx, &upper_idx, rows, find_energy)) {
        return false;
    }

    double delta_energy = rows[upper_idx].energy - rows[lower_idx].energy;

    if (upper_idx != lower_idx && delta_energy > 0.) {
        result->energy = find_energy;
        double slope = (rows[upper_idx].low - rows[lower_idx].low) / delta_energy;
        result->low = rows[lower_idx].low + slope * (find_energy - rows[lower_idx].energy);

        slope = (rows[upper_idx].high - rows[lower_idx].high) / delta_energy;
        result->high = rows[lower_idx].high + slope * (find_energy - rows[lower_idx].energy);

		if (result->high < result->low) {
			// Bad interpolation past end of region.
			return false;
		}
        return true;
    }

    result->energy = rows[lower_idx].energy;
    result->low = rows[lower_idx].low;
    result->high = rows[lower_idx].high;

    return true;

}
