import datetime
import numpy as np
import pandas as pd
from reportlab import platypus
from reportlab.lib import colors, pagesizes, units
from reportlab.lib.styles import getSampleStyleSheet


def to_paragraph(text):
    return text.replace("\n", "<br/>")


table_fields = {
    "energy": {"precision": 2, "label": "Energy\n[eV]"},
    "trip_low": {"precision": 2, "label": "Trip low\n[um]"},
    "tfs_radius": {"precision": 2, "label": "TFS Radius\n[um]"},
    # "xrt_radius": {"precision": 2, "label": "XRT Radius [um]"},
    "trip_high": {"precision": 2, "label": "Trip high\n[um]"},
    "faulted": {"label": "Faulted"},
    "state_fault": {"label": "State\nFault"},
    # "violated": {"label": "Violated"},
    "min_fault": {"label": "Min Energy\nFault"},
    "lens_required_fault": {"label": "Lens Required\nFault"},
    "table_fault": {"label": "Table\nFault"},
}


HEADER = f"""

Report generated: {datetime.datetime.now()}

The next 4 sections describe individual scans, without a pre-focus lens and \
then one per pre-focus lens.
"""

SCAN_INFO = """
1. Choose a few transfocator lens sets to span the effective radius range.
2. For each of those lens sets, scan energy at regular intervals.
3. Each marker on the plot represents one of those scan points.
4. Record if PLC reported a fault and why.
"""


PLOT_INFO = """
<b>No fault</b> indicates that a data point was checked but no fault reported by PLC.
<b>Trip Low</b> and <b>Trip High</b> are values from the spreadsheet table, \
interpolated by the PLC and reported to EPICS.
The lines drawn around these regions and the highlighted regions are directly \
from the spreadsheet.
<b>Min Energy Fault</b> indicates that it does not meet minimum energy \
requirement for a given XRT lens.
<b>Table Fault</b> indicates a fault from the spreadsheet table disallowed \
region.
<b>Lens Required Fault</b> markers are clipped at the bottom of the plot.
"""

results = {
    "pre_focus_0um_lens_0": {
        "title": "No pre-focusing lens",
        "info": """bluesky scan sweep_energy_plan performed without a pre-focus lens.""",
    },
    "pre_focus_750um_lens_1": {
        "title": "750.000µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan with 750.000µm pre-focusing lens..",
    },
    "pre_focus_429um_lens_2": {
        "title": "428.571µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan with 428.571µm pre-focusing lens.",
    },
    "pre_focus_333um_lens_3": {
        "title": "333.333µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan with 333.333µm pre-focusing lens.",
    },
}

stylesheet = getSampleStyleSheet()
builder = [
    platypus.Paragraph("Report document", stylesheet["Heading1"]),
    platypus.Paragraph(to_paragraph(HEADER), stylesheet["Normal"]),
]


for scan_prefix, scan_info in results.items():
    df = pd.read_excel(f"{scan_prefix}.xlsx", engine="openpyxl")
    df = df[list(table_fields)]

    for attr, col_info in table_fields.items():
        precision = col_info.get("precision")
        if precision is not None:
            col = getattr(df, attr)
            setattr(df, attr, [f"%.{precision}f" % item for item in col])

    style = platypus.TableStyle(
        [
            ("FACE", (0, 0), (-1, 0), "Times-Bold"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]
    )

    header = [col_info.get("label", attr) for attr, col_info in table_fields.items()]
    table = platypus.Table([header] + np.array(df).tolist(), repeatRows=1)
    table.setStyle(style)
    plot = platypus.Image(f"{scan_prefix}.png")
    plot.drawWidth = 8.0 * units.inch
    plot.drawHeight = 6.67 * units.inch
    builder.extend(
        [
            platypus.Paragraph(scan_info["title"], stylesheet["Heading1"]),
            platypus.Paragraph(to_paragraph(scan_info["info"]), stylesheet["Normal"]),
            platypus.Paragraph("Scan Information", stylesheet["Heading2"]),
            platypus.Paragraph(to_paragraph(SCAN_INFO), stylesheet["Normal"]),
            platypus.Spacer(0 * units.inch, 0.5 * units.inch),
            plot,
            platypus.Paragraph("Plot / Table Information", stylesheet["Heading2"]),
            platypus.Paragraph(to_paragraph(PLOT_INFO), stylesheet["Normal"]),
            platypus.PageBreakIfNotEmpty(),
            table,
            platypus.PageBreakIfNotEmpty(),
        ]
    )

doc = platypus.SimpleDocTemplate("report.pdf", pagesize=pagesizes.letter)
doc.build(builder)
