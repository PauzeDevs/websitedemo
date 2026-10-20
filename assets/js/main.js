(() => {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-navigation");
  const yearTarget = document.querySelector("#current-year");

  if (yearTarget) {
    yearTarget.textContent = String(new Date().getFullYear());
  }

  if (!menuButton || !navigation) {
    return;
  }

  const menuLabel = menuButton.querySelector(".menu-toggle-label");
  const menuIcon = menuButton.querySelector(".menu-toggle-icon");

  function setMenuOpen(isOpen) {
    navigation.classList.toggle("is-open", isOpen);
    menuButton.setAttribute("aria-expanded", String(isOpen));

    if (menuLabel) {
      menuLabel.textContent = isOpen ? "Close" : "Menu";
    }

    if (menuIcon) {
      menuIcon.textContent = isOpen ? "−" : "+";
    }
  }

  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") !== "true";
    setMenuOpen(isOpen);
  });

  navigation.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof Element && target.closest('a[href^="#"]')) {
      setMenuOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      setMenuOpen(false);
      menuButton.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (
      menuButton.getAttribute("aria-expanded") === "true" &&
      event.target instanceof Node &&
      !menuButton.contains(event.target) &&
      !navigation.contains(event.target)
    ) {
      setMenuOpen(false);
    }
  });

  const desktopQuery = window.matchMedia("(min-width: 761px)");
  const handleBreakpointChange = (event) => {
    if (event.matches) {
      setMenuOpen(false);
    }
  };

  if (typeof desktopQuery.addEventListener === "function") {
    desktopQuery.addEventListener("change", handleBreakpointChange);
  } else {
    // Support older Safari versions.
    desktopQuery.addListener(handleBreakpointChange);
  }
})();
