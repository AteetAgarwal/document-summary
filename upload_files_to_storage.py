from azure.storage.blob import BlobServiceClient
import os
import sys
from dotenv import load_dotenv

def upload_summaries_to_blob_storage(connection_string, container_name):
    """
    Uploads all summaries files in the 'pdf_summaries' folder to Azure Blob Storage.

    Args:
        connection_string (str): The connection string for the Azure Blob Storage account.
        container_name (str): The name of the container in Azure Blob Storage.

    Side Effects:
        Uploads files to the specified Azure Blob Storage container.
    """
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Ensure the container exists
        if not container_client.exists():
            container_client.create_container()

        # Iterate through all files in the 'summaries' folder
        summaries_folder = "summaries"
        for filename in os.listdir(summaries_folder):
            file_path = os.path.join(summaries_folder, filename)

            if os.path.isfile(file_path):
                # Define the blob name with the folder structure
                blob_name = f"etl/pdf_summaries/{filename}"
                print(f"Uploading {blob_name} to Azure Blob Storage...")

                # Upload the file
                with open(file_path, "rb") as data:
                    container_client.upload_blob(name=blob_name, data=data, overwrite=True)

                print(f"Uploaded {blob_name} successfully.")

    except Exception as e:
        print(f"Error uploading summaries to Azure Blob Storage: {e}")

def upload_summary_to_blob_storage(file_name, connection_string, container_name):
    """
    Uploads a single summary file to Azure Blob Storage.

    Args:
        file_name (str): The file name of the document.
        connection_string (str): The connection string for the Azure Blob Storage account.
        container_name (str): The name of the container in Azure Blob Storage.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Ensure the container exists
        if not container_client.exists():
            container_client.create_container()

        # Define the file path and blob name
        filename = f"{file_name}.json"
        file_path = f"summaries/{filename}"
        if not os.path.exists(file_path):
            print(f"Summary file {file_path} does not exist for upload.")
            return False
        # Define the blob name with the folder structure
        blob_name = f"etl/pdf_summaries/{filename}" 
        print(f"Uploading {blob_name} to Azure Blob Storage...")    

        # Check if file exists before uploading
        if not os.path.exists(file_path):
            print(f"Summary file {file_path} not found for upload.")
            return False

        # Upload the file
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)

        print(f"Successfully uploaded {blob_name} to Azure Blob Storage.")
        return True

    except Exception as e:
        print(f"Error uploading summary to Azure Blob Storage: {e}")
        return False

def check_summary_exists_in_blob(file_name, connection_string, container_name):
    """
    Checks if a summary file already exists in Azure Blob Storage.

    Args:
        file_name (str): The file name of the document.
        connection_string (str): The connection string for the Azure Blob Storage account.
        container_name (str): The name of the container in Azure Blob Storage.

    Returns:
        bool: True if the summary exists in blob storage, False otherwise.
    """
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Define the blob name
        filename = f"{file_name}.json"
        blob_name = f"etl/pdf_summaries/{filename}"

        # Check if blob exists
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.exists()

    except Exception as e:
        print(f"Error checking blob existence: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
   # Get environment variables with validation
    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    container_name = os.getenv("STORAGE_CONTAINER_NAME")
    
    # Check if environment variables are set
    if not connection_string:
        print("Error: STORAGE_CONNECTION_STRING environment variable is not set")
        sys.exit(1)
    
    if not container_name:
        print("Error: STORAGE_CONTAINER_NAME environment variable is not set")
        sys.exit(1)

    upload_summaries_to_blob_storage(connection_string, container_name)