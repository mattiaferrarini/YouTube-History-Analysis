import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from file_manager import FileManager

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable and build the YouTube API service
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

# Load the watch history and the already processed data from the files
watch_history = FileManager.load_history()
last_processed_index = FileManager.load_last_processed_history()
processed_history = FileManager.load_processed_history()

print(f'Loaded {len(watch_history)} watch history items.')
print(f'Beginning processing from index: {last_processed_index + 1}.')

# Process the watch history starting from the last processed index
for i in range(last_processed_index + 1, len(watch_history)):
    try:
        # Get video details from the watch history
        video_title = watch_history[i].get('title', '')
        time_of_watch = watch_history[i].get('time', '')
        video_id = watch_history[i].get('titleUrl', '').split('=')[-1]

        # Skip ads and other non-video items
        if not video_title.startswith('Watched '):
            continue

        # Get the topic details from the YouTube API
        video_request = youtube.videos().list(
            part='snippet, topicDetails',
            id=video_id
        )
        video_response = video_request.execute()

        # If an item was obtained, add its data to the processed history 
        if 'items' in video_response and len(video_response['items']) > 0:
            video = video_response['items'][0]
            processed_history.append({
                'title': video_title.replace('Watched ', ''),
                'id': video_id,
                'time': time_of_watch,
                'topicCategories': video.get('topicDetails', {}).get('topicCategories', []),
                'tags': video.get('snippet', {}).get('tags', [])
            })
        last_processed_index = i

        # Print progress update
        print(f'Processing video {i + 1}/{len(watch_history)}', end='\r')

    except HttpError as e:
        if 400 <= e.resp.status < 500:
            print(f'An HTTP error occurred: {e.resp.status} - {e.content}')
            break
    except Exception as e:
        print(f'An error has occured: {str(e)}')
        break
            

# Save all new processed data to the files
FileManager.save_last_processed_history(last_processed_index)
FileManager.save_processed_history(processed_history)
print(f'Processed items until index: {last_processed_index}.')
print('The newly processed data was successfully saved.')