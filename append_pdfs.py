from PyPDF2 import PdfFileMerger

def append_pdfs(pdfs, output_pdf):

	merger = PdfFileMerger()

	for pdf in pdfs:
	    merger.append(pdf)

	merger.write("result.pdf")


pdfs = ['Part 103042018.pdf', 'Part 203042018.pdf']
append_pdfs(pdfs, output_pdf)