import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from scipy.stats import chi2
from tabulate import tabulate
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from oauthlib.oauth2.rfc6749.errors import AccessDeniedError


def main():
    while True:
        menu()
        try:
            option = int(input("Option: "))
            if option == 0:
                create_spreadsheet()
            elif option == 1:
                add_metric()
            elif option == 2:
                show_added_metrics()
            elif option == 3:
                calculate_p_values()
            elif option == 4:
                show_calculated_p_values()
            elif option == 5:
                add_external_metric()
            elif option == 6:
                global metrics_table
                metrics_table = holm_bonferroni_correction(calculated_p_values)
            elif option == 7:
                metrics_table = calculate_statistical_significance(metrics_table)
            elif option == 8:
                results_to_csv(metrics_table)
            elif option == 9:
                break
            else:
                print("Please choose an appropriate option")
        except ValueError:
            print("Please enter a valid option")


def menu():
    print(tabulate(
        [
            ["Create spreadsheet", 0],
            ["Add metrics", 1],
            ["Show added metrics", 2],
            ["Calculate p-values", 3],
            ["Show calculated p-values", 4],
            ["Add external metric p-value", 5],
            ["Apply Holm-Bonferroni correction", 6],
            ["Calculate statistical significance", 7],
            ["Export results to CSV", 8],
            ["Exit", 9]
        ],
        headers = ['Option'], tablefmt = 'fancy_grid'
        )
    )


def create_spreadsheet():
    global SPREADSHEET_ID, creds, service

    # SCOPES define what level of access your program is asking from the user’s Google account during OAuth2 authentication.
    # Google uses the list of scopes to show the permissions screen.
    # The user must approve these scopes.
    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
    try:
        # Authenticate user
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        # Open browser for login
        creds = flow.run_local_server(port = 0)
        service = build('sheets', 'v4', credentials = creds)
        spreadsheet = service.spreadsheets().create(
            body = {
                'properties': {'title': 'Chi metrics'},
                'sheets': [
                    {'properties': {'title': 'Metrics'}},
                    {'properties': {'title': 'Significance'}}
                ]
            },
            fields = 'spreadsheetId'
        ).execute()

        SPREADSHEET_ID = spreadsheet.get('spreadsheetId')
        print('Spreadsheet created')

    except FileNotFoundError:
        print('Missing credentials.json — please add your OAuth credentials file.')
    except AccessDeniedError:
        print('Access denied — user did not grant permission.')
    except GoogleAuthError as e:
        print(f'Authentication failed: {e}')


def contingency_table_p_values(file_path):
    df = pd.read_csv(file_path)
    df['Sum_rows'] = df[['Success', 'Failure']].sum(axis = 1)
    df.loc['Sum_cols'] = df[['Success', 'Failure', 'Sum_rows']].sum()
    df['EV_Success'] = df['Success']['Sum_cols'] * df['Sum_rows'] / df['Sum_rows']['Sum_cols']
    df['EV_Failure'] = df['Failure']['Sum_cols'] * df['Sum_rows'] / df['Sum_rows']['Sum_cols']
    df['Chi2_Success'] = (df['Success'] - df['EV_Success'])**2 / df['EV_Success']
    df['Chi2_Failure'] = (df['Failure'] - df['EV_Failure'])**2 / df['EV_Failure']
    df.loc['Sum_cols'] = df.drop('Sum_cols')[
        [
            'Success',
            'Failure',
            'Sum_rows',
            'EV_Success',
            'EV_Failure',
            'Chi2_Success',
            'Chi2_Failure'
        ]
    ].sum()
    Chi2_statistic = df.loc['Sum_cols']['Chi2_Success'] + df.loc['Sum_cols']['Chi2_Failure']
    p_value = chi2.sf(Chi2_statistic, 1)
    return df, p_value


added_metrics = {}
calculated_p_values = {}
metrics_table = pd.DataFrame()


