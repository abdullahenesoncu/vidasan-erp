import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.colors import red
from io import BytesIO
from django.http import HttpResponse

# Register the Arial font
registerFont(TTFont('Arial', 'ARIAL.ttf'))

def createWorkOrder(siparis, user):
    # Create a BytesIO buffer to receive the PDF
    buffer = BytesIO()

    # Create a canvas object and set the page size
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Define margins
    margin = 50
    content_width = width - 2 * margin

    # Absolute path to the logo image
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'Vidasan', 'logo.png')

    # Draw the logo at the top right corner
    logo_width = 150  # Adjust width as needed
    logo_height = 150  # Adjust height as needed
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width - margin - logo_width, height - logo_height * 4 / 5, width=logo_width, height=logo_height, preserveAspectRatio=True)
    else:
        print(f"Logo file not found: {logo_path}")

    # Draw a title
    c.setFont("Arial", 16)
    c.drawString(margin, height - margin, "İş Emri")

    # Draw rectangles and text for each section
    def draw_section(y, title, content, font_size=12, box_height=35):
        content = str(content)
        c.setFont("Arial", font_size)

        # Draw the rectangle
        c.rect(margin, y - box_height, content_width, box_height, stroke=1, fill=0)

        # Set title color to red
        c.setFillColor(red)
        c.drawString(margin + 5, y - 12, title)

        # Reset fill color for content
        c.setFillColor("black")
        c.drawString(margin + 5, y - 30, content)

        return y - box_height - 10

    # Draw work order details
    y = height - margin - 40
    y = draw_section(y, "İş Tanımı", siparis.definition)
    y = draw_section(y, "Açıklama", siparis.description, box_height=120)  # Larger area for long descriptions
    y = draw_section(y, "Adet", siparis.amount)
    y = draw_section(y, "Termin Tarihi", siparis.deadline if siparis.deadline else 'N/A')
    y = draw_section(y, "Otomotiv Mi?", 'Evet' if siparis.isOEM else 'Hayır')
    y = draw_section(y, "Sipariş Numarası", siparis.orderNumber if siparis.orderNumber else 'N/A')
    y = draw_section(y, "Durum", siparis.state)
    y = draw_section(y, "Isil Islem:", siparis.isilIslem.name if siparis.isilIslem else 'N/A')
    y = draw_section(y, "Kaplama:", siparis.kaplama.name if siparis.kaplama else 'N/A')
    y = draw_section(y, "Patch:", siparis.patch.name if siparis.patch else 'N/A')

    # Draw user information
    c.setFont("Arial", 12)
    c.drawString(margin, y - 20, f"Emri Veren: {user.name}")

    # Draw signature section
    c.setFont("Arial", 12)
    c.drawString(margin, y - 60, "Signature:")
    c.line(margin, y - 70, margin + 200, y - 70)  # Draw a line for the signature

    # Finish up the PDF
    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and close it
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
