import os
from collections import defaultdict
from typing import List, Tuple

import click
import numpy
import pandas
import seaborn
from matplotlib import pyplot
from collections import Counter

seaborn.set_palette("colorblind")
pyplot.rcParams['font.size'] = 18

# define label name and color when plotting
method_dict = {
    "espaloma-0.3": ["espaloma-0.3", "red"], 
    #"espaloma-0.3.0-rc1": ["espaloma-0.3-rc1", "orange"], 
    "openff-2.0.0": ["openff-2.0.0", "purple"], 
    "openff-2.1.0": ["openff-2.1.0", "tab:blue"],
    "gaff-2.11": ["gaff-2.11", "tab:green"], 
    }

def draw_step_plot(
    plot_data: List[numpy.ndarray],
    method_dict: dict,
    metric: str,
    x_range: Tuple[float, float],
    output_path: str,
    n_bins: int = 16,
    bootstrap_iterations: int = 1000,
    percentile=0.95,
):
    """Draw a step plot of data segregated by each method.

    Parameters
    ----------
    plot_data
        A list of the arrays where ``plot_data[i]`` contains the particular metric of
        interest associated with ``method_labels[i]``.
    method_dict
        The label name and color code associated with each data series.
    metric
        The metric contained in the ``plot_data``.
    x_range
        A tuple of the min and max values to use for the x axis.
    output_path
        The path to save the final plot to.
    n_bins
        The number of bins to split the data into.
    bootstrap_iterations
        The number of bootstrap iterations to perform when computing the error bars.
    percentile
        The percentile of the confidence interval to display.
    """

    method_labels = [ value[0] for value in method_dict.values() ]
    method_colors = [ value[1] for value in method_dict.values() ]

    sample_count = min(map(len, plot_data))
    sample_densities = {
        method: numpy.zeros((bootstrap_iterations, n_bins)) for method in method_labels
    }

    if x_range is None:
        x_range = (
            min(numpy.nanmin(data) for data in plot_data),
            max(numpy.nanmax(data) for data in plot_data),
        )

    for sample_index in range(bootstrap_iterations):

        samples_indices = numpy.random.randint(
            low=0, high=sample_count, size=sample_count
        )

        for method, method_data in zip(method_labels, plot_data):

            #print(method, len(method_data))
            sample_data = method_data[samples_indices]
            sample_density, _ = numpy.histogram(
                sample_data, bins=n_bins, range=x_range, density=False
            )

            sample_densities[method][sample_index] = sample_density

    lower_percentile_index = int(bootstrap_iterations * (1 - percentile) / 2)
    upper_percentile_index = int(bootstrap_iterations * (1 + percentile) / 2)

    confidence_intervals = {}

    error_bar_x_values = {}
    error_bar_y_values = {}

    for method, method_data in zip(method_labels, plot_data):

        sorted_samples = numpy.sort(sample_densities[method], axis=0)

        confidence_intervals[method] = (
            sorted_samples[lower_percentile_index],
            sorted_samples[upper_percentile_index],
        )

        error_bar_x_values[method] = (
            numpy.arange(n_bins) / n_bins * (x_range[1] - x_range[0])
        ) + x_range[0]
        error_bar_y_values[method], _ = numpy.histogram(
            method_data, bins=n_bins, range=x_range, density=False
        )

    plot_frame = pandas.DataFrame(
        [
            {"method": method_label, metric: data_point}
            for data_series, method_label in zip(plot_data, method_labels)
            for data_point in data_series
        ]
    )
    
    plot = seaborn.displot(
        data=plot_frame,
        x=metric,
        hue="method",
        kind="hist",
        stat="count",
        bins=n_bins,
        binrange=x_range,
        element="step",
        fill=False,
        aspect=2.5,
        height=3,
        lw=1.25,
        facet_kws={"legend_out": False},
        palette=seaborn.color_palette(method_colors)
        )

    for i, method in enumerate(method_labels):

        x_offset = (x_range[1] - x_range[0]) / n_bins / len(method_labels) * (i + 0.5)

        pyplot.errorbar(
            error_bar_x_values[method] + x_offset,
            error_bar_y_values[method],
            yerr=numpy.array(
                [
                    numpy.abs(
                        confidence_intervals[method][0] - error_bar_y_values[method]
                    ),
                    numpy.abs(
                        confidence_intervals[method][1] - error_bar_y_values[method]
                    ),
                ]
            ),
            marker=None,
            linestyle="none",
        )

    # Remove the legend title.
    plot.legend.set_title(None)

    # Draw a vertical line at x=0 for visual reference
    pyplot.axvline(x=0.0, lw=1.5, ls="--", color="gray", clip_on=False)

    pyplot.gcf().set_size_inches(7, 3)

    # adjust font sizes
    pyplot.xlabel(metric)
    pyplot.ylabel("Density")

    # save with transparency for overlapping plots
    pyplot.savefig(output_path, dpi=2400, transparent=True, bbox_inches="tight")
    pyplot.close("all")


