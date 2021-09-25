var section2_swiper = new Swiper('.section2-swiper', {
    slidesPerView: 3,
    spaceBetween: 15,
    pagination: {
        el: '.section2-swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        640: {
            slidesPerView: 3,
            spaceBetween: 50,
        },
    }
});

var group_deals_swiper = new Swiper('.group-deals', {
    slidesPerView: 2,
    spaceBetween: 20,
    width: 1200,
    breakpoints: {
        375: {
            slidesPerView: 1,
            spaceBetween: 20,
            width: 340,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20,
            width: 1200,
        }
    }
});

var innovation_products_swiper = new Swiper('.innovation-products', {
    slidesPerView: 4,
    spaceBetween: 30,
    breakpoints: {
        375: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        640: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1024: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1280: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
    }
});

var creative_ideas_swiper = new Swiper('.creative-ideas', {
    slidesPerView: 4,
    spaceBetween: 30,
    breakpoints: {
        375: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        640: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1024: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1280: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
    }
});