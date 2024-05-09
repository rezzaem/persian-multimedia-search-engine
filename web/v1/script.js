// const API_KEY = 'AIzaSyD_nl2Hzfq3vebmDD5g1WUJ5OHNHe27tyc';
// const videoTitleInput = document.getElementById('video-title');
// const searchBtn = document.getElementById('search-btn');
// const videoList = document.getElementById('video-list');

// searchBtn.addEventListener('click', fetchRelatedVideos);

// function fetchRelatedVideos() {
//   const videoTitle = videoTitleInput.value.trim();
//   if (videoTitle === '') {
//     alert('Please enter a video title.');
//     return;
//   }

//   const maxResults = 10;
//   const urlParams = new URLSearchParams({
//     key: API_KEY,
//     q: videoTitle,
//     part: 'snippet',
//     type: 'video',
//     maxResults: maxResults,
//   });

//   const apiUrl = `https://www.googleapis.com/youtube/v3/search?${urlParams.toString()}`;

//   fetch(apiUrl)
//     .then(response => response.json())
//     .then(data => {
//       displayVideoList(data.items);
//     })
//     .catch(error => {
//       console.error('Error fetching video data:', error);
//     });
// }

// function displayVideoList(videoItems) {
//   videoList.innerHTML = '';

//   videoItems.forEach(video => {
//     const videoTitle = video.snippet.title;
//     const videoThumbnail = video.snippet.thumbnails.default.url;
//     const videoId = video.id.videoId;

//     const videoElement = document.createElement('div');
//     videoElement.classList.add('video-item');

//     const thumbnailElement = document.createElement('img');
//     thumbnailElement.src = videoThumbnail;
//     thumbnailElement.alt = videoTitle;

//     const titleElement = document.createElement('h3');
//     titleElement.textContent = videoTitle;
//     titleElement.addEventListener('click', () => {
//       const pipedUrl = `https://piped.video/${videoId}`;
//       window.open(pipedUrl, '_blank');
//     });

//     videoElement.appendChild(thumbnailElement);
//     videoElement.appendChild(titleElement);

//     videoList.appendChild(videoElement);
//   });
// }
// ------------------
const API_KEY = 'AIzaSyD_nl2Hzfq3vebmDD5g1WUJ5OHNHe27tyc';
const videoTitleInput = document.getElementById('video-title');
const searchBtn = document.getElementById('search-btn');
const videoList = document.getElementById('video-list');
const videoPlayer = document.getElementById('video-player');

searchBtn.addEventListener('click', fetchRelatedVideos);

function fetchRelatedVideos() {
  const videoTitle = videoTitleInput.value.trim();
  if (videoTitle === '') {
    alert('Please enter a video title.');
    return;
  }

  const maxResults = 10;
  const urlParams = new URLSearchParams({
    key: API_KEY,
    q: videoTitle,
    part: 'snippet',
    type: 'video',
    maxResults: maxResults,
  });

  const apiUrl = `https://www.googleapis.com/youtube/v3/search?${urlParams.toString()}`;

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      displayVideoList(data.items);
    })
    .catch(error => {
      console.error('Error fetching video data:', error);
    });
}

function displayVideoList(videoItems) {
  videoList.innerHTML = '';
  videoPlayer.innerHTML = ''; // Clear the video player

  videoItems.forEach(video => {
    const videoTitle = video.snippet.title;
    const videoThumbnail = video.snippet.thumbnails.default.url;
    const videoId = video.id.videoId;

    const videoElement = document.createElement('div');
    videoElement.classList.add('video-item');
    videoElement.addEventListener('click', () => {
      embedVideo(videoId);
    });

    const thumbnailElement = document.createElement('img');
    thumbnailElement.src = videoThumbnail;
    thumbnailElement.alt = videoTitle;

    const titleElement = document.createElement('h3');
    titleElement.textContent = videoTitle;

    videoElement.appendChild(thumbnailElement);
    videoElement.appendChild(titleElement);

    videoList.appendChild(videoElement);
  });
}

function embedVideo(videoId) {
  const pipedUrl = `https://piped.video/embed/${videoId}`;
  const playerHtml = `<iframe src="${pipedUrl}" width="640" height="360" frameborder="0" allowfullscreen></iframe>`;
  videoPlayer.innerHTML = playerHtml;
}