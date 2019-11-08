# bmClickPlot
Python module to create a plot that can be clicked to select individual data or click-and-dragged to select a range.

Example usage:
```python
import bmClickPlot

x = range(1000)
y = [v*v for v in x]

coords, ranges = bmClickPlot.plot(x, y)

print(coords)
print(ranges)
```