document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value.trim();
    if (query === '') {
        alert('Please enter a video title.');
        return;
    }

    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Debug log
            displayVideoList(data.items);
        })
        .catch(error => {
            console.error('Error fetching video data:', error);
        });
});

function displayVideoList(videoItems) {
    const videoList = document.getElementById('video-list');
    const videoPlayer = document.getElementById('video-player');
    
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
    document.getElementById('video-player').innerHTML = playerHtml;
}
