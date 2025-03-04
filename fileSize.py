import os
import gzip
import shutil


def get_data():
    for file_name in os.listdir(log_dir):
        file_path = os.path.join(log_dir, file_name)

        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            print(f"file size {file_size}")
            if file_size > size_limit:
                # Compress the file
                compressed_file_path = os.path.join(archive_dir, f"{file_name}.gz")

                with open(file_path, 'rb') as f_in:
                    with gzip.open(compressed_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                print(f"Archived: {file_name} ({file_size} bytes)")

                # Optionally, delete the original log file
                os.remove(file_path)


if __name__ == "__main__":
    log_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log"
    archive_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log\\archive"
    size_limit = 10000

    os.makedirs(archive_dir, exist_ok=True)
    get_data()
    print("Hello")
