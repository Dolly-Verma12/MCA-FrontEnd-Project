import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_health_report_pdf(user_name, tasks_done, water_amount, filename="health_report.pdf"):
    filepath = os.path.join("static", filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 750, f"AarogyaSaathi - Health Report for {user_name}")
    
    # Body
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Water Consumed Today: {water_amount} ml")
    c.drawString(100, 670, f"Daily Tasks Completed: {tasks_done}")
    c.drawString(100, 640, "Status: Active & Tracking")
    
    c.save()
    return filepath