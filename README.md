# Call of War production planner

A command-line tool that shows when a build order is ready in Call of War: World War 2.

## What it does

You give the tool your resource stock, your income, and a list of units to build. The tool adds the cost of all units. It then finds the resource that you wait for longest. It prints the time when you can start the build and the time when the build ends.

The tool does not connect to the game. It does not read game data and it does not send input to the game.

## Requirements

- Python 3.8 or later. The tool uses only the standard library.
- Any operating system that runs Python.

## Install

1. Clone the repository:

```
git clone https://github.com/Orpheus-21/call-of-war-planner.git
```

2. Go to the folder:

```
cd call-of-war-planner
```

## Usage

Run the tool with a unit file and a plan file:

```
python3 planner.py units.example.json plan.example.json
```

Run the self-check:

```
python3 planner.py --check
```

The self-check prints `ok` when the calculation is correct.

## Configuration

WARNING: The numbers in `units.example.json` are placeholders. They are not the real game values. Copy the file and enter the real values from the game before you trust the output.

The unit file has one entry for each unit. Each entry has these keys:

- `cost`: the resources that one unit costs, as a name and an amount.
- `build_seconds`: the build time of one unit, in seconds.

The plan file has these keys:

- `stock`: the resources that you have now.
- `income_per_hour`: the resources that you gain in one hour.
- `sites`: the number of places that build at the same time.
- `orders`: the unit names and how many of each you want.

## How it works

The code is in the file `planner.py`. The function `plan` does the calculation in four steps:

1. It adds the cost of all ordered units for each resource.
2. It subtracts the stock from the cost. The result is the deficit.
3. It divides the deficit by the income per hour. The result is the wait time for that resource.
4. It adds the build time of all units and divides the sum by `sites`.

The tool assumes that you wait until all resources are enough. Then you start all builds together. The start time is the longest wait time. The end time is the start time plus the build time.

If a resource has a deficit and no income, the tool prints a stop message.

The tool does not model resources that you gain while the units build. The tool does not model a build queue that has different limits in each province.

## License

This project uses the GNU General Public License version 3 or any later version. The file `LICENSE` has the full text.
