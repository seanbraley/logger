#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from sklearn.cluster import MiniBatchKMeans
from sklearn import preprocessing
import numpy as np
from scipy import stats
from io import BytesIO
import os
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak, Paragraph,  TableStyle, Table, PageBreak, Image, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1

from graphs import PlotManyChart


def full_header_l(canvas, doc):
    canvas.saveState()
    canvas.setPageSize(landscape(letter))
    canvas.restoreState()

lm = 0.75*inch

f_1 = Frame(lm, .75*inch, 9.5*inch, 7*inch)
full_header_landscape_page = PageTemplate(
    id='landscape_frame',
    frames=[f_1,],
    onPage=full_header_l,
)


class PDFWrapper(object):
    def __init__(self, buffer, pagesize):
        self.buffer=buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def generate_pdf(self, input_data, times, max_y, filename='PDFOutput2.pdf'):
        buffer = self.buffer

        doc = BaseDocTemplate(buffer, showBoundary=1, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.25*inch, bottomMargin=0.25*inch)
        width, height = letter
        doc.title = 'CISC425 Output Graph'
        doc.subject = 'Output Graph'
        doc.author = 'Sean Braley'
        doc.creator = 'Sean Braley'

        doc_elements = []

        # Fonts
        pdfmetrics.registerFont(TTFont('Arial', os.path.join('fonts', 'arial.ttf')))
        pdfmetrics.registerFont(TTFont('Arial_I', os.path.join('fonts', 'ariali.ttf')))
        pdfmetrics.registerFont(TTFont('Arial_B', os.path.join('fonts', 'arialbd.ttf')))

        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Title_1_C", fontSize=14, fontName="Arial_B", alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="Regular", fontSize=11, fontName="Arial"))
        styles.add(ParagraphStyle(name="Regular_2", fontSize=8, fontName="Arial", leading=8))
        styles.add(ParagraphStyle(name="Regular_I", fontSize=11, fontName="Arial_I", alignment=TA_CENTER))

        doc.addPageTemplates([full_header_landscape_page,])

        doc_elements.append(NextPageTemplate(['landscape_frame']))

        text_1 = Paragraph("Output Graph", styles['Title_1_C'])

        doc_elements.append(text_1)
        doc_elements.append(Spacer(.25*inch, .25*inch))

        graph = PlotManyChart()
        graph.chart.valueAxis.valueMax = max_y

        graph.chart.data = input_data
        doc_elements.append(graph)

        doc.build(doc_elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf


def run_with_n(clusters=25, certainty=50):
    min_max_scaler = preprocessing.MinMaxScaler()
    kmeans_obj = MiniBatchKMeans(n_clusters=clusters, random_state=abs(hash("Applejuice")) % (10 ** 8))

    output = []
    prev = 0
    with open("real_data.txt", "rb") as infile:
        tmp = []
        for i, line in enumerate(infile):
            item = line.strip().split(',')
            print i, len(item)
            timestamp = item[0]
            fapp = item[-1]
            item[-1] = abs(hash(fapp)) % (10 ** 8)
            # tmp.append(min_max_scaler.fit_transform(np.array([float(x) for x in item[1:]])))
            if len(item) is 28:
                tmp.append(np.array([float(x) for x in item[1:]]))
            if i is 100:
                min_max_scaler.fit(np.array(tmp))
            elif i % 100 is 0 and i is not 0:
                # fit kmeans
                squashed = min_max_scaler.transform(tmp)
                kmeans_obj.partial_fit(squashed)
                a = kmeans_obj.predict(squashed)
                mode, num = stats.mode(a)
                if num[0] >= certainty:
                    # print mode, num
                    output.append(mode[0])
                    prev = mode[0]
                else:
                    output.append(prev)
                tmp = []
    return output

buf = BytesIO()
report = PDFWrapper(buf, 'Letter')
pdf = report.generate_pdf(
    [
        run_with_n(14, 90),
        # run_with_n(20, 75),
        # run_with_n(20, 85),
        # run_with_n(35, 50),
        # run_with_n(50, 50),
        # run_with_n(25, 75),
        # run_with_n(35, 75),
        # run_with_n(50, 75),
    ],
    [],
    15,
)
with open("output.pdf", "wb") as f:
    f.write(pdf)