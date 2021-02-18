#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "interlockTables.h"


/* For each table, dump interpolated data to csv files. */
void dump_tables() {
    RangeRow value;

	const RangeTable *tables[] = {
		&TABLE_NO_LENS, &TABLE_LENS3_333, &TABLE_LENS2_428, &TABLE_LENS1_750
	};

	const char *table_name;

	for (int table_idx=0; table_idx < 4; table_idx++) {
		table_name = tables[table_idx]->table_name;
		FILE *fp = fopen(table_name, "wt");
		if (!fp) {
			fprintf(stderr, "Failed to open %s\n", table_name);
			continue;
		}
		fprintf(fp, "energy,low,high\n");
		for (double energy=0.0; energy < 40000.0; energy += 1.0) {
			if (find_limits(&value, tables[table_idx], energy)) {
				print_row(fp, value, true);
			}
		}
		fclose(fp);
	}
}

int main(void) {
	dump_tables();
	return 0;
}
