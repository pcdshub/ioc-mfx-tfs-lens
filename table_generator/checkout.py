import matplotlib  # isort: skip
import time

try:  # noqa
    matplotlib.use("Qt5Agg")  # noqa
except Exception:  # noqa
    ...  # noqa
import matplotlib.pyplot as plt

import bluesky
import databroker

from bluesky.callbacks import LiveTable
import transfocate
import transfocate.checkout

from config import read_spreadsheet, MIN_RADIUS, MIN_ENERGY


def plot_sweeps():
    """Plot the databroker results from a `sweep_energy_plan`."""
    fig, axes = plt.subplots(
        ncols=2, nrows=2, constrained_layout=True, figsize=(18, 16)
    )
    plot_sweep_energy(0, ax=axes[0, 0], dbi=db[-4])
    plot_sweep_energy(1, ax=axes[0, 1], dbi=db[-3])
    plot_sweep_energy(2, ax=axes[1, 0], dbi=db[-2])
    plot_sweep_energy(3, ax=axes[1, 1], dbi=db[-1])
    fig.tight_layout()

    fn = "summary"
    plt.savefig(f"{fn}.png")
    plt.savefig(f"{fn}.pdf")


def plot_sweep_energy(xrt_lens, dbi, ax=None):
    """Plot the databroker results from a `sweep_energy_plan`."""
    df = dbi.table()
    df = df.set_index(df.energy)

    if ax is None:
        _, ax = plt.subplots(constrained_layout=True, figsize=(12, 10))

    plot_spreadsheet_data(xrt_lens, ax=ax, df=lens_to_spreadsheet_df[xrt_lens])

    ax.set_yscale("log")

    df = df.copy()
    # **NOTE** for the purposes of plotting in log scale, set tfs_radius = 1
    # when zero in actuality
    df.loc[df.tfs_radius == 0.0, "tfs_radius"] = 1.0

    ax.scatter(
        df.energy, df.trip_high, label="Trip high [PLC]", color="black", marker="v"
    )
    ax.scatter(
        df.energy, df.trip_low, label="Trip low [PLC]", color="black", marker="^"
    )

    if False:
        when_faulted = df.where(df.faulted == 1).dropna()
        ax.scatter(
            when_faulted.index,
            when_faulted.tfs_radius,
            label="Scan point - fault",
            color="red",
            marker="x",
        )
    else:
        when_faulted = df.where(df.min_fault == 1).dropna()
        ax.scatter(
            when_faulted.index,
            when_faulted.tfs_radius,
            label="Scan point - min energy fault",
            color="red",
            marker="x",
        )

        when_faulted = df.where(df.lens_required_fault == 1).dropna()
        ax.scatter(
            when_faulted.index,
            when_faulted.tfs_radius,
            label="Scan point - lens required",
            color="red",
            marker="D",
        )

        when_faulted = df.where(df.table_fault == 1).dropna()
        ax.scatter(
            when_faulted.index,
            when_faulted.tfs_radius,
            label="Scan point - table fault",
            color="red",
            marker="+",
        )

    when_not_faulted = df.where(df.faulted == 0).dropna()
    ax.scatter(
        when_not_faulted.index,
        when_not_faulted.tfs_radius,
        color="black",
        marker=".",
        s=3,
        label="Scan point - no fault",
    )

    ax.set_ylim(1, 1e4)

    ax.legend(loc="upper right")
    xrt_radius, *_ = list(df.xrt_radius)
    if xrt_radius == 0.0:
        ax.set_title("No pre-focusing lens")
    else:
        ax.set_title(f"Pre-focusing radius = {xrt_radius:.2f}um (Lens #{xrt_lens})")
    return xrt_radius


def plot_spreadsheet_data(xrt_lens, ax, df):
    ax.fill_between(
        df.energy,
        df.trip_min,
        df.trip_max,
        where=(df.trip_max > df.trip_min),
        interpolate=True,
        color="red",
        alpha=0.2,
        hatch="/",
    )

    ax.plot(df.energy, df.trip_min, lw=1, color="black", label="")
    ax.plot(df.energy, df.trip_max, lw=1, color="black", label="")

    min_energy = MIN_ENERGY[xrt_lens]
    if min_energy > 0.0:
        ax.fill(
            (0, 0, min_energy, min_energy),
            (0, 1e4, 1e4, 0),
            color="red",
            edgecolor="None",
            alpha=0.2,
            hatch="\\",
        )

    ax.set_yscale("log")
    ax.set_ylabel("Reff [um]")
    ax.set_xlabel("Energy [eV]")
    return df


def sweep_and_plot_xrt(xrt_lens, num_steps=100):
    RE(
        transfocate.checkout.sweep_energy_plan(
            tfs, checkout, xrt_lens, num_steps=num_steps
        ),
        LiveTable(fields),
    )

    xrt_radius = plot_sweep_energy(xrt_lens, db[-1])
    fn = f"pre_focus_{xrt_radius:.0f}um_lens_{xrt_lens}"
    plt.savefig(f"{fn}.png")
    plt.savefig(f"{fn}.pdf")
    df = db[-1].table()[fields]
    df.to_excel(f"{fn}.xlsx")


def sweep_and_plot_xrt_all(num_steps):
    for lens_idx in [0, 1, 2, 3]:
        sweep_and_plot_xrt(lens_idx, num_steps=num_steps)

    plot_sweeps()


if __name__ == "__main__":
    plt.ion()
    tfs = transfocate.Transfocator("MFX:LENS", name="tfs")
    checkout = transfocate.checkout.LensInterlockCheckout("MFX:LENS", name="checkout")
    db = databroker.Broker.named("temp")
    RE = bluesky.RunEngine({})
    RE.subscribe(db.insert)
    tfs.interlock.limits.low.name = "trip_low"
    tfs.interlock.limits.high.name = "trip_high"
    tfs.interlock.faulted.name = "faulted"
    tfs.interlock.state_fault.name = "state_fault"
    tfs.interlock.violated_fault.name = "violated"
    tfs.interlock.min_fault.name = "min_fault"
    tfs.interlock.lens_required_fault.name = "lens_required_fault"
    tfs.interlock.table_fault.name = "table_fault"
    checkout.energy.name = "energy"
    tfs.tfs_radius.name = "tfs_radius"
    tfs.xrt_radius.name = "xrt_radius"

    spreadsheet_data = dict(read_spreadsheet())
    lens_to_spreadsheet_df = {
        0: spreadsheet_data["NO_LENS"],
        1: spreadsheet_data["LENS1_750"],
        2: spreadsheet_data["LENS2_428"],
        3: spreadsheet_data["LENS3_333"],
    }

    fields = [
        "energy",
        "trip_low",
        "trip_high",
        "faulted",
        "state_fault",
        "violated",
        "min_fault",
        "lens_required_fault",
        "table_fault",
        "tfs_radius",
        "xrt_radius",
    ]

    with open("README.md", "rt") as f:
        print(f.read())

    print("Connecting to devices...")

    time.sleep(2)
    tfs.wait_for_connection(timeout=5.0)
    checkout.wait_for_connection(timeout=5.0)
