def get_retriever(vector_store,vid_id):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5,
            'filter':{
                'video_id':vid_id
            }
            }
    )