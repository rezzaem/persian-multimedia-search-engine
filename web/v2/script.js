const API_KEY = 'AIzaSyD_nl2Hzfq3vebmDD5g1WUJ5OHNHe27tyc';
const PERPLEXITY_API_KEY = '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';

const videoTitleInput = document.getElementById('video-title');
const searchBtn = document.getElementById('search-btn');
const videoList = document.getElementById('video-list');
const videoPlayer = document.getElementById('video-player');

searchBtn.addEventListener('click', handleUserInput);

function handleUserInput() {
  const userInput = videoTitleInput.value.trim();
  if (userInput === '') {
    alert('Please enter a video title.');
    return;
  }

  checkContentWithPerplexity(userInput)
    .then(isContentAllowed => {
      if (isContentAllowed) {
        fetchRelatedVideos(userInput);
      } else {
        displayContentRestrictedMessage();
      }
    })
    .catch(error => {
      console.error('Error checking content:', error);
    });
}

function checkContentWithPerplexity(content) {
  const options = {
    method: 'POST',
    
    headers: {
        accept: 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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' // Replace with your actual API key
      },
    body: JSON.stringify({
      model: 'llama-3-sonar-small-32k-online',
      messages: [
        { role: 'system', content: 'Check if the given content is against the laws of the Islamic Republic and if it is against just return :YES' },
        { role: 'user', content: content }
      ]
    })
  };

  return fetch('https://api.perplexity.ai/chat/completions', options)
    .then(response => response.json())
    .then(response => console.log(response))
    .then(data => {
      const perplexityResponse = data.result.response.content;
      return !perplexityResponse.includes('YES');
    })
    .catch(err => console.error(err));
}

function fetchRelatedVideos(videoTitle) {
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
  videoPlayer.innerHTML = '';

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

function displayContentRestrictedMessage() {
  videoList.innerHTML = '';
  videoPlayer.innerHTML = '';
  const messageElement = document.createElement('p');
  messageElement.textContent = 'Sorry, the content you input is against the laws of the Islamic Republic.';
  videoList.appendChild(messageElement);
}