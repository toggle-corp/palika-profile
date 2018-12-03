from drafter.draft import PdfDraft
from report import Page1, Page2


PdfDraft('test.pdf')\
    .draw(Page1())\
    .draw(Page2())
