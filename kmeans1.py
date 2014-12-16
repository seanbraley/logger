#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np


from graphs import PlotManyChart

from io import BytesIO
import os

from reportlab.lib import pdfencrypt, colors, utils
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak, Paragraph,  TableStyle, Table, PageBreak, Image, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1


def full_header_l(canvas, doc):
    canvas.saveState()
    canvas.setPageSize(landscape(letter))
    canvas.restoreState()

lm=0.75*inch

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

    def generate_pdf(self, input_data, times, filename='PDFOutput2.pdf'):
        buffer = self.buffer

        doc = BaseDocTemplate(buffer, showBoundary=1, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.25*inch, bottomMargin=0.25*inch)
        width, height = letter
        doc.title = 'CISC425 Output Graph'
        doc.subject = 'Output Graph'
        doc.author = 'Sean Braley'
        doc.creator = 'Sean Braley'

        doc_elements = []

        # Fonts
        pdfmetrics.registerFont(TTFont('Calibri_B', os.path.join('fonts', 'calibrib.ttf')))
        pdfmetrics.registerFont(TTFont('Arial', os.path.join('fonts', 'arial.ttf')))
        pdfmetrics.registerFont(TTFont('Arial_I', os.path.join('fonts', 'ariali.ttf')))
        pdfmetrics.registerFont(TTFont('Arial_B', os.path.join('fonts', 'arialbd.ttf')))



        # Styles
        styles = getSampleStyleSheet()
        #styles.add(ParagraphStyle(name="Title_1", fontSize=12, textColor=colors.red, wordWrap='LTR'))
        styles.add(ParagraphStyle(name="Title_1_C", fontSize=14, fontName="Arial_B", alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="Regular", fontSize=11, fontName="Arial"))
        styles.add(ParagraphStyle(name="Regular_2", fontSize=8, fontName="Arial", leading=8))
        styles.add(ParagraphStyle(name="Regular_I", fontSize=11, fontName="Arial_I", alignment=TA_CENTER))


        #doc.addPageTemplates([template_1, template_2, template_3, template_4, template_5, template_6, page_1, page_2])
        doc.addPageTemplates([full_header_landscape_page,])

        doc_elements.append(NextPageTemplate(['landscape_frame']))

        text_1 = Paragraph("Output Graph", styles['Title_1_C'])

        doc_elements.append(text_1)
        doc_elements.append(Spacer(.25*inch, .25*inch))


        graph = PlotManyChart()
        graph.chart.valueAxis.valueMax = 1
        
        # print input_data.transpose()[0]
        # input_data.transpose()
        # input_data = input_data.transpose()
        newlist = []

        for item in input_data[1:]:
            w = []
            for i, x in enumerate(item):
                w.append((times[i], x))
            newlist.append(w)
        print input_data
        # print len(input_data[0])
        graph.chart.data = input_data
        # [input_data[0:5]]
        doc_elements.append(graph)
                        
        
        doc.build(doc_elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf


    ##################################################################################### /NEW

    #k = KMeans()
    #print k.fit_transform(big_ol_array)
    #data = "1416339672399,6,995.5,-1.8387043,3.4245400".split(",")
    #print k.predict(data)
    #print big_ol_array[:25]


big_ol_array = []
apps_open = [("0", "0.0"),]
times = []
def main():
    with open("data.txt", "rb") as f:
        for i, line in enumerate(f):
            line_a = line.strip().split(",")
            times.append(line_a[0])
            if line_a[-1][:2]==("0."):
                if line_a[-1] != apps_open[-1][1]:
                    apps_open.append((i, line_a[-1]))
            big_ol_array.append([float(x) for x in line_a][1:-1])
    print apps_open
    print len(big_ol_array)
    array = np.array(big_ol_array)

    min_max_scaler = preprocessing.MinMaxScaler()
    scaled_array = min_max_scaler.fit_transform(array)
    print scaled_array[100:102]

    buffer = BytesIO()
    report = PDFWrapper(buffer, 'Letter')
    pdf = report.generate_pdf(
        scaled_array[100:],
        times[100:],
    )
    with open("output.pdf", "wb") as f:
        f.write(pdf)
    #pdf.write("output.pdf")
    
    ##################################################################################### NEW


if __name__=="__main__":
    main()