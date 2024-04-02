import PyPDF2

def extract_text_from_pdf(pdf_file_path):
    text = ''
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text

# Example usage:
pdf_file_path = '/Users/akshaysrinivasan/Downloads/django-chatbot-main/django_chatbot/chatbot/static/assets/Team 16 - Mental health Chatbot.pdf'
text = extract_text_from_pdf(pdf_file_path)
# print(text)
