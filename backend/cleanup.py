import time

def cleanup_old_vectors(index):

    two_hours_ago = time.time() - (2 * 60 * 60)

    index.delete(
        filter={
            "created_at": {
                "$lt": two_hours_ago
            }
        }
    )

    print("Old vectors deleted")