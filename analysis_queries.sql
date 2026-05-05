-- Hotel Booking Analysis SQL Script
-- Database: MySQL

-- 1. Create Schema
CREATE TABLE IF NOT EXISTS hotel_bookings (
    customer_id INT,
    property_id INT,
    city VARCHAR(100),
    star_rating INT,
    booking_date DATE,
    check_in_date DATE,
    check_out_date DATE,
    room_type VARCHAR(50),
    num_rooms_booked INT,
    stay_type VARCHAR(50),
    booking_channel VARCHAR(50),
    booking_value DECIMAL(12, 2),
    costprice DECIMAL(12, 2),
    markup DECIMAL(12, 2),
    selling_price DECIMAL(12, 2),
    payment_method VARCHAR(50),
    refund_status VARCHAR(10),
    refund_amount DECIMAL(12, 2),
    channel_of_booking VARCHAR(50),
    booking_status VARCHAR(20),
    travel_date DATE,
    cashback DECIMAL(12, 2),
    coupon_redeem DECIMAL(12, 2),
    coupon_used VARCHAR(5),
    stay_duration INT,
    lead_time INT,
    total_margin DECIMAL(12, 2),
    is_valid_date BOOLEAN
);

-- Note: To load data from CSV into MySQL, you can use:
-- LOAD DATA INFILE '/path/to/Hotel_Bookings_Cleaned.csv'
-- INTO TABLE hotel_bookings
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- ---------------------------------------------------------
-- TASK 1: IDENTIFY KEY OBSERVATIONS
-- ---------------------------------------------------------

-- 1.1 Booking status distribution
SELECT 
    booking_status, 
    COUNT(*) as total_bookings,
    ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM hotel_bookings), 2) as percentage
FROM hotel_bookings
GROUP BY booking_status;

-- 1.2 Cancellation Patterns by Channel and Star Rating
SELECT 
    channel_of_booking,
    star_rating,
    COUNT(*) as total_bookings,
    SUM(CASE WHEN booking_status = 'Cancelled' THEN 1 ELSE 0 END) as cancellations,
    ROUND(SUM(CASE WHEN booking_status = 'Cancelled' THEN 1 ELSE 0 END) * 100 / COUNT(*), 2) as cancellation_rate
FROM hotel_bookings
GROUP BY channel_of_booking, star_rating
ORDER BY cancellation_rate DESC;

-- 1.3 Revenue by Room Type
SELECT 
    room_type,
    SUM(selling_price) as total_revenue,
    SUM(total_margin) as total_profit,
    ROUND(SUM(total_margin) * 100 / SUM(selling_price), 2) as margin_percentage
FROM hotel_bookings
WHERE booking_status = 'Confirmed'
GROUP BY room_type
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------
-- TASK 2: ROOT CAUSE ANALYSIS
-- ---------------------------------------------------------

-- 2.1 Average Lead Time for Cancelled vs Confirmed
SELECT 
    booking_status,
    AVG(lead_time) as avg_lead_time_days
FROM hotel_bookings
WHERE is_valid_date = 1
GROUP BY booking_status;

-- 2.2 Performance by Channel (Conversion & Value)
SELECT 
    channel_of_booking,
    AVG(selling_price) as avg_booking_value,
    COUNT(*) as total_bookings,
    ROUND(SUM(CASE WHEN booking_status = 'Confirmed' THEN 1 ELSE 0 END) * 100 / COUNT(*), 2) as conversion_rate
FROM hotel_bookings
GROUP BY channel_of_booking
ORDER BY conversion_rate DESC;

-- 2.3 Seasonal Trends influencing Booking Values
SELECT 
    MONTHNAME(check_in_date) as check_in_month,
    AVG(selling_price) as avg_value,
    AVG(stay_duration) as avg_stay_length
FROM hotel_bookings
WHERE booking_status = 'Confirmed' AND check_in_date IS NOT NULL
GROUP BY check_in_month
ORDER BY FIELD(check_in_month, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');

-- ---------------------------------------------------------
-- TASK 3: BUSINESS RECOMMENDATIONS (Supporting Data)
-- ---------------------------------------------------------

-- Identify high-cancellation properties (possible root cause)
SELECT 
    property_id,
    city,
    COUNT(*) as total_bookings,
    SUM(CASE WHEN booking_status = 'Cancelled' THEN 1 ELSE 0 END) as cancellations,
    ROUND(SUM(CASE WHEN booking_status = 'Cancelled' THEN 1 ELSE 0 END) * 100 / COUNT(*), 2) as cancellation_rate
FROM hotel_bookings
GROUP BY property_id, city
HAVING total_bookings > 50
ORDER BY cancellation_rate DESC
LIMIT 10;
