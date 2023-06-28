# Instruction

## Install

```console
python3 -m pip install .
```

## Dev Install

```console
python3 -m pip install --editable .
```

## Help Page

```sh
radig --help
```

## CSV Format

Options:

- title
- color
- bold: linewidth

> bold is optional, default linewidth: 1.5

### Example File

```csv
# title: "Antenna 1", color: "#FF0000", bold: "3"
angles,dbm
0,-10
45,-12
90,-3
135,-6
180,-20
225,-34
270,-2
315,-32
360,-45
# title: "Antenna 2", color: "#00FF00"
angles,dbm
0,-10
45,-12
90,-3
135,-6
180,-20
225,-34
270,-2
315,-32
360,-45
```
