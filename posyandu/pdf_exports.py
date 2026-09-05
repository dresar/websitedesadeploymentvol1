"""
PDF Export functions untuk Posyandu
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime


def create_pdf_export(title, data, headers, filename, color_scheme='blue'):
    """
    Generic function untuk membuat PDF export
    """
    # Create a BytesIO buffer
    output = BytesIO()
    
    # Create PDF document with landscape orientation
    from reportlab.lib.pagesizes import landscape, A4
    doc = SimpleDocTemplate(output, pagesize=landscape(A4), rightMargin=36, leftMargin=36, topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Color schemes
    color_schemes = {
        'blue': colors.darkblue,
        'green': colors.darkgreen,
        'orange': colors.darkorange,
        'brown': colors.brown
    }
    
    header_color = color_schemes.get(color_scheme, colors.darkblue)
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=header_color
    )
    
    # Build content
    content = []
    
    # Title
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 20))
    
    # Summary info
    content.append(Paragraph(f"<b>Total Data:</b> {len(data)} records", styles['Normal']))
    content.append(Paragraph(f"<b>Tanggal Export:</b> {datetime.now().strftime('%d %B %Y, %H:%M')}", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Prepare table data
    table_data = [headers] + data
    
    # Create table
    table = Table(table_data, repeatRows=1)
    
    # Table style
    table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data style
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 20))
    
    # Footer
    content.append(Paragraph(f"<i>Dokumen ini dibuat secara otomatis pada {datetime.now().strftime('%d %B %Y, %H:%M WIB')}</i>", styles['Normal']))
    
    # Build PDF
    doc.build(content)
    
    # Prepare response
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def export_health_records_pdf(records):
    """Export health records to PDF"""
    headers = [
        'ID', 'Nama Pasien', 'NIK', 'Lokasi', 'Tanggal', 
        'Berat (kg)', 'Tinggi (cm)', 'Tekanan Darah', 'Suhu (°C)',
        'Diagnosis', 'Pengobatan', 'Keluhan'
    ]
    
    data = []
    for record in records:
        row = [
            str(record.id) if record.id else '-',
            str(record.patient.name) if record.patient and record.patient.name else '-',
            str(record.patient.nik) if record.patient and record.patient.nik else '-',
            str(record.posyandu.name) if record.posyandu and record.posyandu.name else '-',
            record.visit_date.strftime('%d/%m/%Y') if record.visit_date else '-',
            str(record.weight) if record.weight else '-',
            str(record.height) if record.height else '-',
            str(record.blood_pressure) if record.blood_pressure else '-',
            str(record.temperature) if record.temperature else '-',
            str(record.diagnosis) if record.diagnosis else '-',
            str(record.treatment) if record.treatment else '-',
            str(record.complaints) if record.complaints else '-'
        ]
        data.append(row)
    
    return create_pdf_export(
        "LAPORAN REKAM KESEHATAN POSYANDU",
        data,
        headers,
        "Rekam_Kesehatan_Posyandu.pdf",
        "blue"
    )


def export_immunizations_pdf(immunizations):
    """Export immunizations to PDF"""
    headers = [
        'ID', 'Nama Pasien', 'NIK', 'Lokasi', 'Jenis Vaksin',
        'Tanggal Vaksinasi', 'Nomor Batch', 'Petugas', 'Status', 'Catatan'
    ]
    
    data = []
    for immunization in immunizations:
        row = [
            str(immunization.id) if immunization.id else '-',
            str(immunization.patient.name) if immunization.patient and immunization.patient.name else '-',
            str(immunization.patient.nik) if immunization.patient and immunization.patient.nik else '-',
            str(immunization.posyandu.name) if immunization.posyandu and immunization.posyandu.name else '-',
            str(immunization.get_vaccine_type_display()) if immunization.vaccine_type else '-',
            immunization.immunization_date.strftime('%d/%m/%Y') if immunization.immunization_date else '-',
            str(immunization.batch_number) if immunization.batch_number else '-',
            str(immunization.health_worker) if immunization.health_worker else '-',
            str(immunization.get_status_display()) if immunization.status else '-',
            str(immunization.notes) if immunization.notes else '-'
        ]
        data.append(row)
    
    return create_pdf_export(
        "LAPORAN DATA IMUNISASI POSYANDU",
        data,
        headers,
        "Data_Imunisasi_Posyandu.pdf",
        "green"
    )


def export_nutrition_data_pdf(nutrition_data):
    """Export nutrition data to PDF"""
    headers = [
        'ID', 'Nama Anak', 'NIK', 'Lokasi', 'Tanggal',
        'Usia (bln)', 'Berat (kg)', 'Tinggi (cm)', 'Lingkar Kepala (cm)',
        'Lingkar Lengan (cm)', 'Status Gizi', 'Vitamin A', 'Suplemen Besi', 'Catatan'
    ]
    
    data = []
    for nutrition in nutrition_data:
        row = [
            str(nutrition.id) if nutrition.id else '-',
            str(nutrition.patient.name) if nutrition.patient and nutrition.patient.name else '-',
            str(nutrition.patient.nik) if nutrition.patient and nutrition.patient.nik else '-',
            str(nutrition.posyandu.name) if nutrition.posyandu and nutrition.posyandu.name else '-',
            nutrition.measurement_date.strftime('%d/%m/%Y') if nutrition.measurement_date else '-',
            str(nutrition.age_months) if nutrition.age_months else '-',
            str(nutrition.weight) if nutrition.weight else '-',
            str(nutrition.height) if nutrition.height else '-',
            str(nutrition.head_circumference) if nutrition.head_circumference else '-',
            str(nutrition.arm_circumference) if nutrition.arm_circumference else '-',
            str(nutrition.get_nutrition_status_display()) if nutrition.nutrition_status else '-',
            'Ya' if nutrition.vitamin_a_given else 'Tidak',
            'Ya' if nutrition.iron_supplement_given else 'Tidak',
            str(nutrition.notes) if nutrition.notes else '-'
        ]
        data.append(row)
    
    return create_pdf_export(
        "LAPORAN DATA GIZI POSYANDU",
        data,
        headers,
        "Data_Gizi_Posyandu.pdf",
        "orange"
    )


def export_stunting_data_pdf(stunting_data):
    """Export stunting data to PDF"""
    headers = [
        'ID', 'Nama Anak', 'NIK', 'Tanggal', 'Usia (bln)',
        'Tinggi Badan (cm)', 'Berat Badan (kg)', 'Status Stunting', 'Catatan'
    ]
    
    data = []
    for stunting in stunting_data:
        row = [
            str(stunting.id) if stunting.id else '-',
            str(stunting.balita.name) if stunting.balita and stunting.balita.name else '-',
            str(stunting.balita.nik) if stunting.balita and stunting.balita.nik else '-',
            stunting.tanggal_ukur.strftime('%d/%m/%Y') if stunting.tanggal_ukur else '-',
            str(stunting.usia_bulan) if stunting.usia_bulan else '-',
            str(stunting.tinggi_badan) if stunting.tinggi_badan else '-',
            str(stunting.berat_badan) if stunting.berat_badan else '-',
            str(stunting.get_status_stunting_display()) if stunting.status_stunting else '-',
            str(stunting.keterangan) if stunting.keterangan else '-'
        ]
        data.append(row)
    
    return create_pdf_export(
        "LAPORAN DATA STUNTING POSYANDU",
        data,
        headers,
        "Data_Stunting_Posyandu.pdf",
        "brown"
    )
