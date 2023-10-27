new WOW().init();

var $star_rating = $('.star-rating span');

var SetRatingStar = function() {
  return $star_rating.each(function() {
    if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
      return $(this).removeClass('disactive').addClass('active');
    } else {
      return $(this).removeClass('active').addClass('disactive');
    }
  });
};

$star_rating.on('click', function() {
  $star_rating.siblings('input.rating-value').val($(this).data('rating'));
  return SetRatingStar();
});

SetRatingStar();
$(document).ready(function() {
});


$(function() {
  $('.chosen-select').chosen();
});



$(".catalog-filter-more-search").click( function(){
  $(".catalog-filter-body").toggleClass("active")
  $(this).toggleClass("active")
})

$(".header-call-btn").click( function(){
  $(".header-call-btn-div").toggleClass("active")
})

$(document).on('click', '.default-video-div', function() {
	var $video = $('.default-video'),
	src = $video.attr('src');
   $video.attr('src', src + '&autoplay=1');
   $(".default-video-div").addClass("played")
});

var swiper = new Swiper('.catalog-item-services', {
  slidesPerView: 4,
  spaceBetween: 30,
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      // when window width is >= 320px
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },
      // when window width is >= 480px
      480: {
        slidesPerView: 1,
        spaceBetween: 30
      },
      // when window width is >= 640px
      640: {
        slidesPerView: 2,
        spaceBetween: 30
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 30
      },
      1200: {
          slidesPerView: 4,
          spaceBetween: 30
      }
    }
});


var swiper = new Swiper('.catalog-item-sale', {
  slidesPerView: 4,
  spaceBetween: 30,
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      // when window width is >= 320px
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },
      // when window width is >= 480px
      480: {
        slidesPerView: 1,
        spaceBetween: 30
      },
      // when window width is >= 640px
      640: {
        slidesPerView: 2,
        spaceBetween: 30
      },
      992: {
        slidesPerView: 4,
        spaceBetween: 30
      },
      1700: {
          slidesPerView: 5,
          spaceBetween: 30
      }
    }
});




var prevScrollpos = window.pageYOffset;
window.onscroll = function(){
    var currentScrollPos = window.pageYOffset;
    if(prevScrollpos > currentScrollPos){
        document.getElementById("navbar").style.top = "0px";
    }else if(currentScrollPos == 0){
        document.getElementById("navbar").style.top = "0px";
    }else{
        document.getElementById("navbar").style.top = "-150px";
    }
    prevScrollpos = currentScrollPos;


    
var scrolled;
    scrolled = window.pageYOffset || document.documentElement.scrollTop;
        if(scrolled > 10){
            $("#navbar").addClass('active');
            $("#navbar").removeClass('nonactive');
            $("#burger").addClass('active');
            $("#burger").removeClass('nonactive');
        }
        if(10 > scrolled){
            $("#navbar").addClass('nonactive');
            $("#navbar").removeClass('active'); 
            $("#burger").addClass('nonactive');
            $("#burger").removeClass('active'); 
        }
}


let burger = document.getElementById('burger'),
	 nav    = document.getElementById('main-nav');

burger.addEventListener('click', function(e){
	this.classList.toggle('is-open');
	nav.classList.toggle('is-open');
});











//Ymap start
var spinner = $('.ymap-container').children('.loader');
var check_if_load = 0;
var myMapTemp, myPlacemarkTemp;


function init () {
  var myMapTemp = new ymaps.Map("map-yandex", {
    center: [51.131480, 71.428965],
    zoom: 15,
    controls: ['zoomControl', 'fullscreenControl']
  });

  var myPlacemarkTemp = new ymaps.Placemark([51.131480, 71.428965], {
      balloonContent: "  Рі. РђР»РјР°С‚С‹, СѓР».Р Р°РґР»РѕРІР° 25, 2 СЌС‚Р°Р¶",
  }, {
      iconLayout: 'default#imageWithContent',
      
      iconImageHref: 'img/map-marker.png',
      
      iconImageSize: [50, 50],

      iconImageOffset: [-25, -50],
  });
  
  myMapTemp.geoObjects.add(myPlacemarkTemp);
  var layer = myMapTemp.layers.get(0).get(0);
  waitForTilesLoad(layer).then(function() {
    
    spinner.removeClass('is-active');
  });
}

function waitForTilesLoad(layer) {
  return new ymaps.vow.Promise(function (resolve, reject) {
    var tc = getTileContainer(layer), readyAll = true;
    tc.tiles.each(function (tile, number) {
      if (!tile.isReady()) {
        readyAll = false;
      }
    });
    if (readyAll) {
      resolve();
    } else {
      tc.events.once("ready", function() {
        resolve();
      });
    }
  });
}

function getTileContainer(layer) {
  for (var k in layer) {
    if (layer.hasOwnProperty(k)) {
      if (
        layer[k] instanceof ymaps.layer.tileContainer.CanvasContainer
        || layer[k] instanceof ymaps.layer.tileContainer.DomContainer
      ) {
        return layer[k];
      }
    }
  }
  return null;
}

function loadScript(url, callback){

  var script = document.createElement("script");

  if (script.readyState){  
    script.onreadystatechange = function(){
      if (script.readyState == "loaded" ||
              script.readyState == "complete"){
        script.onreadystatechange = null;
        callback();
      }
    };
  } else {  
    script.onload = function(){
      callback();
    };
  }

  script.src = url;
  document.getElementsByTagName("head")[0].appendChild(script);
}

var ymap = function() {
  $('.ymap-container').click(function(){
      if (check_if_load == 0) {
        check_if_load = 1;

        spinner.addClass('is-active');

        loadScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU&amp;loadByRequire=1", function(){
            ymaps.load(init);
        });         
        
      }
    }
  );  
}

$(function() {
  ymap();
});










