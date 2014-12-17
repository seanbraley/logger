#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.charts.linecharts import HorizontalLineChart



class PlotManyChart(_DrawingEditorMixin, Drawing):
    def __init__(self, width=8*inch, height=6*inch, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self._add(self, HorizontalLineChart(), name='chart', validate=None, desc="The main chart")
        self.chart.width = width
        self.chart.height = height
        self.chart.y = -.1*inch
        self.chart.valueAxis.valueMin = 0
        self.chart.x = .7*inch
        self.chart.valueAxis.valueStep = 5
        self.chart.valueAxis.gridStrokeDashArray = (0, 1, 0)
        self.chart.valueAxis.visibleGrid = True
        self.chart.categoryAxis.labels.dx = 0
        self.chart.categoryAxis.labels.dy = -1
        self.chart.lines[0].strokeColor = colors.red
        self.chart.lines.strokeWidth = 1.5
