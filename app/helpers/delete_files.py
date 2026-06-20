import os


def delete_file(
    file_url: str | None,
):
    if not file_url:
        return

    filepath = file_url.lstrip("/")

    if os.path.exists(filepath):
        os.remove(filepath)
