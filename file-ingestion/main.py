import os, json

import unstructured_client
from unstructured_client.models import operations, shared

from dotenv import load_dotenv
load_dotenv()

client = unstructured_client.UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
    server_url=os.getenv("UNSTRUCTURED_API_URL"),
    server='free-api'
)

filename = "./files/test.txt"
outputFileName = "./out/out.json"
with open(filename, "rb") as f:
    data = f.read()

print('DATA', data)
req = operations.PartitionRequest(
    partition_parameters=shared.PartitionParameters(
        files=shared.Files(
            content=data,
            file_name=filename,
        ),
        strategy=shared.Strategy.HI_RES,
        languages=['eng'],
        split_pdf_page=True,            # If True, splits the PDF file into smaller chunks of pages.
        split_pdf_allow_failed=True,    # If True, the partitioning continues even if some pages fail.
        split_pdf_concurrency_level=15  # Set the number of concurrent request to the maximum value: 15.
    ),
)

try:
    res = client.general.partition(request=req)
    element_dicts = [element for element in res.elements]
    
    # Print the processed data's first element only.
    print(element_dicts[0])

    # Write the processed data to a local file.
    json_elements = json.dumps(element_dicts, indent=2)
    
    with open(outputFileName, "w") as file:
        file.write(json_elements)
except Exception as e:
    print(e)
