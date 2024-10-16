# TheoGraph : Streamlit App

## Environment
This app uses following python packages:
- Streamlit
- Plotly Express
- Pandas

Environment folder contains the environment.yaml file that can be imported to install all these libraries.

## Datasets

### Input data table

The aim is to keep the number of required data fields minimum. So, this app requires following data fields:
- Client_ID
- Event_ID
- Start_Date
- End_Date
- Event_Type
- Event_Subtype
- Event_Desc

### Sample dataset
| Client_ID | Event_ID | Start_Date | End_Date | Event_Type | Event_Subtype | Event_Desc |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 1234 | R4321 | 15/10/2023 | 15/10/2023 | Request | Request | This is request |
| 1234 | S4321 | 20/10/2023 |  | Service | Residential | This is ongoning residential service |
| 5678 | R8756 | 17/03/2024 | 18/03/2024 | Request | Request | This is request |

> Test dataset csv is available under 'dataset' folder

PS.: Date format- 31/12/2023 (dd/mm/YYYY)

## Using the app
1. Upload the csv data file using the 'Browse files' button.
2. Once the csv is uploaded, sidebar form will be visible.
3. Enter the valid client_id to see the theograph of that client.
4. The chart can be filtered using optional Chart Start Date and Chart End Date inputs.
5. To download the theograph visual, use the camera icon at top right of the visual.
6. Use 'Download CSV' button to download the csv data file of that specific client.