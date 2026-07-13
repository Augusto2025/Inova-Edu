const slides = document.querySelector('.slides');
const total = document.querySelectorAll('.slides img').length;

let index = 0;

setInterval(() => {

    index++;

    slides.style.transition = "transform 1s ease";
    slides.style.transform = `translateX(-${index * 100}vw)`;

    if(index === total - 1){

        setTimeout(() => {

            slides.style.transition = "none";
            index = 0;
            slides.style.transform = `translateX(0)`;

        },1000);

    }

},5000);