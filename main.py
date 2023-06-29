import math
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import List, Optional

import click
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, read_csv


@dataclass()
class Dataset:
    title: str = ""
    color: str = ""
    bold: Optional[float] = None
    data: str = ""


def parse_metadata(metadata: str):
    title: str = ""
    color: str = ""
    bold: Optional[float] = None

    if metadata[0] == "#":
        metadata = metadata[1:]
    metadata_list = metadata.strip().split(",")

    for meta in metadata_list:
        option, value = meta.split(":")
        option = option.strip()
        value = value.strip()
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]

        if option == "title":
            title = value

        if option == "color":
            color = value

        if option == "bold":
            bold = float(value)

    return title, color, bold


def get_csv_files(
    file: str,
) -> list[Dataset]:
    csv_files: List[Dataset] = []
    index_list = []

    for idx, line in enumerate(file.splitlines()):
        if line[0] == "#":
            index_list.append(idx)

    lines = file.splitlines()

    while len(index_list) > 0:
        dataset: Dataset = Dataset()
        csv_file: list[str] = []

        if len(index_list) == 1:
            csv_file = lines[index_list[0] :]
        else:
            csv_file = lines[index_list[0] : index_list[1]]

        metadata = csv_file[0]
        csv = "\n".join(csv_file[1:])
        title, color, bold = parse_metadata(metadata)

        dataset.title = title
        dataset.color = color
        dataset.data = csv
        dataset.bold = bold

        csv_files.append(dataset)

        index_list.pop(0)
    return csv_files


def plot_graphs(
    csv_list: List[Dataset],
    *,
    title="",
    range_min: Optional[int],
    range_step: Optional[int],
    show: bool,
    output_filename: Path,
):
    fig = plt.figure()
    ax = fig.add_subplot(projection="polar")
    ax.set_title(title)

    data_frame_list: List[DataFrame] = []
    data_dbm_max: float = -120

    for idx, csv in enumerate(csv_list):
        data_frame_list.append(read_csv(StringIO(csv.data), header=0))

        data_dbm_max = max(data_dbm_max, float(data_frame_list[idx]["dbm"].max()))

    for csv, data in zip(csv_list, data_frame_list):
        data["angles"] = data["angles"].apply(lambda x: x * 2 * math.pi / 360)
        data["dbm"] = data["dbm"].apply(lambda x: x - data_dbm_max)

        ax.plot(
            data["angles"],
            data["dbm"],
            color=csv.color,
            label=csv.title,
            linewidth=csv.bold if csv.bold is not None else 1.5,
        )

        ax.legend(
            loc="lower right",
            # loc="best",
            bbox_to_anchor=(1.1, -0.1),
        )

    if range_min is not None and range_step is not None:
        ax.set_yticks(ticks=np.arange(range_min, 0, range_step))

    ax.set_xticks(ticks=np.arange(0, np.radians(360), np.radians(30)))

    if show:
        plt.show()
    else:
        fig.set_size_inches(10, 10)
        fig.set_dpi(600)
        fig.savefig(output_filename)


@click.command(help="Plot for Radiation Diagram.")
@click.argument("filename", type=Path)
@click.option(
    "--title",
    "-t",
    type=str,
    prompt="Title of Plot",
    default="Radiation Diagram",
    show_default=True,
    help="Graph title.",
)
@click.option(
    "--range_min",
    "-m",
    type=int,
    default=None,
    show_default=True,
    help="Min graph Y ticks.",
)
@click.option(
    "--range_step",
    "-s",
    type=int,
    default=None,
    show_default=True,
    help="Graph Y ticks step.",
)
@click.option(
    "--output_filename",
    "-o",
    "output_filename",
    type=Path,
    default=None,
    show_default=True,
    help="Output file name.",
)
@click.option(
    "--show",
    is_flag=True,
    show_default=True,
    help="Shows the graph instead of autosave.",
)
def cli(
    filename: Path,
    *,
    title: str,
    range_min: Optional[int],
    range_step: Optional[int],
    output_filename: Optional[Path],
    show: bool,
):
    file = filename.open(encoding="utf-8")
    file_str = file.read()

    csv_files = get_csv_files(file_str)

    if output_filename is None:
        output_filename = Path.cwd() / filename.with_suffix(".png").name
    plot_graphs(
        csv_files,
        title=title,
        range_min=range_min,
        range_step=range_step,
        show=show,
        output_filename=output_filename,
    )


if __name__ == "__main__":
    cli()
