      
const img = document.getElementById('Stream');
const btnCamara = document.getElementById('btnCamara');
const btnImg = document.getElementById('btnImg');
const btnVideo = document.getElementById('btnVideo');

btnCamara.addEventListener('click', () => {
    img.src = "http://localhost:8000/stream"
});

btnVideo.addEventListener('click', () => {
    img.src = "http://localhost:8000/video"
});

btnImg.addEventListener('click', () => {
    img.src = "http://localhost:8000/imagen"
});