def draw_ddE_histogram_in_ranges(
    plot_data: List[numpy.ndarray],
    method_dict: dict,
    metric: str,
    output_path: str,
):
    """Draw bar plot with ddE in bins of ranges of deltaE.

    Parameters
    ----------
    plot_data
        A list of the arrays where ``plot_data[i]`` contains the particular metric of
        interest associated with ``method_labels[i]``.
    method_dict
        The label name and color code associated with each data series.
    metric
        The metric contained in the ``plot_data``.
    output_path
        The path to save the final plot to.
    """
    method_labels = [ value[0] for value in method_dict.values() ]
    method_colors = [ value[1] for value in method_dict.values() ]

    bins = numpy.array([-150, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 100])
    bin_inds = {}
    for i in range(len(method_labels)):
        bin_inds[i] = numpy.digitize(plot_data[i], bins)
    counts = {}
    for i in range(len(method_labels)):
        counts[i] = Counter(bin_inds[i])
    fig = pyplot.figure(figsize=(10,6))
    width=0.15
    x = [1,2,3,4,5]
    mid = int(len(bins)/2)
    y = {}
    for i in range(len(method_labels)):
        y[i] = [counts[i][mid], counts[i][mid-1]+counts[i][mid+1], counts[i][mid-2]+counts[i][mid+2], counts[i][mid-3]+counts[i][mid+3], counts[i][mid-4]+counts[i][mid+4]]
        y[i] = [t/(sum(counts[i].values()) - counts[i][len(bins)]) for t in y[i]]
        xw = [t+(i-1)*width for t in x]
        pyplot.bar(xw, y[i], width=width, alpha=0.6, label=method_labels[i], color=method_colors[i])
    pyplot.xlabel("ddE (kcal/mol) in ranges of [-1, 1], \n [-2, -1] & [1, 2], \n [-3, -2] & [2, 3], ...")
    pyplot.ylabel("Densities")
    pyplot.legend()
    # save with transparency for overlapping plots
    pyplot.savefig(output_path, dpi=2400, transparent=True, bbox_inches="tight")
    pyplot.close("all")


def draw_box_plot(
    plot_data: List[numpy.ndarray],
    method_dict: dict,
    metric: str,
    y_range: Tuple[float, float],
    output_path: str,
):
    """Draw a violin plot of data segregated by each method.

    Parameters
    ----------
    plot_data
        A list of the arrays where ``plot_data[i]`` contains the particular metric of
        interest associated with ``method_labels[i]``.
    method_dict
        The label name and color code associated with each data series.
    metric
        The metric contained in the ``plot_data``.
    output_path
        The path to save the final plot to.
    """

    method_labels = [ value[0] for value in method_dict.values() ]
    method_colors = [ value[1] for value in method_dict.values() ]

    plot_frame = pandas.DataFrame(
        [
            {"method": method_label, metric: data_point}
            for data_series, method_label in zip(plot_data, method_labels)
            for data_point in data_series
        ]
    )

    #seaborn.catplot(data=plot_frame, x="method", y=metric, kind="box", dodge=False)
    seaborn.catplot(data=plot_frame, x="method", y=metric, kind="box", dodge=False, palette=seaborn.color_palette(method_colors))

    pyplot.xticks(rotation=45, ha='right', rotation_mode='anchor')

    if y_range is not None:
        pyplot.ylim(y_range)

    pyplot.xlabel("Force Field")
    pyplot.ylabel(metric)
    #pyplot.xticks(fontsize=18)
    #pyplot.yticks(fontsize=18)

    # save with transparency for overlapping plots
    pyplot.savefig(output_path, dpi=2400, transparent=True, bbox_inches="tight")
    pyplot.close("all")


