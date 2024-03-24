from fetch_details_gamil import get_labels, get_message_list
from database import insert_into_messages, insert_into_labels


def run_get_email():
    try:
        # Fetch messages and labels and store into db
        insert_into_messages(get_message_list())
        insert_into_labels(get_labels())

    except Exception as e:
        # Handle any exceptions that occur during the process
        print("An error occurred:", e)

if __name__ == "__main__":
    run_get_email()