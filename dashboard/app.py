import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px


# Database connection function
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="Project_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch data from MySQL
def fetch_data(query):
    connection = get_connection()
    df = pd.DataFrame()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
    finally:
        connection.close()
    return df

# Streamlit App Layout
st.set_page_config(page_title="Multi-Source Integration Hub", layout="wide")
st.sidebar.title("Multi-Source Integration Hub")
st.sidebar.markdown("---")

# Sidebar Navigation
option = st.sidebar.radio("Select Analysis:", [
    "Sales Performance",
    "Product Analysis",
    "Aggregation",
    "Business Metrics",
])

if option == "Sales Performance":
    st.title("Sales Performance Analysis")
    
    if st.button("Fetch Sales Data"):
        df = fetch_data("SELECT * FROM dm_sales_performance ORDER BY total_revenue DESC LIMIT 20")
        st.dataframe(df)

        # Convert total_revenue to millions
        df['total_revenue'] = df['total_revenue'] / 1_000_000  

        # Format values in 'K' with 1 decimal place
        df['formatted_revenue'] = (df['total_revenue'] * 1000).map(lambda x: f"{x:.1f}K")

        # Bar chart
        fig = px.bar(df, 
                     x='customer_state', 
                     y='total_revenue', 
                     text=df['formatted_revenue'],  
                     title='State-wise Revenue (in Millions)', 
                     color='total_revenue',
                     color_continuous_scale=[
                         "rgb(0, 0, 139)",
                         "rgb(0, 0, 205)",
                         "rgb(30, 144, 255)", 
                         "rgb(135, 206, 250)"
                     ])

        # Styling the text inside bars
        fig.update_traces(textposition="outside", textfont_size=12, marker=dict(line=dict(width=0.5, color='black')))

        st.plotly_chart(fig, use_container_width=True)

elif option == "Product Analysis":
    st.title("Product Category Analysis")
    if st.button("Fetch Product Data"):
        df = fetch_data("SELECT * FROM dm_product_category_analysis ORDER BY total_revenue DESC LIMIT 10")
        st.dataframe(df)

        # Brighter color palette
        bright_colors = ['#FF4500', '#FF6347', '#FFD700', '#32CD32', '#1E90FF', 
                         '#8A2BE2', '#00FA9A', '#FF69B4', '#FFA500', '#7FFF00']

        # Pie chart
        fig_pie = px.pie(df, names='product_category_name', values='total_revenue',
                         title='Revenue Contribution by Product Category',
                         color_discrete_sequence=bright_colors)
        fig_pie.update_traces(textinfo='label')
        st.plotly_chart(fig_pie, use_container_width=True)

        # Donut chart
        fig_donut = px.pie(df, names='product_category_name', values='total_revenue',
                           title='Revenue Share by Category', hole=0.3,
                           color_discrete_sequence=bright_colors)

        st.plotly_chart(fig_donut, use_container_width=True)

elif option == "Aggregation":
    st.title("Aggregated Data Analysis")
    selected_option = st.selectbox("Select Aggregation Type:", 
                                   ["Total Sales by Customer", "Revenue by Category", 
                                    "Monthly Sales Summary", "Daily Sales Summary"])

    if st.button("Fetch Aggregated Data"):
        if selected_option == "Daily Sales Summary":
            df = fetch_data("SELECT * FROM daily_sales_summary")
            st.dataframe(df)

        elif selected_option == "Monthly Sales Summary":
            df = fetch_data("SELECT * FROM monthly_sales_summary WHERE year=2017")
            st.dataframe(df)
            fig = px.area(df, x='month', y='total_revenue',
                          title='Monthly Sales Trend',
                          markers=True,
                          color_discrete_sequence=['#FF5733'],  # Brightened color
                          line_shape="spline")  # Smooth curve for better trend visualization

            # Enhancing readability and aesthetics
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Total Revenue",
                xaxis=dict(tickmode='linear', showgrid=False),  # Ensure all months are displayed
                yaxis=dict(title="Revenue", tickformat=".2s", showgrid=True, gridcolor='lightgray'),
                plot_bgcolor="white"
            )

            # Adjusting markers and line properties
            fig.update_traces(
                marker=dict(size=7, line=dict(width=1, color='black')),
                line=dict(width=3),
                fill="tonexty",  # Adds a smooth gradient fill below the line
                textposition='top center',
                textfont_size=12
            )

            st.plotly_chart(fig, use_container_width=True)

        elif selected_option == "Revenue by Category":
            df = fetch_data("SELECT * FROM revenue_by_category")
            st.dataframe(df)

            #Bar Chart
            fig = px.bar(df, x='product_category_name', y='total_revenue',
                         title='Revenue by Product Category',
                         color='total_revenue',  # Gradient color effect
                         text_auto='.2s',  # Auto-format text inside bars
                         color_continuous_scale='sunset')
            
            fig.update_traces(marker_line_color='black', marker_line_width=1.2, 
                              textposition='outside', textfont_size=12)

            st.plotly_chart(fig, use_container_width=True)

        elif selected_option == "Total Sales by Customer":
            df = fetch_data("SELECT * FROM total_sales_by_customer")
            st.dataframe(df)


elif option == "Business Metrics":
    st.title("Business Metrics Overview")
    if st.button("Fetch Business Metrics"):
        df = fetch_data("SELECT * FROM business_metrics_view")
        st.dataframe(df)

        # Horizontal Bar Chart for Business Metrics
        fig_hbar = px.bar(df, y='metric_name', x='metric_value', text='metric_value', 
                          title='Business Metrics Horizontal Bar Chart', 
                          orientation='h', color='metric_value', 
                          color_continuous_scale='inferno')
        st.plotly_chart(fig_hbar, use_container_width=True)

        # Donut Chart for Business Metrics
        fig_donut = px.pie(df, names='metric_name', values='metric_value', 
                          title='Business Metrics Donut Chart', hole=0.4)
        st.plotly_chart(fig_donut, use_container_width=True)


        # Line Graph for Business Metrics
        fig_line = px.line(df, x='metric_name', y='metric_value', 
                           title='Business Metrics Line Graph', markers=True, 
                           line_shape='spline', line_dash_sequence=['dot'], 
                           color_discrete_sequence=['#FF6347'])
        st.plotly_chart(fig_line, use_container_width=True)


        # Vertical Bar Chart
        fig_bar = px.bar(df, x='metric_name', y='metric_value', text='metric_value', 
                         title='Business Metrics Vertical Bar Chart', 
                         color='metric_value', color_continuous_scale='Plasma')
        st.plotly_chart(fig_bar, use_container_width=True)

        # Pie Chart
        fig_pie = px.pie(df, names='metric_name', values='metric_value', 
                         title='Business Metrics Pie Chart')
        st.plotly_chart(fig_pie, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Developed by Sumanth Kumar Valluru")