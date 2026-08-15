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

/* Newsletter signup.
 *
 * The form works without any of this: it POSTs to Buttondown and the visitor
 * lands on Buttondown's confirmation page. This upgrade keeps them on the page
 * instead — and, importantly, reads the actual response before saying anything.
 *
 * The endpoint sends `access-control-allow-origin: *`, so the status code is
 * readable. Had it not been, the only option would have been a no-cors request
 * whose outcome is invisible, and the honest thing then would have been to
 * leave the plain form alone rather than print "thanks, you're subscribed" on
 * the strength of having sent something into the dark.
 */
(function () {
  "use strict";

  var form = document.querySelector(".signup__form[data-async]");
  if (!form || !window.fetch || !window.URLSearchParams) return;

  var status = document.getElementById("signup-status");
  var fallback = form.getAttribute("data-fallback");

  function say(message, isError) {
    if (!status) return;
    status.textContent = message;
    status.classList.toggle("is-error", Boolean(isError));
  }

  form.addEventListener("submit", function (event) {
    var field = form.querySelector('input[type="email"]');
    var button = form.querySelector("button");
    if (!field || !field.value || !field.checkValidity()) return;  // let the browser complain

    event.preventDefault();
    button.disabled = true;
    say("Subscribing…");

    fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ email: field.value }).toString()
    })
      .then(function (response) {
        if (!response.ok) throw new Error("the mailing list returned " + response.status);
        form.hidden = true;
        say("Thanks. There's a confirmation link in your inbox — it only counts once you click it.");
      })
      .catch(function (error) {
        button.disabled = false;
        say(
          "That didn't go through (" + error.message + "). " +
          "You can subscribe directly at " + fallback + ".",
          true
        );
      });
  });
})();