def draw_plots(energies, rmsds, tfds, method_dict, output_directory):
    """Draw step and violin plots of a set of ddE, RMSD, and TFD metrics."""

    os.makedirs(output_directory, exist_ok=True)

    draw_box_plot(
        energies,
        method_dict,
        metric="ddE (kcal/mol)",
        y_range=(-15.0, 15.0),
        output_path=os.path.join(output_directory, "box-dde.svg"),
    )
    draw_step_plot(
        energies,
        method_dict,
        metric="ddE (kcal/mol)",
        x_range=(-15.0, 15.0),
        output_path=os.path.join(output_directory, "step-dde.svg"),
    )
    draw_ddE_histogram_in_ranges(
        energies,
        method_dict,
        metric="ddE (kcal/mol)",
        output_path=os.path.join(output_directory, "dde-in-ranges.svg"),
    )

    for key, values in rmsds.items():
        metric = fr"{key} ($\mathrm{{\AA}}$)"
        if key in ["Angle RMSD", "Dihedral RMSD", "Proper RMSD", "Improper RMSD"]:
            metric = fr"{key} ($\mathrm{{degrees}}$)"

        draw_box_plot(
            values,
            method_dict,
            metric=metric,
            y_range=(0, 3) if key == "RMSD" else None,
            output_path=os.path.join(
                output_directory, f"box-{key.lower().replace(' ', '_')}.svg"
            ),
        )
        draw_step_plot(
            values,
            method_dict,
            metric=metric,
            x_range=(0, 3) if key == "RMSD" else None,
            output_path=os.path.join(
                output_directory, f"step-{key.lower().replace(' ', '_')}.svg"
            ),
        )

    draw_box_plot(
        tfds,
        method_dict,
        metric="TFD",
        y_range=(0, 0.5),
        output_path=os.path.join(output_directory, "box-tfd.svg"),
    )
    draw_step_plot(
        tfds,
        method_dict,
        metric="TFD",
        x_range=(0, 0.5),
        output_path=os.path.join(output_directory, "step-tfd.svg"),
    )


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), default="03-metrics.csv")
def main(input_path):
    print("Plotting full metrics")

    metrics_frame = pandas.read_csv(input_path)
    #method_labels = sorted(metrics_frame["Force Field"].unique(), reverse=True)
    method_keynames = list(method_dict.keys())
    metrics = []

    #for method_label in method_labels:
    for method_keyname in method_keynames:
        method_frame = metrics_frame[metrics_frame["Force Field"] == method_keyname]
        metrics.append(
            (
                method_frame["SMILES"].values,
                method_frame["ddE"].values,
                method_frame["TFD"].values,
                method_frame["RMSD"].values,
                method_frame["FB OBJECTIVE"].values,
                method_frame["Bond RMSD"].values,
                method_frame["Angle RMSD"].values,
                method_frame["Dihedral RMSD"].values,
                method_frame["Improper RMSD"].values,
            )
        )

    # Plot the full statistics
    (
        smiles,
        energies,
        tfds,
        full_rmsds,
        fb_objectives,
        bond_rmsds,
        angle_rmsds,
        proper_rmsds,
        improper_rmsds,
    ) = zip(*metrics)

    draw_plots(
        energies,
        {
            "RMSD": full_rmsds,
            "Bond RMSD": bond_rmsds,
            "Angle RMSD": angle_rmsds,
            "Proper RMSD": proper_rmsds,
            "Improper RMSD": improper_rmsds,
            "FB OBJECTIVE" : fb_objectives, 
        },
        tfds,
        method_dict,
        os.path.join("04-outputs"),
    )


if __name__ == "__main__":
    main()
