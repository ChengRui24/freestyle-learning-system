(function () {
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".side nav a"));
  var sections = navLinks
    .map(function (a) {
      return document.querySelector(a.getAttribute("href"));
    })
    .filter(Boolean);
  var io = new IntersectionObserver(
    function (entries) {
      var vis = entries
        .filter(function (x) {
          return x.isIntersecting;
        })
        .sort(function (a, b) {
          return b.intersectionRatio - a.intersectionRatio;
        })[0];
      if (!vis) return;
      navLinks.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href") === "#" + vis.target.id);
      });
    },
    { rootMargin: "-20% 0px -70% 0px", threshold: [0, 0.2, 0.5] }
  );
  sections.forEach(function (s) {
    io.observe(s);
  });

  function scrollToHash() {
    var id = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (!id) return;
    var el = document.getElementById(id);
    if (el) el.scrollIntoView();
  }

  window.addEventListener("hashchange", scrollToHash);
  window.addEventListener("load", scrollToHash);
  scrollToHash();
  setTimeout(scrollToHash, 0);
  setTimeout(scrollToHash, 50);
  setTimeout(scrollToHash, 300);
})();
