from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.bucket("ta_bucket")


def upload_file(local_file, cloud_file):
    """Uploads a file to the bucket."""
    # source_file: GCP에 업로드할 파일 절대경로
    # destination_blob: 업로드할 파일을 GCP에 저장할 때의 이름

    blob = bucket.blob(cloud_file)
    blob.upload_from_filename(local_file)


def download_file(cloud_file, local_file):
    """Downloads a blob from the bucket."""
    # source_blob: GCP에 저장되어 있는 파일 명
    # destination_file: 다운받을 파일을 저장할 경로("local/path/to/file")

    blob = bucket.blob(cloud_file)
    blob.download_to_filename(local_file)


if __name__ == "__main__":
    datafile_list = [
        "playerdata.csv",
        "rankdata.csv",
        "registered_player_list.json",
        "serverdata.csv",
    ]

    for datafile in datafile_list:
        download_file(f"data/{datafile}", f"data\\{datafile}")
        print(f"{datafile} downloaded successfully.")

    # for datafile in datafile_list:
    #     upload_file(f"data\\{datafile}", f"data/{datafile}")
    #     print(f"{datafile} uploaded successfully.")
