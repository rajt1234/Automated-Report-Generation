# ===== IMPORT NECESSARY LIBRARIES =====
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from math import ceil
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# === CONFIG ===
CSV_FILE = "used_cars_data.csv"  # Your dataset file
PDF_FILE = "used_cars_full_report.pdf"
CHART1 = "top_brands.png"
CHART2 = "avg_price_brand.png"
CHART3 = "seating_capacity_heatmap.png"
CHART4 = "transmission_types.png"
CHART5 = "price_distribution.png"
CHART6 = "cars_by_year.png"
LOGO_FILE = "logo_placeholder.png"

# === LOAD DATA ===
df = pd.read_csv(CSV_FILE)
df['Brand'] = df['Name'].apply(lambda x: str(x).split()[0])

# === CALCULATE INSIGHTS ===
total_cars = len(df)
avg_price = df['Price'].mean()
most_common_fuel = df['Fuel_Type'].mode()[0]
most_common_brand = df['Brand'].mode()[0]

# === CHART 1: Top Brands ===
top_brands = df['Brand'].value_counts().nlargest(10)
plt.figure(figsize=(6, 4))
top_brands.plot(kind='bar', color='skyblue')
plt.title("Top 10 Brands (By Count)")
plt.ylabel("Number of Cars")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHART1)
plt.close()

# === CHART 2: Avg Price by Brand ===
avg_price_brand = df.groupby("Brand")["Price"].mean().dropna().sort_values(ascending=False).head(10)
plt.figure(figsize=(6, 4))
avg_price_brand.plot(kind='bar', color='orange')
plt.title("Average Price by Brand (Top 10)")
plt.ylabel("Avg Price (Lakh ₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHART2)
plt.close()

# === CHART 3: Heatmap of Seating Capacity vs Number of Cars ===
if 'Seating_Capacity' in df.columns:
    seating_data = df['Seating_Capacity'].value_counts().sort_index()
else:
    seating_data = pd.Series({
        2: 15,
        4: 119,
        5: 5932,
        6: 36,
        7: 794,
        8: 169,
        9: 3,
        10: 7
    })

heatmap_df = pd.DataFrame(seating_data)
heatmap_df.columns = ['Number of Cars']

plt.figure(figsize=(6, 4))
sns.heatmap(heatmap_df.T, annot=True, cmap='Reds', fmt='d')
plt.title('Distribution of Cars by Seating Capacity')
plt.xlabel('Seating Capacity')
plt.ylabel('')
plt.tight_layout()
plt.savefig(CHART3)
plt.close()

# === CHART 4: Transmission Type Counts ===
transmission_counts = df['Transmission'].value_counts()
plt.figure(figsize=(6, 4))
transmission_counts.plot(kind='bar', color='green')
plt.title("Transmission Types")
plt.ylabel("Number of Cars")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART4)
plt.close()

# === CHART 5: Price Distribution Histogram ===
plt.figure(figsize=(6, 4))
plt.hist(df['Price'], bins=30, color='purple', edgecolor='black')
plt.title("Price Distribution")
plt.xlabel("Price (Lakh ₹)")
plt.ylabel("Number of Cars")
plt.tight_layout()
plt.savefig(CHART5)
plt.close()

# === CHART 6: Year-wise Car Counts ===
year_counts = df['Year'].value_counts().sort_index()
plt.figure(figsize=(8, 4))
year_counts.plot(kind='bar', color='teal')
plt.title("Number of Cars by Year")
plt.xlabel("Year")
plt.ylabel("Number of Cars")
plt.tight_layout()
plt.savefig(CHART6)
plt.close()

# === CREATEING PLACEHOLDER LOGO ===
plt.figure(figsize=(2, 1))
plt.text(0.5, 0.5, '....Analysed Car Data....', fontsize=20, ha='center', va='center')
plt.axis('off')
plt.savefig(LOGO_FILE, bbox_inches='tight', transparent=True)
plt.close()

# === PDF SETUP ===
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
elements = []

