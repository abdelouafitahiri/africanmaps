setTimeout(function () {
    var _0xebf0x1 = document.getElementById("preloader");
    if (_0xebf0x1) {
      _0xebf0x1.classList.add("preloader-hide");
    }
  }, 150);
  document.addEventListener("DOMContentLoaded", () => {
    ("use strict");
    let _0xebf0x2 = true;
    let _0xebf0x3 = true;
    var _0xebf0x4 = "PayApp";
    var _0xebf0x5 = 1;
    var _0xebf0x6 = false;
    var _0xebf0x7 = "https://www.enableds.com/products/payapp/v13/";
    var _0xebf0x8 = "https://www.enableds.com/products/payapp/v13/_service-worker.js";
    function _0xebf0x9() {
      var _0xebf0xa, _0xebf0xb, _0xebf0xc, _0xebf0xd, _0xebf0xe;
      var _0xebf0xf = document.querySelectorAll(".card-stack .card");
      if (_0xebf0xf[0]) {
        var _0xebf0x10 = document.querySelectorAll(".card-stack")[0].getAttribute("data-stack-height");
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0xf.length; _0xebf0xa++) {
          _0xebf0xf[_0xebf0xa].style.height = +_0xebf0x10 + 20 + "px";
          _0xebf0xf[_0xebf0xa].style.marginBottom = -1 * +_0xebf0x10 + "px";
          _0xebf0xf[_0xebf0xa].style.zIndex = 70 - _0xebf0xa;
          _0xebf0xf[_0xebf0xa].style.transform = "scale(0." + (99 - _0xebf0xa * 10) + ")";
        }
        ;
        var _0xebf0x11 = document.querySelectorAll(".btn-stack-click")[0];
        var _0xebf0x12 = document.querySelectorAll(".card-stack-click")[0];
        var _0xebf0x13 = document.querySelectorAll(".card-stack")[0];
        var _0xebf0x14 = document.querySelectorAll(".btn-stack-info")[0];
        function _0xebf0x15() {
          if (_0xebf0x13.classList.contains("card-stack-active")) {
            _0xebf0x14.classList.remove("disabled");
            _0xebf0x11.classList.add("disabled");
            _0xebf0x12.classList.remove("no-click");
            _0xebf0x13.classList.remove("card-stack-active");
          } else {
            _0xebf0x14.classList.add("disabled");
            _0xebf0x11.classList.remove("disabled");
            _0xebf0x12.classList.add("no-click");
            _0xebf0x13.classList.add("card-stack-active");
          }
        }
        _0xebf0x12.addEventListener("click", function (_0xebf0xb) {
          _0xebf0x15();
        });
        _0xebf0x11.addEventListener("click", function (_0xebf0xb) {
          _0xebf0x15();
        });
      }
      ;
      document.querySelectorAll("#page")[0].style.display = "block";
      var _0xebf0x16 = document.getElementsByClassName("splide");
      if (_0xebf0x16.length) {
        var _0xebf0x17 = document.querySelectorAll(".single-slider");
        if (_0xebf0x17.length) {
          _0xebf0x17.forEach(function (_0xebf0xb) {
            var _0xebf0x18 = new Splide("#" + _0xebf0xb.id, {type: "loop", autoplay: true, interval: 4e3, perPage: 1}).mount();
            var _0xebf0x19 = document.querySelectorAll(".slider-next");
            var _0xebf0x1a = document.querySelectorAll(".slider-prev");
            _0xebf0x19.forEach(_0xebf0xc => {
              return _0xebf0xc.addEventListener("click", _0xebf0xc => {
                _0xebf0x18.go(">");
              });
            });
            _0xebf0x1a.forEach(_0xebf0xc => {
              return _0xebf0xc.addEventListener("click", _0xebf0xc => {
                _0xebf0x18.go("<");
              });
            });
          });
        }
        ;
        var _0xebf0x1b = document.querySelectorAll(".double-slider");
        if (_0xebf0x1b.length) {
          _0xebf0x1b.forEach(function (_0xebf0xb) {
            var _0xebf0x1c = new Splide("#" + _0xebf0xb.id, {type: "loop", autoplay: true, interval: 4e3, arrows: false, perPage: 2}).mount();
          });
        }
        ;
        var _0xebf0x1d = document.querySelectorAll(".triple-slider");
        if (_0xebf0x1d.length) {
          _0xebf0x1d.forEach(function (_0xebf0xb) {
            var _0xebf0x1e = new Splide("#" + _0xebf0xb.id, {type: "loop", autoplay: true, interval: 4e3, arrows: false, perPage: 3, perMove: 1}).mount();
          });
        }
        ;
        var _0xebf0x1f = document.querySelectorAll(".quad-slider");
        if (_0xebf0x1f.length) {
          _0xebf0x1f.forEach(function (_0xebf0xb) {
            var _0xebf0x20 = new Splide("#" + _0xebf0xb.id, {type: "loop", autoplay: true, interval: 4e3, arrows: false, perPage: 4, perMove: 1}).mount();
          });
        }
      }
      ;
      const _0xebf0x21 = document.querySelectorAll('a[href="#"]');
      _0xebf0x21.forEach(_0xebf0xc => {
        return _0xebf0xc.addEventListener("click", _0xebf0xb => {
          _0xebf0xb.preventDefault();
          return false;
        });
      });
      function _0xebf0x22() {
        var _0xebf0x23 = document.querySelectorAll("[data-submenu]");
        if (_0xebf0x23.length) {
          var _0xebf0x24 = document.querySelectorAll(".submenu-active")[0];
          if (_0xebf0x24) {
            var _0xebf0x25 = document.querySelectorAll(".submenu-active")[0].getAttribute("data-submenu");
            var _0xebf0x26 = document.querySelectorAll("#" + _0xebf0x25);
            var _0xebf0x27 = document.querySelectorAll("#" + _0xebf0x25 + " a");
            var _0xebf0x28 = _0xebf0x27.length;
            var _0xebf0x29 = _0xebf0x28 * 43;
            _0xebf0x26[0].style.height = _0xebf0x29 + "px";
          }
          ;
          _0xebf0x23.forEach(_0xebf0xc => {
            return _0xebf0xc.addEventListener("click", _0xebf0xb => {
              const _0xebf0x25 = _0xebf0xc.getAttribute("data-submenu");
              var _0xebf0x26 = document.querySelectorAll("#" + _0xebf0x25);
              var _0xebf0x27 = document.querySelectorAll("#" + _0xebf0x25 + " a");
              var _0xebf0x28 = _0xebf0x27.length;
              var _0xebf0x29 = _0xebf0x28 * 43;
              if (_0xebf0xc.classList.contains("submenu-active")) {
                _0xebf0x26[0].style.height = "0px";
                _0xebf0xc.classList.remove("submenu-active");
              } else {
                _0xebf0x26[0].style.height = _0xebf0x29 + "px";
                _0xebf0xc.classList.add("submenu-active");
              }
              ;
              return false;
            });
          });
        }
      }
      function _0xebf0x2a() {
        var _0xebf0x2b = document.querySelectorAll("[data-menu-active]");
        if (_0xebf0x2b) {
          var _0xebf0x2c = _0xebf0x2b[0].getAttribute("data-menu-active");
          var _0xebf0x2d = document.querySelectorAll("#" + _0xebf0x2c)[0];
          _0xebf0x2d.classList.add("list-group-item-active");
          if (_0xebf0x2d.parentNode.classList.contains("list-submenu")) {
            var _0xebf0x2e = _0xebf0x2d.parentNode.getAttribute("id");
            document.querySelectorAll('[data-submenu="' + _0xebf0x2e + '"]')[0].classList.add("submenu-active");
            _0xebf0x22();
          }
        }
      }
      var _0xebf0x2f = document.querySelectorAll("[data-search]");
      if (_0xebf0x2f.length) {
        var _0xebf0x30 = document.querySelectorAll(".search-results");
        var _0xebf0x31 = document.querySelectorAll(".search-no-results");
        var _0xebf0x32 = document.querySelectorAll(".search-results div")[0].childElementCount;
        function _0xebf0x33() {
          var _0xebf0x34 = _0xebf0x2f[0].value;
          var _0xebf0x35 = _0xebf0x34.toLowerCase();
          if (_0xebf0x35 != "") {
            _0xebf0x30[0].classList.remove("disabled-search-list");
            var _0xebf0x36 = document.querySelectorAll("[data-filter-item]");
            for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x36.length; _0xebf0xa++) {
              var _0xebf0x37 = _0xebf0x36[_0xebf0xa].getAttribute("data-filter-name");
              if (_0xebf0x37.includes(_0xebf0x35)) {
                _0xebf0x36[_0xebf0xa].classList.remove("disabled");
              } else {
                _0xebf0x36[_0xebf0xa].classList.add("disabled");
              }
              ;
              var _0xebf0x38 = document.querySelectorAll(".search-results div")[0].getElementsByClassName("disabled").length;
              if (_0xebf0x38 === _0xebf0x32) {
                _0xebf0x31[0].classList.remove("disabled");
              } else {
                _0xebf0x31[0].classList.add("disabled");
              }
            }
          }
          ;
          if (_0xebf0x35 === "") {
            _0xebf0x30[0].classList.add("disabled-search-list");
            _0xebf0x31[0].classList.add("disabled");
            var _0xebf0x36 = document.querySelectorAll("[data-filter-item]");
            for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x36.length; _0xebf0xa++) {
              _0xebf0x36[_0xebf0xa].classList.remove("disabled");
            }
          }
          ;
          if (_0xebf0x35.length === 0) {
            _0xebf0x30[0].classList.add("disabled-search-list");
            _0xebf0x31[0].classList.add("disabled");
            var _0xebf0x36 = document.querySelectorAll("[data-filter-item]");
            for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x36.length; _0xebf0xa++) {
              _0xebf0x36[_0xebf0xa].classList.remove("disabled");
            }
          }
        }
        _0xebf0x2f[0].addEventListener("change", function () {
          _0xebf0x33();
        });
        _0xebf0x2f[0].addEventListener("keyup", function () {
          _0xebf0x33();
        });
        _0xebf0x2f[0].addEventListener("keydown", function () {
          _0xebf0x33();
        });
        _0xebf0x2f[0].addEventListener("click", function () {
          _0xebf0x33();
        });
      }
      ;
      const _0xebf0x39 = document.querySelectorAll("[data-back-button]");
      if (_0xebf0x39.length) {
        _0xebf0x39.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xb => {
            _0xebf0xb.stopPropagation;
            _0xebf0xb.preventDefault;
            window.history.go(-1);
          });
        });
      }
      ;
      var _0xebf0x3a = document.querySelectorAll("[data-auto-activate]")[0];
      if (_0xebf0x3a) {
        setTimeout(function () {
          var _0xebf0x3b = new bootstrap.Offcanvas(_0xebf0x3a);
          _0xebf0x3b.show();
        }, 600);
      }
      ;
      var _0xebf0x3c = document.querySelectorAll("[data-auto-hide-target]");
      _0xebf0x3c.forEach(_0xebf0xc => {
        return _0xebf0xc.addEventListener("click", _0xebf0xb => {
          var _0xebf0x3d = _0xebf0xc.getAttribute("data-auto-hide-target");
          var _0xebf0x3e = _0xebf0xc.getAttribute("data-auto-hide-time");
          var _0xebf0x3f = document.querySelectorAll(_0xebf0x3d)[0];
          var _0xebf0x40 = new bootstrap.Offcanvas(_0xebf0x3f);
          _0xebf0x40.show();
          setTimeout(function () {
            _0xebf0x40.hide();
          }, _0xebf0x3e);
        });
      });
      const _0xebf0x41 = document.getElementsByClassName("card");
      function _0xebf0x42() {
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x41.length; _0xebf0xa++) {
          if (_0xebf0x41[_0xebf0xa].getAttribute("data-card-height") === "cover") {
            if (window.matchMedia("(display-mode: fullscreen)").matches) {
              var _0xebf0x43 = window.outerHeight;
            }
            ;
            if (!window.matchMedia("(display-mode: fullscreen)").matches) {
              var _0xebf0x43 = window.innerHeight;
            }
            ;
            var _0xebf0x44 = _0xebf0x43 + "px";
          }
          ;
          if (_0xebf0x41[_0xebf0xa].hasAttribute("data-card-height")) {
            var _0xebf0x45 = _0xebf0x41[_0xebf0xa].getAttribute("data-card-height");
            _0xebf0x41[_0xebf0xa].style.height = _0xebf0x45 + "px";
            if (_0xebf0x45 === "cover") {
              var _0xebf0x46 = _0xebf0x45;
              _0xebf0x41[_0xebf0xa].style.height = _0xebf0x44;
            }
          }
        }
      }
      if (_0xebf0x41.length) {
        _0xebf0x42();
        window.addEventListener("resize", _0xebf0x42);
      }
      ;
      function _0xebf0x47() {
        var _0xebf0x48 = document.querySelectorAll("[data-toggle-theme]");
        function _0xebf0x49() {
          document.getElementById("theme-check").setAttribute("content", "#1f1f1f");
          document.body.classList.add("theme-dark");
          document.body.classList.remove("theme-light", "detect-theme");
          for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x48.length; _0xebf0xa++) {
            _0xebf0x48[_0xebf0xa].checked = "checked";
          }
          ;
          localStorage.setItem(_0xebf0x4 + "-Theme", "dark-mode");
          _0xebf0x51();
          setTimeout(function () {
            _0xebf0x52();
          }, 650);
        }
        function _0xebf0x4a() {
          document.getElementById("theme-check").setAttribute("content", "#FFFFFF");
          document.body.classList.add("theme-light");
          document.body.classList.remove("theme-dark", "detect-theme");
          for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x48.length; _0xebf0xa++) {
            _0xebf0x48[_0xebf0xa].checked = false;
          }
          ;
          localStorage.setItem(_0xebf0x4 + "-Theme", "light-mode");
          _0xebf0x51();
          setTimeout(function () {
            _0xebf0x52();
          }, 650);
        }
        function _0xebf0x4b() {
          const _0xebf0x4c = window.matchMedia("(prefers-color-scheme: dark)").matches;
          const _0xebf0x4d = window.matchMedia("(prefers-color-scheme: light)").matches;
          const _0xebf0x4e = window.matchMedia("(prefers-color-scheme: no-preference)").matches;
          window.matchMedia("(prefers-color-scheme: dark)").addListener(_0xebf0xb => {
            return _0xebf0xb.matches && _0xebf0x49();
          });
          window.matchMedia("(prefers-color-scheme: light)").addListener(_0xebf0xb => {
            return _0xebf0xb.matches && _0xebf0x4a();
          });
          if (_0xebf0x4c) {
            _0xebf0x49();
          }
          ;
          if (_0xebf0x4d) {
            _0xebf0x4a();
          }
        }
        var _0xebf0x4f = document.querySelectorAll("[data-toggle-theme]");
        _0xebf0x4f.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xb => {
            if (document.body.className == "theme-light") {
              _0xebf0x51();
              _0xebf0x49();
            } else {
              if (document.body.className == "theme-dark") {
                _0xebf0x51();
                _0xebf0x4a();
              }
            }
            ;
            setTimeout(function () {
              _0xebf0x52();
            }, 350);
          });
        });
        if (localStorage.getItem(_0xebf0x4 + "-Theme") == "dark-mode") {
          for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x48.length; _0xebf0xa++) {
            _0xebf0x48[_0xebf0xa].checked = "checked";
          }
          ;
          document.body.className = "theme-dark";
        }
        ;
        if (localStorage.getItem(_0xebf0x4 + "-Theme") == "light-mode") {
          document.body.className = "theme-light";
        }
        ;
        if (document.body.className == "detect-theme") {
          _0xebf0x4b();
        }
        ;
        const _0xebf0x50 = document.querySelectorAll(".detect-dark-mode");
        _0xebf0x50.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xb => {
            document.body.classList.remove("theme-light", "theme-dark");
            document.body.classList.add("detect-theme");
            setTimeout(function () {
              _0xebf0x4b();
            }, 50);
          });
        });
        function _0xebf0x51() {
          document.body.classList.add("no-ani");
        }
        function _0xebf0x52() {
          document.body.classList.remove("no-ani");
        }
      }
      _0xebf0x47();
      const _0xebf0x53 = document.getElementsByClassName("upload-file");
      if (_0xebf0x53.length) {
        _0xebf0x53[0].addEventListener("change", _0xebf0x54, false);
        function _0xebf0x54(_0xebf0xe) {
          if (this.files && this.files[0]) {
            var _0xebf0x55 = document.getElementById("image-data");
            _0xebf0x55.src = URL.createObjectURL(this.files[0]);
            _0xebf0x55.classList.add("mt-4", "mb-3", "mx-auto");
          }
          ;
          const _0xebf0x56 = _0xebf0xe.target.files;
          const _0xebf0x57 = _0xebf0x56[0].name;
          const _0xebf0x58 = (_0xebf0x56[0].size / 1e3).toFixed(2) + "kb";
          const _0xebf0x59 = document.getElementsByClassName("upload-file-name")[0].getAttribute("data-text-before");
          const _0xebf0x5a = document.getElementsByClassName("upload-file-name")[0].getAttribute("data-text-after");
          document.getElementsByClassName("upload-file-name")[0].innerHTML = _0xebf0x59 + " " + _0xebf0x57 + " - " + _0xebf0x58 + " - " + _0xebf0x5a;
          document.getElementsByClassName("upload-file-name")[0].classList.add("pb-3");
        }
      }
      ;
      var _0xebf0x5b = document.querySelectorAll(".offcanvas");
      if (_0xebf0x5b) {
        setTimeout(function () {
          _0xebf0x5b.forEach(function (_0xebf0xb) {
            _0xebf0xb.style.display = "block";
          });
        }, 250);
      }
      ;
      var _0xebf0x5c = document.querySelectorAll("[data-menu-load]");
      _0xebf0x5c.forEach(function (_0xebf0xb) {
        var _0xebf0x5d = _0xebf0xb.getAttribute("data-menu-load");
        fetch(_0xebf0x5d).then(_0xebf0x5e => {
          return _0xebf0x5e.text();
        }).then(_0xebf0x5f => {
          return _0xebf0xb.innerHTML = _0xebf0x5f;
        }).then(_0xebf0x5e => {
          setTimeout(function () {
            if (_0xebf0x5c[_0xebf0x5c.length - 1] === _0xebf0xb) {
              _0xebf0x47();
              _0xebf0x22();
              _0xebf0xb1();
              _0xebf0x2a();
            }
          }, 500);
        }).catch(function () {
          _0xebf0xb.innerHTML = "<h5 class='font-16 px-4 py-4 mb-0'>Please use a Local Server such as AMPPS or WAMP to see externally loaded menus or put " + _0xebf0x4 + " files on your server. <br> To load menus from inside your HTML you must remove the data-menu-load=`your-menu.html` and copy what is inside your-menu.html in this div. <br>Using external menus, editing a single menu will show in all pages. <br><br> For more information please read the Documentation -> Menu Chapter.</h5>";
        });
      });
      var _0xebf0x60 = document.querySelectorAll(".check-visited");
      if (_0xebf0x60) {
        function _0xebf0x61() {
          var _0xebf0x62 = JSON.parse(localStorage.getItem(_0xebf0x4 + "_Visited_Links")) || [];
          var _0xebf0x63 = document.querySelectorAll(".check-visited a");
          for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x63.length; _0xebf0xa++) {
            var _0xebf0x64 = _0xebf0x63[_0xebf0xa];
            _0xebf0x64.addEventListener("click", function (_0xebf0xb) {
              var _0xebf0x65 = this.href;
              if (_0xebf0x62.indexOf(_0xebf0x65) == -1) {
                _0xebf0x62.push(_0xebf0x65);
                localStorage.setItem(_0xebf0x4 + "_Visited_Links", JSON.stringify(_0xebf0x62));
              }
            });
            if (_0xebf0x62.indexOf(_0xebf0x64.href) !== -1) {
              _0xebf0x64.className += " visited-link";
            }
          }
        }
        _0xebf0x61();
      }
      ;
      var _0xebf0x66 = document.querySelectorAll(".header-auto-show");
      if (_0xebf0x66.length) {
        var _0xebf0x67 = document.querySelectorAll(".header-auto-show");
        window.addEventListener("scroll", function () {
          if (document.querySelectorAll(".scroll-ad, .header-auto-show").length) {
            function _0xebf0x68() {
              _0xebf0x67[0].classList.add("header-active");
            }
            function _0xebf0x69() {
              _0xebf0x67[0].classList.remove("header-active");
            }
            var _0xebf0x6a = window.outerWidth;
            var _0xebf0x6b = document.documentElement.scrollTop;
            let _0xebf0x6c = _0xebf0x6b <= 30;
            var _0xebf0x6d = _0xebf0x6b >= 30;
            let _0xebf0x6e = _0xebf0x6a - _0xebf0x6b + 1e3 <= 150;
            if (_0xebf0x67.length) {
              _0xebf0x6c ? _0xebf0x69() : null;
              _0xebf0x6d ? _0xebf0x68() : null;
            }
          }
        });
      }
      ;
      var _0xebf0x6f = document.querySelectorAll(".stepper-add");
      var _0xebf0x70 = document.querySelectorAll(".stepper-sub");
      if (_0xebf0x6f.length) {
        _0xebf0x6f.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xe => {
            var _0xebf0x71 = _0xebf0xc.parentElement.querySelector("input").value;
            _0xebf0xc.parentElement.querySelector("input").value = +_0xebf0x71 + 1;
          });
        });
        _0xebf0x70.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xe => {
            var _0xebf0x71 = _0xebf0xc.parentElement.querySelector("input").value;
            _0xebf0xc.parentElement.querySelector("input").value = +_0xebf0x71 - 1;
          });
        });
      }
      ;
      var _0xebf0x72 = document.querySelectorAll("[data-trigger-switch]:not([data-toggle-theme])");
      if (_0xebf0x72.length) {
        _0xebf0x72.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xe => {
            var _0xebf0x73 = _0xebf0xc.getAttribute("data-trigger-switch");
            _0xebf0xc.classList.add("no-click");
            setTimeout(function () {
              _0xebf0xc.classList.remove("no-click");
            }, 270);
            var _0xebf0x74 = document.getElementById(_0xebf0x73);
            _0xebf0x74.checked ? _0xebf0x74.checked = false : _0xebf0x74.checked = true;
          });
        });
      }
      ;
      var _0xebf0x75 = document.querySelectorAll(".header-date")[0];
      if (_0xebf0x75) {
        var _0xebf0x76 = new Date;
        var _0xebf0x77 = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        var _0xebf0x78 = new Date;
        var _0xebf0x79 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        var _0xebf0x7a = new Date;
        var _0xebf0x7b = _0xebf0x7a.getDate();
        var _0xebf0x7c = "th";
        if (_0xebf0x7b === 1) {
          _0xebf0x7c = "st";
        }
        ;
        if (_0xebf0x7b === 2) {
          _0xebf0x7c = "nd";
        }
        ;
        if (_0xebf0x7b === 3) {
          _0xebf0x7c = "rd";
        }
        ;
        if (_0xebf0x7b === 21) {
          _0xebf0x7c = "st";
        }
        ;
        if (_0xebf0x7b === 22) {
          _0xebf0x7c = "nd";
        }
        ;
        if (_0xebf0x7b === 22) {
          _0xebf0x7c = "rd";
        }
        ;
        if (_0xebf0x7b === 31) {
          _0xebf0x7c = "st";
        }
        ;
        _0xebf0x75.innerHTML += _0xebf0x77[_0xebf0x76.getDay()] + " " + _0xebf0x7b + _0xebf0x7c + " " + _0xebf0x79[_0xebf0x78.getMonth()];
      }
      ;
      var _0xebf0x7d = document.querySelectorAll(".needs-validation");
      Array.prototype.slice.call(_0xebf0x7d).forEach(function (_0xebf0x7d) {
        _0xebf0x7d.addEventListener("submit", function (_0xebf0xe) {
          if (!_0xebf0x7d.checkValidity()) {
            _0xebf0xe.preventDefault();
            _0xebf0xe.stopPropagation();
          } else {
            _0xebf0xe.preventDefault();
            _0xebf0xe.stopPropagation();
            qrFunction(_0xebf0xe);
          }
          ;
          _0xebf0x7d.classList.add("was-validated");
        }, false);
      });
      var _0xebf0x7e = document.querySelectorAll(".form-label input, .form-label select, .form-label textarea");
      _0xebf0x7e.forEach(_0xebf0xc => {
        return _0xebf0xc.addEventListener("input", _0xebf0xe => {
          if (_0xebf0xc.value == "") {
            _0xebf0xc.parentElement.querySelectorAll("label")[0].classList.remove("form-label-active");
          }
          ;
          if (_0xebf0xc.value !== "") {
            _0xebf0xc.parentElement.querySelectorAll("label")[0].classList.add("form-label-active");
          }
        });
      });
      setTimeout(function () {
        var _0xebf0x7f = document.querySelectorAll(".copyright-year");
        if (_0xebf0x7f) {
          _0xebf0x7f.forEach(function (_0xebf0xb) {
            var _0xebf0x80 = new Date;
            const _0xebf0x81 = _0xebf0x80.getFullYear();
            _0xebf0xb.textContent = _0xebf0x81;
          });
        }
      }, 500);
      var _0xebf0x82 = document.querySelectorAll(".offline-message");
      if (!_0xebf0x82.length) {
        const _0xebf0x83 = document.createElement("p");
        const _0xebf0x84 = document.createElement("p");
        _0xebf0x83.className = "offline-message bg-red-dark shadow-bg shadow-bg-s color-white";
        _0xebf0x83.innerHTML = '<i class="bi bi-wifi-off pe-2"></i> No internet connection detected';
        _0xebf0x84.className = "online-message bg-green-dark shadow-bg shadow-bg-s color-white";
        _0xebf0x84.innerHTML = '<i class="bi bi-wifi pe-2"></i> You are back online.';
        document.querySelectorAll("#page")[0].appendChild(_0xebf0x83);
        document.querySelectorAll("#page")[0].appendChild(_0xebf0x84);
      }
      ;
      function _0xebf0x85() {
        var _0xebf0x86 = document.querySelectorAll("a");
        _0xebf0x86.forEach(function (_0xebf0xb) {
          var _0xebf0x87 = _0xebf0xb.getAttribute("href");
          if (_0xebf0x87.match(/.html/)) {
            _0xebf0xb.classList.add("show-offline");
            _0xebf0xb.setAttribute("data-link", _0xebf0x87);
            _0xebf0xb.setAttribute("href", "#");
          }
        });
        var _0xebf0x88 = document.querySelectorAll(".show-offline");
        _0xebf0x88.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xe => {
            document.getElementsByClassName("offline-message")[0].classList.add("offline-message-active");
            setTimeout(function () {
              document.getElementsByClassName("offline-message")[0].classList.remove("offline-message-active");
            }, 1500);
          });
        });
      }
      function _0xebf0x89() {
        var _0xebf0x8a = document.querySelectorAll("[data-link]");
        _0xebf0x8a.forEach(function (_0xebf0xb) {
          var _0xebf0x87 = _0xebf0xb.getAttribute("data-link");
          if (_0xebf0x87.match(/.html/)) {
            _0xebf0xb.setAttribute("href", _0xebf0x87);
            _0xebf0xb.removeAttribute("data-link", "");
          }
        });
      }
      var _0xebf0x8b = document.getElementsByClassName("offline-message")[0];
      var _0xebf0x8c = document.getElementsByClassName("online-message")[0];
      function _0xebf0x8d() {
        _0xebf0x89();
        _0xebf0x8b.classList.remove("offline-message-active");
        _0xebf0x8c.classList.add("online-message-active");
        setTimeout(function () {
          _0xebf0x8c.classList.remove("online-message-active");
        }, 2e3);
        console.info("Connection: Online");
      }
      function _0xebf0x8e() {
        _0xebf0x85();
        _0xebf0x8c.classList.remove("online-message-active");
        _0xebf0x8b.classList.add("offline-message-active");
        setTimeout(function () {
          _0xebf0x8b.classList.remove("offline-message-active");
        }, 2e3);
        console.info("Connection: Offline");
      }
      var _0xebf0x8f = document.querySelectorAll(".simulate-offline");
      var _0xebf0x90 = document.querySelectorAll(".simulate-online");
      if (_0xebf0x8f.length) {
        _0xebf0x8f[0].addEventListener("click", function () {
          _0xebf0x8e();
        });
        _0xebf0x90[0].addEventListener("click", function () {
          _0xebf0x8d();
        });
      }
      ;
      function _0xebf0x91(_0xebf0xe) {
        var _0xebf0x92 = navigator.onLine ? "online" : "offline";
        _0xebf0x8d();
      }
      function _0xebf0x93(_0xebf0xe) {
        _0xebf0x8e();
      }
      window.addEventListener("online", _0xebf0x91);
      window.addEventListener("offline", _0xebf0x93);
      let _0xebf0x94 = {Android: function () {
        return navigator.userAgent.match(/Android/i);
      }, iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
      }, any: function () {
        return _0xebf0x94.Android() || _0xebf0x94.iOS();
      }};
      function _0xebf0x95() {
        if (/iP(hone|od|ad)/.test(navigator.platform)) {
          var _0xebf0x96 = navigator.appVersion.match(/OS (\d+)_(\d+)_?(\d+)?/);
          return [parseInt(_0xebf0x96[1], 10)];
        }
      }
      const _0xebf0x97 = document.getElementsByClassName("show-android");
      const _0xebf0x98 = document.getElementsByClassName("show-ios");
      const _0xebf0x99 = document.getElementsByClassName("show-no-device");
      if (!_0xebf0x94.any()) {
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x98.length; _0xebf0xa++) {
          _0xebf0x98[_0xebf0xa].classList.add("disabled");
        }
        ;
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x97.length; _0xebf0xa++) {
          _0xebf0x97[_0xebf0xa].classList.add("disabled");
        }
      }
      ;
      if (_0xebf0x94.iOS()) {
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x99.length; _0xebf0xa++) {
          _0xebf0x99[_0xebf0xa].classList.add("disabled");
        }
        ;
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x97.length; _0xebf0xa++) {
          _0xebf0x97[_0xebf0xa].classList.add("disabled");
        }
        ;
        var _0xebf0x9a = _0xebf0x95();
        if (_0xebf0x9a > 15) {}
      }
      ;
      if (_0xebf0x94.Android()) {
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x98.length; _0xebf0xa++) {
          _0xebf0x98[_0xebf0xa].classList.add("disabled");
        }
        ;
        for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0x99.length; _0xebf0xa++) {
          _0xebf0x99[_0xebf0xa].classList.add("disabled");
        }
      }
      ;
      function _0xebf0x9b() {
        (function (_0xebf0x9c, _0xebf0x9d, _0xebf0x9e) {
          if (_0xebf0x9e in _0xebf0x9d && _0xebf0x9d[_0xebf0x9e]) {
            var _0xebf0x9f, _0xebf0xb = _0xebf0x9c.location, _0xebf0xa0 = /^(a|html)$/i;
            _0xebf0x9c.addEventListener("click", function (_0xebf0x9c) {
              _0xebf0x9f = _0xebf0x9c.target;
              while (!_0xebf0xa0.test(_0xebf0x9f.nodeName)) {
                _0xebf0x9f = _0xebf0x9f.parentNode;
              }
              ;
              "href" in _0xebf0x9f && (_0xebf0x9f.href.indexOf("http") || ~_0xebf0x9f.href.indexOf(_0xebf0xb.host)) && (_0xebf0x9c.preventDefault(), _0xebf0xb.href = _0xebf0x9f.href);
            }, false);
            document.querySelectorAll(".page-content")[0].classList.add("is-on-homescreen");
            setTimeout(function () {
              document.querySelectorAll("#footer-bar")[0].classList.remove("iosTabBar");
            }, 50);
          }
        }(document, window.navigator, "standalone"));
      }
      _0xebf0x9b();
      if (_0xebf0x2 === true) {
        var _0xebf0xa1 = document.querySelectorAll("#menu-install-pwa-ios")[0];
        if (_0xebf0xa1) {
          var _0xebf0xa2 = new bootstrap.Offcanvas(_0xebf0xa1);
        }
        ;
        var _0xebf0xa3 = document.querySelectorAll("#menu-install-pwa-android")[0];
        if (_0xebf0xa3) {
          var _0xebf0xa4 = new bootstrap.Offcanvas(_0xebf0xa3);
        }
        ;
        var _0xebf0xa5 = document.getElementsByTagName("html")[0];
        if (!_0xebf0xa5.classList.contains("isPWA")) {
          if ("serviceWorker" in navigator) {
            window.addEventListener("load", function () {
              navigator.serviceWorker.register(_0xebf0x8, {scope: _0xebf0x7}).then(function (_0xebf0xa6) {
                _0xebf0xa6.update();
              });
            });
          }
          ;
          var _0xebf0xa7 = _0xebf0x5 * 24;
          var _0xebf0xa8 = Date.now();
          var _0xebf0xa9 = localStorage.getItem(_0xebf0x4 + "-PWA-Timeout-Value");
          if (_0xebf0xa9 == null) {
            localStorage.setItem(_0xebf0x4 + "-PWA-Timeout-Value", _0xebf0xa8);
          } else {
            if (_0xebf0xa8 - _0xebf0xa9 > _0xebf0xa7 * 60 * 60 * 1e3) {
              localStorage.removeItem(_0xebf0x4 + "-PWA-Prompt");
              localStorage.setItem(_0xebf0x4 + "-PWA-Timeout-Value", _0xebf0xa8);
            }
          }
          ;
          const _0xebf0xaa = document.querySelectorAll(".pwa-dismiss");
          _0xebf0xaa.forEach(_0xebf0xc => {
            return _0xebf0xc.addEventListener("click", _0xebf0xb => {
              const _0xebf0xab = document.querySelectorAll("#menu-install-pwa-android, #menu-install-pwa-ios");
              for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0xab.length; _0xebf0xa++) {
                _0xebf0xab[_0xebf0xa].classList.remove("menu-active");
              }
              ;
              localStorage.setItem(_0xebf0x4 + "-PWA-Timeout-Value", _0xebf0xa8);
              localStorage.setItem(_0xebf0x4 + "-PWA-Prompt", "install-rejected");
              console.log("PWA Install Rejected. Will Show Again in " + _0xebf0x5 + " Days");
            });
          });
          const _0xebf0xab = document.querySelectorAll("#menu-install-pwa-android, #menu-install-pwa-ios");
          if (_0xebf0xab.length) {
            if (_0xebf0x94.Android()) {
              if (localStorage.getItem(_0xebf0x4 + "-PWA-Prompt") != "install-rejected") {
                function _0xebf0xac() {
                  setTimeout(function () {
                    if (!window.matchMedia("(display-mode: fullscreen)").matches) {
                      console.log("Triggering PWA Window for Android");
                      _0xebf0xa4.show();
                    }
                  }, 3500);
                }
                var _0xebf0xad;
                window.addEventListener("beforeinstallprompt", _0xebf0xb => {
                  _0xebf0xb.preventDefault();
                  _0xebf0xad = _0xebf0xb;
                  _0xebf0xac();
                });
              }
              ;
              const _0xebf0xae = document.querySelectorAll(".pwa-install");
              _0xebf0xae.forEach(_0xebf0xc => {
                return _0xebf0xc.addEventListener("click", _0xebf0xb => {
                  _0xebf0xad.prompt();
                  _0xebf0xad.userChoice.then(_0xebf0xaf => {
                    if (_0xebf0xaf.outcome === "accepted") {
                      console.log("Added");
                    } else {
                      localStorage.setItem(_0xebf0x4 + "-PWA-Timeout-Value", _0xebf0xa8);
                      localStorage.setItem(_0xebf0x4 + "-PWA-Prompt", "install-rejected");
                      setTimeout(function () {
                        if (!window.matchMedia("(display-mode: fullscreen)").matches) {
                          _0xebf0xa4.show();
                        }
                      }, 50);
                    }
                    ;
                    _0xebf0xad = null;
                  });
                });
              });
              window.addEventListener("appinstalled", _0xebf0xd => {
                _0xebf0xa4.hide();
              });
            }
            ;
            if (_0xebf0x94.iOS()) {
              if (localStorage.getItem(_0xebf0x4 + "-PWA-Prompt") != "install-rejected") {
                setTimeout(function () {
                  if (!window.matchMedia("(display-mode: fullscreen)").matches) {
                    console.log("Triggering PWA Window for iOS");
                    _0xebf0xa2.show();
                  }
                }, 3500);
              }
            }
          }
        }
        ;
        _0xebf0xa5.setAttribute("class", "isPWA");
      }
      ;
      setTimeout(function () {
        var _0xebf0xb0 = document.body;
        _0xebf0xb0.removeAttribute("style");
      }, 100);
      function _0xebf0xb1() {
        var _0xebf0xb2 = document.querySelectorAll("[data-change-highlight]");
        _0xebf0xb2.forEach(_0xebf0xc => {
          return _0xebf0xc.addEventListener("click", _0xebf0xb => {
            var _0xebf0xb3 = _0xebf0xc.getAttribute("data-change-highlight");
            var _0xebf0xb4 = document.querySelectorAll(".page-highlight");
            if (_0xebf0xb4.length) {
              _0xebf0xb4.forEach(function (_0xebf0xb) {
                _0xebf0xb.remove();
              });
            }
            ;
            var _0xebf0xb5 = document.createElement("link");
            _0xebf0xb5.rel = "stylesheet";
            _0xebf0xb5.className = "page-highlight";
            _0xebf0xb5.type = "text/css";
            _0xebf0xb5.href = "styles/highlights/" + _0xebf0xb3 + ".css";
            document.getElementsByTagName("head")[0].appendChild(_0xebf0xb5);
            document.body.setAttribute("data-highlight", "highlight-" + _0xebf0xb3);
            localStorage.setItem(_0xebf0x4 + "-Highlight", _0xebf0xb3);
          });
        });
        var _0xebf0xb6 = localStorage.getItem(_0xebf0x4 + "-Highlight");
        if (_0xebf0xb6) {
          document.body.setAttribute("data-highlight", _0xebf0xb6);
          var _0xebf0xb5 = document.createElement("link");
          _0xebf0xb5.rel = "stylesheet";
          _0xebf0xb5.className = "page-highlight";
          _0xebf0xb5.type = "text/css";
          _0xebf0xb5.href = "styles/highlights/" + _0xebf0xb6 + ".css";
          if (!document.querySelectorAll(".page-highlight").length) {
            document.getElementsByTagName("head")[0].appendChild(_0xebf0xb5);
            document.body.setAttribute("data-highlight", "highlight-" + _0xebf0xb6);
          }
        }
      }
      _0xebf0xb1();
      var _0xebf0xb7 = new LazyLoad;
      var _0xebf0xb8, _0xebf0xb9, _0xebf0xba, _0xebf0xbb;
      var _0xebf0xbc = "plugins/";
      let _0xebf0xbd = [{id: "uniqueID", plug: "pluginName/plugin.js", call: "pluginName/pluginName-call.js", style: "pluginName/pluginName-style.css", trigger: ".pluginTriggerClass"}, {id: "apex-chart", plug: "apex/apexcharts.js", call: "apex/apex-call.js", trigger: ".chart"}, {id: "demo-functions", call: "demo/demo.js", trigger: ".demo-boxed"}];
      for (let _0xebf0xa = 0; _0xebf0xa < _0xebf0xbd.length; _0xebf0xa++) {
        if (document.querySelectorAll("." + _0xebf0xbd[_0xebf0xa].id + "-c").length) {
          document.querySelectorAll("." + _0xebf0xbd[_0xebf0xa].id + "-c")[0].remove();
        }
        ;
        var _0xebf0xbe = document.querySelectorAll(_0xebf0xbd[_0xebf0xa].trigger);
        if (_0xebf0xbe.length) {
          var _0xebf0xbf = document.getElementsByTagName("script")[1], _0xebf0xc0 = document.createElement("script");
          _0xebf0xc0.type = "text/javascript";
          _0xebf0xc0.className = _0xebf0xbd[_0xebf0xa].id + "-p";
          _0xebf0xc0.src = _0xebf0xbc + _0xebf0xbd[_0xebf0xa].plug;
          _0xebf0xc0.addEventListener("load", function () {
            if (_0xebf0xbd[_0xebf0xa].call !== undefined) {
              var _0xebf0xc1 = document.getElementsByTagName("script")[2], _0xebf0xc2 = document.createElement("script");
              _0xebf0xc2.type = "text/javascript";
              _0xebf0xc2.className = _0xebf0xbd[_0xebf0xa].id + "-c";
              _0xebf0xc2.src = _0xebf0xbc + _0xebf0xbd[_0xebf0xa].call;
              _0xebf0xc1.parentNode.insertBefore(_0xebf0xc2, _0xebf0xc1);
            }
          });
          if (!document.querySelectorAll("." + _0xebf0xbd[_0xebf0xa].id + "-p").length && _0xebf0xbd[_0xebf0xa].plug !== undefined) {
            _0xebf0xbf.parentNode.insertBefore(_0xebf0xc0, _0xebf0xbf);
          } else {
            setTimeout(function () {
              var _0xebf0xbf = document.getElementsByTagName("script")[1], _0xebf0xc0 = document.createElement("script");
              _0xebf0xc0.type = "text/javascript";
              _0xebf0xc0.className = _0xebf0xbd[_0xebf0xa].id + "-c";
              _0xebf0xc0.src = _0xebf0xbc + _0xebf0xbd[_0xebf0xa].call;
              _0xebf0xbf.parentNode.insertBefore(_0xebf0xc0, _0xebf0xbf);
            }, 50);
          }
          ;
          if (_0xebf0xbd[_0xebf0xa].style !== undefined) {
            if (!document.querySelectorAll("." + _0xebf0xbd[_0xebf0xa].id + "-s").length) {
              var _0xebf0xc3 = document.createElement("link");
              _0xebf0xc3.className = _0xebf0xbd[_0xebf0xa].id + "-s";
              _0xebf0xc3.rel = "stylesheet";
              _0xebf0xc3.type = "text/css";
              _0xebf0xc3.href = _0xebf0xbc + _0xebf0xbd[_0xebf0xa].style;
              document.getElementsByTagName("head")[0].appendChild(_0xebf0xc3);
            }
          }
        }
      }
    }
    if ("scrollRestoration" in window.history) {
      window.history.scrollRestoration = "manual";
    }
    ;
    if (_0xebf0x3 === true) {
      if (window.location.protocol !== "file:") {
        const _0xebf0xc4 = {containers: ["#page"], cache: false, animateHistoryBrowsing: false, plugins: [new SwupPreloadPlugin], linkSelector: 'a:not(.external-link):not(.default-link):not([href^="https"]):not([href^="http"]):not([data-gallery])'};
        const _0xebf0xc5 = new Swup(_0xebf0xc4);
        document.addEventListener("swup:pageView", _0xebf0xb => {
          _0xebf0x9();
        });
      }
    }
    ;
    _0xebf0x9();
  });
  