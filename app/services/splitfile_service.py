from io import (BytesIO, StringIO)
import logging
import math
import os
#from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfreader import (PDFDocument)
from fastapi import (APIRouter, HTTPException, File, UploadFile, Form, Depends, Request, BackgroundTasks)
from pypdf import PdfWriter, PdfReader
import zipfile


logger = logging.getLogger(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))


def createZipFile(filename: str):
    return zipfile.ZipFile(filename, "w")

def appendFileToZip(zip: zipfile.ZipFile, filename: str):
    zip.write(filename)

def splitFile(pdfReader: PdfReader, filename: str, pageNumber: int, totalPages: int, zip: zipfile.ZipFile):
    writer_buffer = BytesIO()
    pdf_writer = PdfWriter(writer_buffer)

    for page in range(pageNumber, totalPages):
        pdf_writer.add_page(pdfReader.pages[page])

    with open(filename, 'wb') as file1:
        pdf_writer.write(file1)

    writer_buffer.close()
    pdf_writer.close()
    appendFileToZip(zip, filename)
    

class SplitFileService:
    def split(self, zipname: str, filename: str, split_numPages: int, file_content: bytes):
        #pdfFile = PDFDocument(file_content)
        
        reader_buffer = BytesIO(file_content)
        pdf_reader = PdfReader(reader_buffer)
        numPages = len(pdf_reader.pages)

        if split_numPages >= numPages:
            split_numPages = int( numPages / 2)

        zip_buffer = BytesIO()
        zipFile = zipfile.ZipFile(zip_buffer, "w")

        part = 1
        for pageNumber in range(0, numPages, split_numPages):
            splitFile(pdf_reader, 
                "%s_part%s.pdf" %(filename.removesuffix(".pdf"), part), 
                pageNumber, 
                min(split_numPages * part, numPages),
                zipFile)
            part += 1

        reader_buffer.close()       
        zipFile.close()

        return zip_buffer.getvalue()