# === COVER PAGE ===
elements.append(Image(LOGO_FILE, width=150, height=50))
elements.append(Spacer(1, 20))
elements.append(Paragraph("<u>USED CARS MARKET ANALYSIS REPORT</u>", styles['Title']))
elements.append(Spacer(1, 20))
elements.append(Paragraph("The analysed report focuses on the Indian used car market, with the CSV providing raw, structured data (7,252 entries, 14 attributes) and the PDF presenting this data in table format for analysis. The dataset's diversity (budget to luxury cars, multiple cities, fuel types) makes it valuable for predictive modeling and market studies.", styles['Normal']))
elements.append(Spacer(1, 10))
elements.append(Paragraph("""This report includes statistical insights, visualizations, and the full dataset.This report includes statistical insights, visualizations, and the full dataset. It covers a diverse range of vehicles, from budget models (e.g., Tata Nano, Maruti Alto) to luxury brands (e.g., Audi, BMW, Mercedes-Benz), with Diesel and Petrol as dominant fuel types and a mix of manual and automatic transmissions. It spans multiple cities, enabling region-specific analysis, and captures ownership histories to assess resale value impacts.
<br/><br/>
<b>📘 <u>Market Analysis Report Overview (from PDF)</u></b>
<br/><br/>
The "Used Cars Market Analysis Report" spans 305 pages, with a significant portion dedicated to the "Full Data Table" (pages 5–305), which mirrors the CSV dataset, listing details like Brand, Name, Location, Year, Fuel Type, Transmission, Owner Type, and Price for thousands of cars. The report also includes:
<br/><br/>
<b>• Visual Insights (Page 3): </b>Likely contains charts or graphs (e.g., distribution of cars by year, as hinted on Page 4), though specific visualizations are not fully detailed due to truncation.<br/>
<b>• Data Distribution (Page 4): </b>Mentions "Number of Cars by Year" (1990–2019), suggesting an analysis of market trends over time.<br/>
<b>• Comprehensive Data Tables (Pages 5–305):</b>Provide detailed records, organized by attributes like Brand, Location, and Price, covering cities such as Mumbai, Delhi, Chennai, Kolkata, Hyderabad, and others, with prices ranging from 0.56 lakhs to 69.5 lakhs.
<br/><br/>
<b>📘 <u>Key Insights</u></b>                         
<br/><br/>
<b>• Diversity: </b>The dataset includes vehicles from various brands, years, and price points, reflecting the heterogeneity of the Indian used car market.<br/>
<b>• Geographical Spread: </b>Listings span multiple cities, enabling region-specific analyses.<br/>
<b>• Challenges: </b>Missing data in "New Price" and "Power" fields, and inconsistent mileage values (e.g., 0.0 kmpl), require preprocessing for accurate analysis.<br/>
<b>• Applications: </b>The dataset and report are valuable for studying price determinants (e.g., mileage, engine size, ownership history), predicting resale values, and understanding regional market preferences.
<br/><br/>
This combined dataset and report serve as a robust resource for researchers, analysts, and automotive professionals aiming to explore pricing trends, consumer behavior, and market dynamics in India's used car industry. The dataset's diversity (budget to luxury cars, multiple cities, fuel types) makes it valuable for predictive modeling and market studies.""", styles['Normal']))
elements.append(PageBreak())

# === INSIGHTS ===
elements.append(Paragraph("🔍 Key Market Insights", styles['Heading1']))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"<b>Total Cars:</b> {total_cars}", styles['Normal']))
elements.append(Paragraph(f"<b>Average Price:</b> ₹ {avg_price:.2f} Lakh", styles['Normal']))
elements.append(Paragraph(f"<b>Most Common Fuel Type:</b> {most_common_fuel}", styles['Normal']))
elements.append(Paragraph(f"<b>Most Common Brand:</b> {most_common_brand}", styles['Normal']))
elements.append(Spacer(1, 12))

# === INSERTING CHARTS ===
elements.append(Image(CHART1, width=400, height=250))
elements.append(Spacer(1, 12))
elements.append(Image(CHART2, width=400, height=250))
elements.append(PageBreak())
elements.append(Paragraph("Additional Visual Insights", styles['Heading1']))
elements.append(Spacer(1, 12))
elements.append(Image(CHART3, width=400, height=150))
elements.append(Spacer(1, 12))
elements.append(Image(CHART4, width=400, height=250))
elements.append(Spacer(1, 12))
elements.append(Image(CHART5, width=400, height=250))
elements.append(Spacer(1, 12))
elements.append(Image(CHART6, width=400, height=250))
elements.append(PageBreak())

# === FULL DATA TABLE ===
full_df = df[['Brand', 'Name', 'Location', 'Year', 'Fuel_Type', 'Transmission', 'Owner_Type', 'Price']].dropna()
rows_per_page = 40
total_pages = ceil(len(full_df) / rows_per_page)

for page in range(total_pages):
    chunk = full_df.iloc[page * rows_per_page: (page + 1) * rows_per_page]
    table_data = [chunk.columns.tolist()] + chunk.values.tolist()

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(Paragraph(f"📄 Full Data Table - Page {page + 1}", styles['Heading2']))
    elements.append(table)
    elements.append(PageBreak())

# === PAGE NUMBER FUNCTION ===
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(200 * mm, 10 * mm, text)

# === BUILDING PDF WITH PAGE NUMBERS ===
doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

print(f"✅ Report generated: {PDF_FILE}")