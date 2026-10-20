(() => {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-navigation");
  const yearTarget = document.querySelector("#current-year");

  if (yearTarget) {
    yearTarget.textContent = String(new Date().getFullYear());
  }

  const menuFilterButtons = Array.from(document.querySelectorAll(".menu-filter[data-filter]"));
  const menuCards = Array.from(document.querySelectorAll(".menu-card[data-category]"));
  const filterStatus = document.querySelector("#menu-filter-status");
  const filterContainer = document.querySelector(".menu-filters");

  if (menuFilterButtons.length > 0 && menuCards.length > 0 && filterContainer) {
    function applyMenuFilter(filter) {
      let visibleCount = 0;

      menuCards.forEach((card) => {
        const shouldShow = filter === "all" || card.dataset.category === filter;
        card.hidden = !shouldShow;
        if (shouldShow) visibleCount += 1;
      });

      menuFilterButtons.forEach((button) => {
        const isActive = button.dataset.filter === filter;
        button.classList.toggle("is-active", isActive);
        button.setAttribute("aria-pressed", String(isActive));
      });

      if (filterStatus) {
        const categoryName = filter === "all"
          ? "all menu highlights"
          : menuFilterButtons.find((button) => button.dataset.filter === filter)?.textContent.trim() || filter;
        filterStatus.textContent = `Showing ${visibleCount} ${categoryName.toLowerCase()}.`;
      }
    }

    menuFilterButtons.forEach((button) => {
      button.addEventListener("click", () => applyMenuFilter(button.dataset.filter || "all"));
    });
    filterContainer.hidden = false;
    applyMenuFilter("all");
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
