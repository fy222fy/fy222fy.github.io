// Small behaviors of the site. Everything works without JavaScript; this only adds convenience.
(function () {
  "use strict";

  var root = document.documentElement;

  // Light and dark theme ------------------------------------------------------
  // Follows the system setting until the visitor chooses; the choice is remembered on this device.
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  function currentTheme() {
    return root.getAttribute("data-theme") || (systemDark.matches ? "dark" : "light");
  }

  function setTheme(theme) {
    var system = systemDark.matches ? "dark" : "light";
    try {
      if (theme === system) {
        root.removeAttribute("data-theme");
        localStorage.removeItem("theme");
      } else {
        root.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
      }
    } catch (e) {
      root.setAttribute("data-theme", theme);
    }
  }

  document.querySelectorAll(".theme-toggle").forEach(function (button) {
    button.addEventListener("click", function () {
      setTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  });

  // Navigation on small screens -----------------------------------------------
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function setNav(open) {
    root.classList.toggle("nav-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    var label = navToggle.querySelector(".label");
    if (label) label.textContent = open ? label.dataset.close : label.dataset.open;
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      setNav(!root.classList.contains("nav-open"));
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && root.classList.contains("nav-open")) {
        setNav(false);
        navToggle.focus();
      }
    });
    window.matchMedia("(min-width: 921px)").addEventListener("change", function (event) {
      if (event.matches) setNav(false);
    });
  }

  // Panels that open and close: abstracts and BibTeX ----------------------------
  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-toggle]");
    if (!button) return;
    var panel = document.getElementById(button.getAttribute("aria-controls"));
    if (!panel) return;
    var open = button.getAttribute("aria-expanded") !== "true";
    // only one panel of an entry is open at a time
    var entry = button.closest(".pub");
    if (entry && open) {
      entry.querySelectorAll("[data-toggle][aria-expanded='true']").forEach(function (other) {
        other.setAttribute("aria-expanded", "false");
        var otherPanel = document.getElementById(other.getAttribute("aria-controls"));
        if (otherPanel) otherPanel.hidden = true;
      });
    }
    button.setAttribute("aria-expanded", String(open));
    panel.hidden = !open;
  });

  // Copy buttons ------------------------------------------------------------------
  function copyText(text, button) {
    var label = button.dataset.label || button.textContent;
    var done = function () {
      button.textContent = button.dataset.done || label;
      setTimeout(function () {
        button.textContent = label;
      }, 1600);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done);
    } else {
      var area = document.createElement("textarea");
      area.value = text;
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy");
        done();
      } catch (e) {}
      area.remove();
    }
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-copy]");
    if (!button) return;
    var source = button.parentElement.querySelector("pre");
    if (source) copyText(source.textContent.replace(/\n$/, ""), button);
  });

  // Code blocks in articles get a copy button
  var prose = document.querySelector(".prose");
  if (prose) {
    var copyLabel = prose.dataset.copy || "Copy";
    var copiedLabel = prose.dataset.copied || "Copied";
    prose.querySelectorAll("div.highlight, figure.highlight").forEach(function (block) {
      if (!block.querySelector("pre")) return;
      var button = document.createElement("button");
      button.type = "button";
      button.className = "copy-code";
      button.textContent = copyLabel;
      button.dataset.copy = "";
      button.dataset.label = copyLabel;
      button.dataset.done = copiedLabel;
      block.appendChild(button);
    });
  }

  // Table of contents: mark the section being read --------------------------------
  var toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    var links = {};
    toc.querySelectorAll("a[href^='#']").forEach(function (link) {
      links[decodeURIComponent(link.getAttribute("href").slice(1))] = link;
    });
    var headings = Array.prototype.filter.call(
      document.querySelectorAll(".prose h1[id], .prose h2[id], .prose h3[id]"),
      function (heading) {
        return links[heading.id];
      }
    );
    var active = null;
    var mark = function () {
      var current = headings[0];
      headings.forEach(function (heading) {
        if (heading.getBoundingClientRect().top < 120) current = heading;
      });
      if (current && links[current.id] !== active) {
        if (active) active.classList.remove("is-active");
        active = links[current.id];
        active.classList.add("is-active");
      }
    };
    var ticking = false;
    window.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          mark();
          ticking = false;
        });
      },
      { passive: true }
    );
    mark();
  }

  // Print button on the CV page ------------------------------------------------------
  document.querySelectorAll("[data-print]").forEach(function (button) {
    button.addEventListener("click", function () {
      window.print();
    });
  });
})();
