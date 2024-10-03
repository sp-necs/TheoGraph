import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime as dt

st.set_page_config(layout='wide')
st.title("Theograph")
st.subheader("Welcome to Theograph app!")
st.write("This theograph app generate visuals to better understand clients journey through the system. Please upload the input file to see their journey!")

input_csv = st.file_uploader("Input CSV",
                                 type=['csv'])

required_columns = ['Client_ID','Event_ID','Start_Date','End_Date','Event_Type','Event_Subtype','Event_Desc']

sample_dataset= pd.DataFrame({
    'Client_ID' : [1234,1234,5678],
    'Event_ID' : ['R4321','S4321','R8756'],
    'Start_Date' : ['15/10/2023','20/10/2023','17/03/2024'],
    'End_Date' : ['15/10/2023',None,'18/03/2024'],
    'Event_Type' : ['Request','Service','Request'],
    'Event_Subtype' : ['Request','Residential','Request'],
    'Event_Desc' : ['This is request','This is ongoning residential service','This is request']
})

if input_csv is None:
    st.write("Please upload the input csv of following format and column names (If event is ongoing then keep 'End_Date' empty):")
    st.dataframe(sample_dataset, hide_index=True,
                 column_config={'Client_ID': st.column_config.TextColumn()}
                 )
    st.write("PS.: Date format- 31/12/2023 (dd/mm/YYYY)")
else:
    input_dataset = pd.read_csv(input_csv)

    column_errors = []
    for i in required_columns:
        if i not in input_dataset.columns:
            column_errors.append(i)

    if len(column_errors) > 0:
        st.error(f"Error: Column missing/incorrect in input file: {column_errors}")
    else:
        client_id_list = list(set(input_dataset["Client_ID"]))
        #st.write(input_dataset)
        client_form = st.sidebar.form("Client_ID_Form")
        client_id = client_form.number_input(label="Client ID", value=None, placeholder="Please enter client ID ....", step=1)
        client_form.divider()
        chart_start_date = client_form.date_input(label="Chart Start Date (Optional)", max_value=dt.today(), value=None)
        chart_end_date = client_form.date_input(label="Chart End Date (Optional)", max_value=dt.today(), value=None)
        sbt_btn = client_form.form_submit_button("Submit")

        if sbt_btn:
            if client_id is None:
                st.error("Error: Please enter the valid client id!")
            elif client_id not in client_id_list:
                st.warning(f"Client ID: '{client_id}' is not in the dataset!")
            else:
                client_dataset = input_dataset[input_dataset["Client_ID"] == client_id]
                client_dataset["Start_Date"] = pd.to_datetime(client_dataset["Start_Date"],format='%d/%m/%Y')
                client_dataset["End_Date"] = pd.to_datetime(client_dataset["End_Date"],format='%d/%m/%Y')
                client_dataset["Updated_End_Date"] = client_dataset["End_Date"].fillna(dt.today())
                event_list = list(client_dataset["Event_Type"].unique())
                for i in event_list:
                    client_dataset["Event_Type_Rank"] = [event_list.index(x) for x in client_dataset["Event_Type"]]
                #client_dataset["Event_Type_Rank"] = client_dataset["Event_Type"].rank(method="max")
                client_dataset["Event_Subtype_Rank"] = client_dataset.groupby(["Event_Type"])["Event_Subtype"].rank(method="dense",pct=True)
                client_dataset["Event_Type_Subtype_Rank"] = client_dataset["Event_Type_Rank"] + client_dataset["Event_Subtype_Rank"]

                #st.write(client_dataset)
                client_dataset["Date"] = client_dataset.apply(lambda x: pd.date_range(start=x["Start_Date"],end=x["Updated_End_Date"], freq='D'), axis=1)
                client_dataset = client_dataset.explode("Date")
                if chart_start_date is not None:
                    client_dataset = client_dataset[client_dataset["Date"]>=pd.to_datetime(chart_start_date)]
                if chart_end_date is not None:
                    client_dataset = client_dataset[client_dataset["Date"]<=pd.to_datetime(chart_end_date)]

                #st.write(client_dataset)
                
                fig = px.line(
                    x = client_dataset["Date"],
                    y = client_dataset["Event_Type_Subtype_Rank"],
                    color = client_dataset["Event_Type"],
                    #color_discrete_sequence = ['rgb(204, 204, 204)','rgb(204, 20, 204)'],
                    symbol = client_dataset["Event_Subtype"],
                    symbol_sequence= ['circle', 'circle-dot', 'square-dot', 'square'],
                    title = f"Theograph of client ID '{client_id}'",
                    custom_data=[client_dataset["Event_ID"],client_dataset["Start_Date"],client_dataset["End_Date"].fillna("Open"),client_dataset["Event_Desc"]]
                )
                fig.update_layout(
                    yaxis = dict(
                    showticklabels = False
                    ),
                    xaxis_title = "Date",
                    yaxis_title = "Events"
                )
                fig.update_traces(
                    mode = "markers",
                    hovertemplate = "Event ID: %{customdata[0]} <br>Start Date: %{customdata[1]} <br>End Date: %{customdata[2]} <br>Event Desc: %{customdata[3]}"
                )
                fig.update_legends(
                    title = "Event Type / Subtype"
                )
                fig.update_yaxes(
                    showgrid = False
                )

                st.divider()
                st.plotly_chart(fig)

                export_csv = input_dataset[input_dataset["Client_ID"] == client_id].to_csv(index=False)
                st.download_button(
                    label = "Download CSV",
                    data = export_csv,
                    file_name = str(dt.today().strftime('%Y%m%d'))+"_"+str(client_id)+".csv",
                    mime = "text/csv"
                )
                # input_dataset["Start_Date"] = pd.to_datetime(input_dataset["Start_Date"],format='%d/%m/%Y')
                # input_dataset["End_Date"] = pd.to_datetime(input_dataset["End_Date"],format='%d/%m/%Y')
                # st.dataframe(
                #     input_dataset[input_dataset["Client_ID"] == client_id].sort_values(["Start_Date","End_Date"]),
                #     hide_index=True,
                #     column_config={
                #         "Client_ID" : st.column_config.TextColumn("Client ID"),
                #         "Event_ID" : "Event ID",
                #         "Start_Date" : "Start Date",
                #         "End_Date" : "End Date",
                #         "Event_Type" : "Event Type",
                #         "Event_Subtype" : "Event Subtype",
                #         "Event_Desc" : "Event Description"
                #         }
                #     )