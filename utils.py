import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def error(text):
    """Creates an error message box and print the error."""

    print(f"[!]   {text}!")
    messagebox.showerror("[ Error ]", text)


def add_graphs(cur, frame):
    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'

    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#1a1a1a'

    colors = [
"#FF5A5F",  # Red
"#0079BF",  # Blue
"#00C2E0",  # Teal
"#51E898",  # Green
"#F2D600",  # Yellow
"#FF7A5A",  # Orange
"#A652BB",  # Purple
"#EB5A46",  # Coral
"#FFD500",  # Gold
"#8ED1FC",  # Sky Blue
]

    try:
        order_status = ["Paid","Pending"]
        cur.execute("SELECT payment_status, COUNT(*) as count FROM orders GROUP BY payment_status;")
        payments = cur.fetchall()
        order_count = [x[1] for x in payments]

        figure = plt.Figure(figsize=(3, 3), dpi=100)
        ax = figure.add_subplot(1, 1, 1)

        ax.pie(order_count, labels=order_status, autopct="%1.1f%%", colors=colors, startangle=90)
        ax.set_title("Order Status Pie Chart")

        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=780,y=270)
    except:
        pass

    # Bar Graph for Earnings per month

    figure = plt.Figure(figsize=(7, 4), dpi=100)
    ax = figure.add_subplot(1, 1, 1)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    cur.execute("SELECT DATE_FORMAT(o.date, '%b') AS month, SUM(oi.quantity * oi.price) AS earnings FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.payment_status = 'paid' AND YEAR(o.date) = YEAR(CURDATE()) GROUP BY month ORDER BY o.date;")
    results  = cur.fetchall()
    earnings = [0] * 12
    for month, earning in results:
        index = months.index(month)
        earnings[index] = earning
    ax.bar(months, earnings,color=colors)
    ax.set_xlabel("Months")
    ax.set_ylabel("Earnings ($)")
    ax.set_title("Monthly Earnings")

    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=30,y=270)