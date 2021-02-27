import numpy as np
import pandas as pd
from reportlab import platypus
from reportlab.lib import colors, pagesizes, units
from reportlab.lib.styles import getSampleStyleSheet


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


results = {
    "pre_focus_0um_lens_0": {
        "title": "No pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan performed without a pre-focus lens.",
    },
    "pre_focus_750um_lens_1": {
        "title": "750.000µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan.",
    },
    "pre_focus_429um_lens_2": {
        "title": "428.571µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan.",
    },
    "pre_focus_333um_lens_3": {
        "title": "333.333µm pre-focusing lens",
        "info": "bluesky scan sweep_energy_plan.",
    },
}

stylesheet = getSampleStyleSheet()
builder = []

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
    # builder.append()
    # Story = [Spacer(1,2*inch)]
    # style = styles["Normal"]
    # for i in range(100):
    #     bogustext = ("This is Paragraph number %s.  " % i) *20
    #     p = Paragraph(bogustext, style)
    #     Story.append(p)
    #     Story.append(Spacer(1,0.2*inch))
    plot = platypus.Image(f"{scan_prefix}.png")
    plot.drawWidth = 8.0 * units.inch
    plot.drawHeight = 6.67 * units.inch
    builder.extend(
        [
            platypus.Paragraph(scan_info["title"], stylesheet["title"]),
            platypus.Paragraph(scan_info["info"], stylesheet["Normal"]),
            platypus.Spacer(0 * units.inch, 0.5 * units.inch),
            plot,
            platypus.PageBreakIfNotEmpty(),
            table,
            platypus.PageBreakIfNotEmpty(),
        ]
    )

doc = platypus.SimpleDocTemplate("report.pdf", pagesize=pagesizes.letter)
doc.build(builder)
