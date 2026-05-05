# Power BI Implementation Guide: Hotel Booking Dashboard

This guide provides the necessary steps, DAX measures, and layout instructions to recreate the Hotel Booking analysis in Power BI using the `Hotel_Bookings_Cleaned.csv` file.

## 1. Data Connection & Modeling
1. **Get Data**: Select **Text/CSV** and import `Hotel_Bookings_Cleaned.csv`.
2. **Transform Data**:
    - Ensure `booking_date`, `check_in_date`, `check_out_date`, and `travel_date` are set to **Date** type.
    - Ensure `selling_price`, `costprice`, and `markup` are set to **Fixed Decimal Number** (Currency).
3. **Modeling**:
    - Since this is a flat file, no complex relationships are needed initially.
    - Recommended: Create a **Date Table** and link it to `check_in_date` for advanced time intelligence.

## 2. DAX Measures (Essential)

Create a new table `_Measures` and add the following:

### Total Volume & Status
```dax
Total Bookings = COUNTROWS('Hotel_Bookings_Cleaned')

Confirmed Bookings = CALCULATE([Total Bookings], 'Hotel_Bookings_Cleaned'[booking_status] = "Confirmed")

Cancellation Rate % = 
DIVIDE(
    CALCULATE([Total Bookings], 'Hotel_Bookings_Cleaned'[booking_status] = "Cancelled"),
    [Total Bookings],
    0
)
```

### Financials
```dax
Total Revenue = SUM('Hotel_Bookings_Cleaned'[selling_price])

Total Margin = SUM('Hotel_Bookings_Cleaned'[total_margin])

Margin % = DIVIDE([Total Margin], [Total Revenue], 0)

Avg Booking Value = AVERAGE('Hotel_Bookings_Cleaned'[selling_price])
```

### Operational
```dax
Avg Lead Time = AVERAGE('Hotel_Bookings_Cleaned'[lead_time])

Avg Stay Length = AVERAGE('Hotel_Bookings_Cleaned'[stay_duration])
```

## 3. Dashboard Layout & Visuals

### Page 1: Executive Overview
- **KPI Cards**: Total Revenue, Confirmed Bookings, Cancellation Rate %, Margin %.
- **Donut Chart**: `booking_status` breakdown (Confirmed, Cancelled, Failed).
- **Bar Chart**: `Total Revenue` by `room_type`.
- **Map Visual**: `Total Bookings` by `city`.
- **Slicer**: `booking_channel`, `star_rating`, `stay_type`.

### Page 2: Cancellation & Performance Analysis
- **Clustered Column Chart**: `Cancellation Rate %` by `channel_of_booking`.
- **Line Chart**: `Avg Lead Time` vs. `Cancellation Rate %` over `booking_date`.
- **Decomposition Tree**: Analyze `Cancellation Rate %` by `star_rating`, then `city`, then `room_type`.
- **Scatter Plot**: `Lead Time` (X-axis) vs. `Selling Price` (Y-axis), colored by `booking_status`.

### Page 3: Temporal Trends
- **Area Chart**: `Total Revenue` by Month (using `check_in_date`).
- **Matrix**: `city` (Rows) vs. `Month` (Columns) with `Confirmed Bookings` as values (use Conditional Formatting/Heatmap).

## 4. Visual Excellence Tips
- **Theme**: Use the **"Executive"** or **"Innovate"** theme in Power BI for a premium look.
- **Interactivity**: Enable **"Edit Interactions"** to ensure the seasonal charts aren't filtered by the status donut in a confusing way.
- **Tooltips**: Create a custom Tooltip page showing `Top 5 Properties by Margin` when hovering over a city on the map.

---
*Report Author: Business Analyst AI*
