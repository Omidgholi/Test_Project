import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tkinter.messagebox


#Make sure dates are in correct format


def gym_analysis(venue, start_date, end_date):


    cols = ["venue", "date", "time", "status", "count"]
    df = pd.read_csv("occupancy_data_new.csv",names=cols).drop_duplicates()

    df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True, cache=True, errors="coerce")
    df['time'] = pd.to_datetime(df['time'], infer_datetime_format=True, cache=True, errors="coerce") #.dt.hour

    start_time = 0
    end_time = 24


    if start_date is None and end_date is None:
        if venue == "ALL":
            data = df[
                df["status"].eq("Open")]# & df['time']].between(start_time,end_time)
        else:
            data = df[df["venue"].eq(venue) & df["status"].eq("Open") & df['time'].between(start_time, end_time)]
    else:
        try:
            if venue == "ALL":
                data = df[df["status"].eq("Open") & df["date"].between(start_date, end_date) & df['time'].between(start_time,end_time)]
            else:
                data = df[df["venue"].eq(venue) & df["status"].eq("Open") & df["date"].between(start_date, end_date) & df['time'].between(start_time, end_time)]
        except:
            tkinter.messagebox.showerror(message="Please Select a different date range", title="Error", icon="error")
            exit()
    try:
        bottom_quartile = round(data["count"].quantile(0.25))
        top_quartile = round(data["count"].quantile(0.75))
        average = round(data["count"].mean())
        print(f"Bottom Quartile: {bottom_quartile}\nAverage: {average}\nTop Quartile: {top_quartile}")
        bottom_quart = data[data["count"].between(bottom_quartile, top_quartile)]
        # print(bottom_quart)
    except:
        tkinter.messagebox.showerror(message="No data available for this date range", title="Error", icon="error")
        exit()

    print(data)


    ax = sns.lineplot(data=data, x="time", y="count", hue="venue", ci=None)
    ax.set(xlabel="Time (24h Format)", ylabel="Count")
    if start_date is None and end_date is None:
        ax.set_title(f"Occupancy Data for {venue}")
    else:
        ax.set_title(f"Occupancy Data for {venue} from {start_date} to {end_date}")
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.show()
    plt.savefig("test.png")