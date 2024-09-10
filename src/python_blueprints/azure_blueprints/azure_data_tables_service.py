import os
from openpyxl import Workbook

from azure.data.tables import TableServiceClient, TableClient


def read_rows():
    connection_string = os.environ['AZURE_CONN_STR']
    my_filter = "PartitionKey eq 'YOUR_PARTITION_KEY'"
    table_name = "TABLE NAME"

    with TableServiceClient.from_connection_string(conn_str=connection_string) as table_service_client:
        table_client = table_service_client.get_table_client(table_name)
        entities = table_client.query_entities(my_filter)
        rows = []
        key_row = []
        is_first = True
        for entity in entities:
            print(entity)
            val_row = []
            for key in entity.keys():
                if is_first:
                    key_row.append(key)
                val_row.append(entity[key])
            if is_first:
                rows.append(key_row)
            is_first = False
            rows.append(val_row)

    return rows


def write_to_excel(excel_name, value_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "results"

    for row in value_rows:
        ws.append(row)

    wb.save("../../../output/" + excel_name + ".xlsx")


if __name__ == "__main__":
    rows = read_rows()
    write_to_excel("excel file name", rows)
