def check_video_exists(index,vid_id):
    results= index.query(
        vector=[0.0]*1536,
        top_k=1,
        filter={
            'video_id':vid_id.lower()
        },
        include_metadata=True
    )
    return len(results['matches'])>0