def add_metric():
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', 1) 
    root.update()

    file_paths = filedialog.askopenfilenames(
        title = 'Choose metric files',
        filetypes = [('Pliki CSV', '*.csv')]
    )

    root.destroy()
    
    if file_paths:
        for path in file_paths:
            metric_name = os.path.splitext(os.path.basename(path))[0]
            added_metrics[metric_name] = path
        
        print(f'Successfully added {len(file_paths)} metric(s)')
    else:
        print('File selection cancelled. No metrics were added')


def show_added_metrics():
    if added_metrics:
        print('Added metrics:')
        iteration = 0
        for metric, path in added_metrics.items():
            iteration += 1
            print(f'{iteration}. {metric}: {path}')
    else:
        print('No metrics added yet')


def calculate_p_values():
    global SPREADSHEET_ID, creds, service
    current_row = 1

    if added_metrics:
        for metric, path in added_metrics.items():
            df, p_value = contingency_table_p_values(path)
            calculated_p_values[metric] = p_value
            df_to_write = [df.columns.tolist()] + df.astype(str).values.tolist()
            metric_header = [
                [
                    f'Metric: {metric}',
                    'P-value:',
                    np.float64(p_value)
                ]
            ]
            blank_row = [["", ""]]
            block_to_write = metric_header + df_to_write + blank_row
            start_range = f"Metrics!A{current_row}"
            service.spreadsheets().values().update(
                spreadsheetId = SPREADSHEET_ID,
                range = start_range,
                valueInputOption = "RAW",
                body = {"values": block_to_write}
            ).execute()
            current_row += len(block_to_write) + 1
        print('P-values calculated')
    else:
        print('No metrics available for calculations yet')


def show_calculated_p_values():
    if calculated_p_values:
        print('Calculated p-values:')
        iteration = 0
        for metric, p_value in calculated_p_values.items():
            iteration += 1
            print(f'{iteration}. {metric}: {p_value}')
    else:
        print('No metrics hence no p-values :(')


def holm_bonferroni_correction(metrics):
    holm_bonferroni_table = pd.DataFrame(columns = ['Metric', 'p-value'])
    for metric, p_value in metrics.items():
        holm_bonferroni_table.loc[len(holm_bonferroni_table)] = [metric, p_value]

    holm_bonferroni_table = holm_bonferroni_table.sort_values(by = 'p-value', ascending = True).reset_index(drop = True)
    n_of_metrics = len(holm_bonferroni_table)
    holm_bonferroni_table['Corrected alpha'] = 0.05 / (n_of_metrics - (holm_bonferroni_table.index + 1) + 1)

    print('Metrics with corrected alpha:')
    print(holm_bonferroni_table)

    return holm_bonferroni_table


def calculate_statistical_significance(corrected_alpha_table):
    global SPREADSHEET_ID, creds, service

    corrected_alpha_table['Statistical significance'] = np.where(
        corrected_alpha_table['p-value'] < corrected_alpha_table['Corrected alpha'],
        'Significant',
        'Not significant'
    )

    df_to_write = [corrected_alpha_table.columns.tolist()] + corrected_alpha_table.astype(str).values.tolist()
    start_range = f'Significance!A1'
    service.spreadsheets().values().update(
        spreadsheetId = SPREADSHEET_ID,
        range = start_range,
        valueInputOption = "RAW",
        body = {"values": df_to_write}
    ).execute()

    print('Statistical significance:')
    print(corrected_alpha_table)

    return corrected_alpha_table


def add_external_metric():
    external_metric_name = input("Please specify metric name: ")
    external_metric_p_value = np.float64(input("Please specify metric p-value: "))
    calculated_p_values[external_metric_name] = external_metric_p_value


def results_to_csv(corrected_alpha_table):
    corrected_alpha_table.to_csv('Chi2_significance_results.csv', index = False)

    print('Results exported')


if __name__ == "__main__":
    main()