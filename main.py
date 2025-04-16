import os
import json
import unicodedata
from time import sleep
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Muat variabel lingkungan dari file .env
load_dotenv()
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

# Atur scope yang dibutuhkan
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_PATH = "token.json"
# nahh
def authorize():
    """
    Mengotorisasi aplikasi dengan OAuth 2.0.
    Jika token sudah ada dan valid, digunakan. Jika tidak, akan dilakukan proses otorisasi baru.
    """
    creds = None
    # Jika file token sudah ada, coba load kredensial yang tersimpan
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as token_file:
            creds = Credentials.from_authorized_user_info(json.load(token_file), SCOPES)
    
    # Jika tidak ada kredensial yang valid, lakukan otorisasi baru
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_console()
        # Simpan token untuk pemakaian selanjutnya
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    return creds

def get_judol_comment(text):
    """
    Mengecek apakah text dianggap sebagai spam berdasarkan:
      1. Normalisasi Unicode (jika text berbeda setelah normalisasi, dianggap spam).
      2. Kehadiran kata-kata terblokir dalam text.
    """
    normalized_text = unicodedata.normalize("NFKD", text)
    if text != normalized_text:
        return True
    # Baca daftar kata-kata terblokir dari file blockedword.json
    with open("src/blockedword.json", "r") as f:
        blocked_words = json.load(f)
    lower_text = text.lower()
    return any(word.lower() in lower_text for word in blocked_words)

def fetch_comments(creds, video_id):
    """
    Mengambil komentar dari video YouTube tertentu dan mendeteksi komentar spam.
    """
    youtube = build("youtube", "v3", credentials=creds)
    spam_comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        ).execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comment_text = comment["textDisplay"]
            comment_id = item["id"]
            print(f'Checking comment: "{comment_text}"')
            if get_judol_comment(comment_text):
                print(f'🚨 Spam terdeteksi!: "{comment_text}"')
                spam_comments.append(comment_id)
    except Exception as error:
        print("Error fetching comments:", error)
    return spam_comments

def delete_comments(creds, comment_ids):
    """
    Menghapus (menolak) komentar-komentar yang terdeteksi spam.
    Proses dilakukan dalam chunk (potongan) masing-masing 50 komentar.
    """
    youtube = build("youtube", "v3", credentials=creds)
    total_comments = len(comment_ids)
    total_deleted = 0

    while comment_ids:
        # Ambil chunk komentar (maksimum 50 ID)
        chunk = comment_ids[:50]
        comment_ids = comment_ids[50:]
        try:
            # Untuk API YouTube, parameter "id" bisa berupa daftar ID yang dipisahkan koma.
            ids_str = ",".join(chunk)
            youtube.comments().setModerationStatus(
                id=ids_str,
                moderationStatus="rejected"
            ).execute()
            total_deleted += len(chunk)
            print(f"Kemajuan: {total_deleted}/{total_comments} ({len(comment_ids)} remaining)")
            print("Menghapus ID komentar berikut:", chunk)
        except Exception as error:
            print(f"Gagal menghapus ID komentar ini {chunk}: {error}")
        # Sedikit delay bila diperlukan (opsional)
        sleep(0.5)

def youtube_content_list(creds):
    """
    Mengambil daftar video dari channel YouTube berdasarkan upload playlist.
    """
    youtube = build("youtube", "v3", credentials=creds)
    all_videos = []
    try:
        # Dapatkan detail channel, khususnya relatedPlaylists.uploads
        channel_response = youtube.channels().list(
            part="contentDetails",
            id=YOUTUBE_CHANNEL_ID
        ).execute()

        channel = channel_response["items"][0]
        uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

        next_page_token = None
        while True:
            playlist_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            all_videos.extend(playlist_response.get("items", []))
            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as error:
        print("Error fetching videos:", error)
    return all_videos

def main():
    """
    Fungsi utama: Mengotorisasi, mengunduh daftar video, 
    memeriksa komentar untuk spam, dan menghapus komentar yang terdeteksi spam.
    """
    creds = authorize()
    content_list = youtube_content_list(creds)

    for video in content_list:
        title = video["snippet"]["title"]
        video_id = video["snippet"]["resourceId"]["videoId"]
        print(f'\n📹 Ngecek video: {title} (ID: {video_id})')
        spam_comments = fetch_comments(creds, video_id)

        if spam_comments:
            print(f'🚫 terdeteksi {len(spam_comments)} komentar spam. ngehapus dulu wir...')
            delete_comments(creds, spam_comments)
            print("✅ komentar terdetwksi bosku.")
        else:
            print("✅ Tidak ditemukan komentar spam.")

if __name__ == '__main__':
    main()
