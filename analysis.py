import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Premium Aesthetics
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlepad'] = 20
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.transparent'] = False

# High-fidelity Color Palettes
COLORS = ['#1a73e8', '#d93025', '#f9ab00', '#188038', '#5f6368']

def perform_analysis():
    # Load data
    df = pd.read_csv('Hotel_bookings_final.csv')
    
    # 1. Feature Engineering
    date_cols = ['booking_date', 'check_in_date', 'check_out_date', 'travel_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
        
    df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days
    df['lead_time'] = (df['check_in_date'] - df['booking_date']).dt.days
    df['total_margin'] = df['selling_price'] - df['costprice']
    df['has_dates'] = df['check_in_date'].notna()
    
    os.makedirs('visualizations', exist_ok=True)

    # --- VISUAL 1: Status Breakdown ---
    plt.figure(figsize=(10, 8))
    labels = ['Confirmed', 'Cancelled (No Dates)', 'Cancelled (With Dates)', 'Failed']
    sizes = [
        (df['booking_status']=='Confirmed').sum(),
        ((df['booking_status'] == 'Cancelled') & (~df['has_dates'])).sum(),
        ((df['booking_status'] == 'Cancelled') & (df['has_dates'])).sum(),
        (df['booking_status']=='Failed').sum()
    ]
    explode = (0.1, 0, 0, 0)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
            colors=['#4285F4', '#EA4335', '#FBBC05', '#9AA0A6'], explode=explode, shadow=True)
    plt.title('Booking Lifecycle Distribution', weight='bold')
    plt.savefig('visualizations/status_breakdown.png', bbox_inches='tight')

    # --- VISUAL 2: Cancellation Rate by Channel ---
    plt.figure()
    chan_cancel = df.groupby('channel_of_booking')['booking_status'].apply(lambda x: (x == 'Cancelled').mean() * 100).sort_values()
    ax = sns.barplot(x=chan_cancel.index, y=chan_cancel.values, palette='Blues_d')
    plt.title('Cancellation Propensity by Booking Channel', weight='bold')
    plt.ylabel('Cancellation Rate (%)')
    plt.xlabel('Channel of Booking')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', weight='bold')
    plt.savefig('visualizations/cancel_by_channel.png', bbox_inches='tight')
    
    # --- VISUAL 3: Value by Star Rating ---
    plt.figure()
    star_val = df[df['booking_status'] == 'Confirmed'].groupby('star_rating')['selling_price'].mean()
    ax = sns.barplot(x=star_val.index, y=star_val.values, palette='YlOrRd')
    plt.title('Average Booking Value (ABV) per Star Rating', weight='bold')
    plt.ylabel('Average Selling Price ($)')
    plt.xlabel('Star Rating')
    plt.savefig('visualizations/value_by_star.png', bbox_inches='tight')

    # --- VISUAL 4: Monthly Volume Trend ---
    plt.figure()
    df['check_in_month'] = df['check_in_date'].dt.month
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_stats = df[df['booking_status'] == 'Confirmed'].groupby('check_in_month')['selling_price'].count().reindex(range(1, 13))
    
    sns.lineplot(x=month_names, y=monthly_stats.values, marker='o', color='#1a73e8', linewidth=3, markersize=10)
    plt.fill_between(month_names, monthly_stats.values, alpha=0.1, color='#1a73e8')
    plt.title('Monthly Confirmed Booking Volume', weight='bold')
    plt.ylabel('Number of Bookings')
    plt.savefig('visualizations/seasonal_volume.png', bbox_inches='tight')

    # --- VISUAL 5: Lead Time Kernel Density ---
    plt.figure()
    df_with_dates = df[df['has_dates']].copy()
    sns.kdeplot(data=df_with_dates, x='lead_time', hue='booking_status', common_norm=False, fill=True, palette='coolwarm')
    plt.title('Lead Time Density: Confirmed vs. Cancelled', weight='bold')
    plt.xlabel('Days from Booking to Check-in')
    plt.xlim(0, 150)
    plt.savefig('visualizations/lead_time_distribution.png', bbox_inches='tight')

    # --- VISUAL 6: Profit Margin Efficiency ---
    plt.figure()
    df['margin_pct'] = (df['total_margin'] / df['selling_price']) * 100
    avg_margin = df[df['booking_status'] == 'Confirmed'].groupby('channel_of_booking')['margin_pct'].mean()
    sns.barplot(x=avg_margin.index, y=avg_margin.values, palette='Greens_d')
    plt.title('Margin Efficiency Index by Channel', weight='bold')
    plt.ylabel('Average Margin %')
    plt.savefig('visualizations/margin_pct_by_channel.png', bbox_inches='tight')

    print("\nPremium visualizations generated successfully.")

if __name__ == "__main__":
    perform_analysis()
