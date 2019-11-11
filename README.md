# bmClickPlot
Python module to create a plot that can be clicked to select individual data or click-and-dragged to select a range.

## cloning the repository

to clone the repo use:
```bash
git clone https://github.com/BenjaminMummery/bmClickPlot.git
```
This will create a directory called `bmClickPlot` and clone the repository into it.

## Example usage:

```py
import bmClickPlot

x = range(1000)
y = [v*v for v in x]

coords, ranges = bmClickPlot.plot(x, y)

print(coords)
print(ranges)
```