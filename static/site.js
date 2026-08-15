/* Click-to-play for the episode grid.
 *
 * Six YouTube iframes on one page is several megabytes and a set of
 * third-party cookies that nobody asked for, on the page most likely to be
 * opened on a phone on mobile data. So each episode ships as a still with a
 * play control that is a real link to YouTube. This upgrades that link in
 * place: press it and the still is replaced by the player, already playing.
 *
 * Without JavaScript the links still work — they just open YouTube. That is
 * the whole fallback, and it needs no markup of its own.
 */
(function () {
  "use strict";

  var frames = document.querySelectorAll(".episode__frame[data-youtube]");
  if (!frames.length || !("replaceChildren" in Element.prototype)) return;

  frames.forEach(function (frame) {
    frame.addEventListener("click", function (event) {
      // Leave modified clicks alone: cmd/ctrl-click and middle-click mean
      // "open YouTube in a new tab", and hijacking them is rude.
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();

      var id = frame.getAttribute("data-youtube");
      var iframe = document.createElement("iframe");

      // nocookie, and autoplay only because a person just pressed play.
      iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) +
                   "?autoplay=1&rel=0&modestbranding=1&playsinline=1";
      iframe.title = frame.getAttribute("aria-label") || "Pioneer One episode";
      iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen";
      iframe.allowFullscreen = true;
      iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");

      frame.replaceChildren(iframe);
      frame.removeAttribute("href");
      frame.removeAttribute("aria-label");
      iframe.focus({ preventScroll: true });
    });
  });
})();
