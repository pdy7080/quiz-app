# src/utils/youtube_uploader.py
import os
import time
import pickle
import traceback
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

class YouTubeUploader:
   def __init__(self, max_retries=3, retry_delay=5):
       # API 인증 관련
       self.credentials = None
       self.youtube = None
       self.scopes = [
           'https://www.googleapis.com/auth/youtube.upload',
           'https://www.googleapis.com/auth/youtube.readonly',
           'https://www.googleapis.com/auth/youtube.force-ssl',
           'https://www.googleapis.com/auth/youtubepartner'
       ]
       self.api_name = "youtube"
       self.api_version = "v3"
       
       # 재시도 설정
       self.max_retries = max_retries
       self.retry_delay = retry_delay
       
       # 일일 업로드 제한 관리
       self.daily_upload_count = 0
       self.last_upload_date = None
       self.MAX_DAILY_UPLOADS = 5
       self.UPLOAD_RESET_HOUR = 0

   def _check_upload_limit(self):
       """일일 업로드 제한 체크"""
       current_time = datetime.now()
       
       if (self.last_upload_date is None or 
           self.last_upload_date.date() != current_time.date()):
           print("Resetting daily upload count")
           self.daily_upload_count = 0
           self.last_upload_date = current_time
           return True
           
       if self.daily_upload_count >= self.MAX_DAILY_UPLOADS:
           next_reset = (current_time + timedelta(days=1)).replace(
               hour=self.UPLOAD_RESET_HOUR, minute=0, second=0
           )
           wait_seconds = (next_reset - current_time).total_seconds()
           print(f"Daily upload limit reached. Next reset in {wait_seconds/3600:.1f} hours")
           print(f"Current uploads today: {self.daily_upload_count}/{self.MAX_DAILY_UPLOADS}")
           return False
           
       return True

   def authenticate(self):
       """YouTube API 인증 (재시도 로직 포함)"""
       for attempt in range(self.max_retries):
           try:
               creds = None
               if os.path.exists('token.pickle'):
                   print("Loading existing token...")
                   with open('token.pickle', 'rb') as token:
                       creds = pickle.load(token)
                       
               if not creds or not creds.valid:
                   if creds and creds.expired and creds.refresh_token:
                       print("Refreshing access token...")
                       creds.refresh(Request())
                   else:
                       print("Fetching new token...")
                       flow = InstalledAppFlow.from_client_secrets_file(
                           'client_secrets.json', self.scopes)
                       creds = flow.run_local_server(port=0)
                       
                   print("Saving token...")
                   with open('token.pickle', 'wb') as token:
                       pickle.dump(creds, token)
                       
               self.youtube = build(self.api_name, self.api_version, credentials=creds)
               print("YouTube API authentication successful")
               return self.youtube
               
           except Exception as e:
               print(f"Authentication attempt {attempt + 1}/{self.max_retries} failed: {str(e)}")
               if attempt < self.max_retries - 1:
                   print(f"Retrying in {self.retry_delay} seconds...")
                   time.sleep(self.retry_delay)
               else:
                   print("All authentication attempts failed")
                   raise

   def get_channel_id(self):
       """브랜드 계정 채널 ID 가져오기 (재시도 로직 포함)"""
       for attempt in range(self.max_retries):
           try:
               channels = self.youtube.channels().list(
                   mine=True,
                   part='id,snippet'
               ).execute()
               
               print("Available channels:")
               for channel in channels.get('items', []):
                   print(f"Channel Title: {channel['snippet']['title']}")
                   print(f"Channel ID: {channel['id']}")
                   
               for channel in channels.get('items', []):
                   if '1 minute knowledge' in channel['snippet']['title'].lower():
                       print(f"Found target channel: {channel['snippet']['title']}")
                       return channel['id']
                       
               return None
               
           except Exception as e:
               print(f"Channel ID fetch attempt {attempt + 1}/{self.max_retries} failed: {str(e)}")
               if attempt < self.max_retries - 1:
                   print(f"Retrying in {self.retry_delay} seconds...")
                   time.sleep(self.retry_delay)
                   self.authenticate()  # 재인증
               else:
                   print("All attempts to get channel ID failed")
                   raise

   def upload_video(self, file_path, title, description, privacy_status="public"):
       """비디오 업로드 (재시도 로직 포함)"""
       if not self._check_upload_limit():
           return None
           
       for attempt in range(self.max_retries):
           try:
               if not self.youtube:
                   print("Authenticating...")
                   self.authenticate()

               if not os.path.exists(file_path):
                   print(f"Error: Video file not found at {file_path}")
                   return None

               print("Getting channel ID...")
               channel_id = self.get_channel_id()
               if not channel_id:
                   print("Could not find target channel")
                   return None

               body = {
                   'snippet': {
                       'channelId': channel_id,
                       'title': title,
                       'description': description,
                       'tags': ['quiz', 'educational', 'fun', '1minuteknowledge', 'shorts'],
                       'categoryId': '27'
                   },
                   'status': {
                       'privacyStatus': privacy_status,
                       'selfDeclaredMadeForKids': False
                   }
               }

               print(f"Starting upload attempt {attempt + 1}/{self.max_retries}")
               insert_request = self.youtube.videos().insert(
                   part=','.join(body.keys()),
                   body=body,
                   media_body=MediaFileUpload(
                       file_path, 
                       chunksize=1024*1024,
                       resumable=True
                   )
               )

               response = None
               while response is None:
                   try:
                       status, response = insert_request.next_chunk()
                       if status:
                           print(f"Uploaded {int(status.progress() * 100)}%")
                   except HttpError as e:
                       if "uploadLimitExceeded" in str(e):
                           print("YouTube upload limit exceeded")
                           self.daily_upload_count = self.MAX_DAILY_UPLOADS
                           return None
                       elif e.resp.status in [500, 502, 503, 504]:
                           # 재시도 가능한 서버 에러
                           continue
                       else:
                           raise
                   except (ConnectionError, ConnectionAbortedError) as e:
                       print(f"Connection error: {e}")
                       if attempt < self.max_retries - 1:
                           print(f"Retrying in {self.retry_delay} seconds...")
                           time.sleep(self.retry_delay)
                           break
                       else:
                           raise

               if response:
                   print(f"Upload Complete! Video ID: {response['id']}")
                   self.daily_upload_count += 1
                   print(f"Daily uploads: {self.daily_upload_count}/{self.MAX_DAILY_UPLOADS}")
                   return response['id']

           except Exception as e:
               print(f"Upload attempt {attempt + 1} failed: {str(e)}")
               if attempt < self.max_retries - 1:
                   print(f"Retrying in {self.retry_delay} seconds...")
                   time.sleep(self.retry_delay)
                   self.authenticate()  # 재인증
               else:
                   print("All upload attempts failed")
                   raise

       return None