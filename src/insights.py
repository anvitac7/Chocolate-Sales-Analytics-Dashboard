def generate_insights(df):
    """
    Generate key business insights from filtered dataframe
    """

    total_revenue = df["amount"].sum()

    top_country = (
        df.groupby("country")["amount"]
        .sum()
        .idxmax()
    )

    top_product = (
        df.groupby("product")["amount"]
        .sum()
        .idxmax()
    )

    peak_month = (
        df.groupby("month_name")["amount"]
        .sum()
        .idxmax()
    )

    insights = f"""
    🔹 Top Revenue Country: {top_country}  
    🔹 Best Selling Product: {top_product}  
    🔹 Peak Sales Month: {peak_month}  
    🔹 Total Revenue: ${total_revenue:,.0f}
    """

    return insights