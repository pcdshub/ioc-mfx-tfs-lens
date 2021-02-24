import matplotlib  # isort: skip

try:  # noqa
    matplotlib.use('Qt5Agg')  # noqa
except Exception:  # noqa
    ...  # noqa
import matplotlib.pyplot as plt

import bluesky
import databroker

from bluesky.callbacks import LiveTable
import transfocate
import transfocate.checkout

from config import read_spreadsheet


def plot_sweep_energy(xrt_lens, dbi):
    """Plot the databroker results from a `sweep_energy_plan`."""
    df = dbi.table()
    df = df.set_index(df.energy)

    fig, ax = plt.subplots(constrained_layout=True, figsize=(12, 10))
    plot_spreadsheet_data(ax=ax, df=lens_to_spreadsheet_df[xrt_lens])

    ax.set_yscale('log')

    ax.scatter(df.energy, df.trip_high, label='Trip high', color='black', marker='v')
    ax.scatter(df.energy, df.trip_low, label='Trip low', color='black', marker='^')
    
    when_faulted = df.where(df.faulted == 1).dropna()
    ax.scatter(when_faulted.index, when_faulted.tfs_radius, color='red', marker='x')
    
    ax.set_ylim(1, 1e4)
    
    xrt_radius, *_ = list(df.xrt_radius)
    ax.set_title(f'xrt_radius = {xrt_radius:.2f} (idx={xrt_lens})')
    return xrt_radius, fig


def plot_spreadsheet_data(ax, df):
    ax.fill_between(
        df.energy, df.trip_min, df.trip_max,
        where=(df.trip_max > df.trip_min),
        interpolate=True,
        color='red',
        alpha=0.2,
        hatch='/',
    )

    df.trip_min.plot(ax=ax, lw=1, color='black')
    df.trip_max.plot(ax=ax, lw=1, color='black')

    ax.legend(loc='best')
    ax.set_yscale('log')
    ax.set_ylabel('Reff')
    ax.set_xlabel('Energy [eV]')
    return df


def sweep_and_plot_xrt(xrt_lens, num_steps=150):
    RE(transfocate.checkout.sweep_energy_plan(tfs, checkout, xrt_lens, num_steps=num_steps), LiveTable(fields))
    xrt_radius, _ = plot_sweep_energy(xrt_lens, db[-1])
    plt.savefig(f"xrt_lens_{xrt_lens}_{xrt_radius:.0f}um.png")


if __name__ == "__main__":
    plt.ion()
    tfs = transfocate.Transfocator("MFX:LENS", name="tfs")
    checkout = transfocate.checkout.LensInterlockCheckout("MFX:LENS", name="checkout")
    db = databroker.Broker.named('temp')
    RE = bluesky.RunEngine({})
    RE.subscribe(db.insert)
    tfs.interlock.limits.low.name = 'trip_low'
    tfs.interlock.limits.high.name = 'trip_high'
    tfs.interlock.faulted.name = 'faulted'
    tfs.interlock.state_fault.name = 'state_fault'
    tfs.interlock.violated_fault.name = 'violated'
    tfs.interlock.min_fault.name = 'min_fault'
    tfs.interlock.lens_required_fault.name = 'lens_required_fault'
    tfs.interlock.table_fault.name = 'table_fault'
    checkout.energy.name = 'energy'
    tfs.tfs_radius.name = 'tfs_radius'
    tfs.xrt_radius.name = 'xrt_radius'

    spreadsheet_data = dict(read_spreadsheet())
    lens_to_spreadsheet_df = {
        0: spreadsheet_data["NO_LENS"],
        1: spreadsheet_data["LENS1_750"],
        2: spreadsheet_data["LENS2_428"],
        3: spreadsheet_data["LENS3_333"],
    }

    fields = [
        'energy',

        'trip_low',
        'trip_high',

        'faulted',
        'state_fault',
        'violated',
        'min_fault',
        'lens_required_fault',
        'table_fault',

        'tfs_radius',
        'xrt_radius',
    ]
    tfs.wait_for_connection()
    checkout.wait_for_connection()
