(() => {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-navigation");
  const yearTarget = document.querySelector("#current-year");

  if (yearTarget) yearTarget.textContent = String(new Date().getFullYear());
  if (menuButton && navigation) {
  const menuLabel = menuButton.querySelector(".menu-toggle-label");
  const menuIcon = menuButton.querySelector(".menu-toggle-icon");

  function setMenuOpen(isOpen) {
    navigation.classList.toggle("is-open", isOpen);
    menuButton.setAttribute("aria-expanded", String(isOpen));
    if (menuLabel) menuLabel.textContent = isOpen ? "Close" : "Menu";
    if (menuIcon) menuIcon.textContent = isOpen ? "−" : "+";
  }

  menuButton.addEventListener("click", () => {
    setMenuOpen(menuButton.getAttribute("aria-expanded") !== "true");
  });

  navigation.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof Element && target.closest('a[href^="#"]')) setMenuOpen(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      setMenuOpen(false);
      menuButton.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (menuButton.getAttribute("aria-expanded") !== "true") return;
    if (event.target instanceof Node && !menuButton.contains(event.target) && !navigation.contains(event.target)) {
      setMenuOpen(false);
    }
  });

  const desktopQuery = window.matchMedia("(min-width: 761px)");
  const handleBreakpointChange = (event) => {
    if (event.matches) setMenuOpen(false);
  };
  if (typeof desktopQuery.addEventListener === "function") {
    desktopQuery.addEventListener("change", handleBreakpointChange);
  } else {
    desktopQuery.addListener(handleBreakpointChange);
  }
  }
})();

/* Forced scroll reveals: use viewport checks even when IntersectionObserver is unavailable. */
(() => {
  "use strict";

  const revealSelector = [
    ".hero-copy",
    ".hero-visual",
    ".story-visual",
    ".story-copy",
    ".section-heading",
    ".menu-sheet",
    ".quote-band blockquote",
    ".gallery-item",
    ".visit-copy",
    ".visit-detail",
    ".site-footer .wordmark",
    ".site-footer .footer-links",
    ".copyright"
  ].join(", ");

  const targets = Array.from(document.querySelectorAll(revealSelector));
  if (!targets.length) return;

  document.documentElement.classList.add("has-scroll-reveal");
  const siblingIndexes = new Map();

  targets.forEach((element) => {
    element.classList.add("scroll-reveal");

    const siblings = siblingIndexes.get(element.parentElement) || 0;
    element.style.setProperty("--scroll-reveal-delay", `${Math.min(siblings, 4) * 70}ms`);
    siblingIndexes.set(element.parentElement, siblings + 1);

    if (element.matches(".hero-copy, .story-visual, .visit-copy")) {
      element.dataset.revealDirection = "left";
    } else if (element.matches(".hero-visual, .story-copy")) {
      element.dataset.revealDirection = "right";
    }
  });

  const revealIfVisible = (element) => {
    const rect = element.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.94 && rect.bottom > 0) {
      element.classList.add("is-revealed");
      return true;
    }
    return false;
  };

  // Reveal visible content immediately so the page never starts with hidden sections.
  targets.forEach(revealIfVisible);

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-revealed");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0, rootMargin: "0px 0px 40px 0px" });

    targets.forEach((element) => {
      if (!element.classList.contains("is-revealed")) observer.observe(element);
    });
  } else {
    let ticking = false;
    const checkVisible = () => {
      targets.forEach((element) => {
        if (!element.classList.contains("is-revealed")) revealIfVisible(element);
      });
      ticking = false;
    };
    const requestCheck = () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(checkVisible);
    };
    window.addEventListener("scroll", requestCheck, { passive: true });
    window.addEventListener("resize", requestCheck);
    requestCheck();
  }
})();
