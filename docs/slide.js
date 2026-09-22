(() => {
  const slides = Array.from(document.querySelectorAll(".slide"));
  if (!slides.length) return;

  const prevButton = document.querySelector("[data-slide-prev]");
  const nextButton = document.querySelector("[data-slide-next]");
  const currentLabel = document.querySelector("[data-slide-current]");
  const totalLabel = document.querySelector("[data-slide-total]");
  const progressBar = document.querySelector("[data-slide-progress]");
  const nextPage = document.body.dataset.nextPage || "";
  const prevPage = document.body.dataset.prevPage || "";

  let currentIndex = 0;
  let wheelLocked = false;
  let touchStartX = 0;
  let touchStartY = 0;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function indexFromHash() {
    const match = location.hash.match(/^#slide-(\d+)$/);
    if (!match) return 0;
    return clamp(Number(match[1]) - 1, 0, slides.length - 1);
  }

  function render() {
    slides.forEach((slide, index) => {
      const active = index === currentIndex;
      slide.classList.toggle("active", active);
      slide.setAttribute("aria-hidden", String(!active));
    });

    if (currentLabel) currentLabel.textContent = String(currentIndex + 1);
    if (totalLabel) totalLabel.textContent = String(slides.length);
    if (progressBar) {
      progressBar.style.width =
        (((currentIndex + 1) / slides.length) * 100) + "%";
    }

    if (prevButton) {
      prevButton.disabled = currentIndex === 0 && !prevPage;
    }
    if (nextButton) {
      nextButton.disabled =
        currentIndex === slides.length - 1 && !nextPage;
    }

    history.replaceState(null, "", "#slide-" + (currentIndex + 1));
  }

  function goTo(index) {
    currentIndex = clamp(index, 0, slides.length - 1);
    render();
  }

  function next() {
    if (currentIndex < slides.length - 1) {
      goTo(currentIndex + 1);
    } else if (nextPage) {
      location.href = nextPage;
    }
  }

  function previous() {
    if (currentIndex > 0) {
      goTo(currentIndex - 1);
    } else if (prevPage) {
      location.href = prevPage;
    }
  }

  prevButton?.addEventListener("click", previous);
  nextButton?.addEventListener("click", next);

  addEventListener("keydown", (event) => {
    const target = event.target;
    if (
      target instanceof HTMLInputElement ||
      target instanceof HTMLTextAreaElement ||
      target instanceof HTMLSelectElement
    ) return;

    if (
      event.key === "ArrowRight" ||
      event.key === "PageDown" ||
      event.key === " "
    ) {
      event.preventDefault();
      next();
    } else if (
      event.key === "ArrowLeft" ||
      event.key === "PageUp"
    ) {
      event.preventDefault();
      previous();
    } else if (event.key === "Home") {
      event.preventDefault();
      goTo(0);
    } else if (event.key === "End") {
      event.preventDefault();
      goTo(slides.length - 1);
    }
  });

  addEventListener("wheel", (event) => {
    if (wheelLocked || Math.abs(event.deltaY) < 25) return;
    wheelLocked = true;
    if (event.deltaY > 0) next();
    else previous();
    setTimeout(() => {
      wheelLocked = false;
    }, 500);
  }, { passive: true });

  addEventListener("touchstart", (event) => {
    const touch = event.changedTouches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
  }, { passive: true });

  addEventListener("touchend", (event) => {
    const touch = event.changedTouches[0];
    const deltaX = touch.clientX - touchStartX;
    const deltaY = touch.clientY - touchStartY;
    if (Math.abs(deltaX) < 50 || Math.abs(deltaX) < Math.abs(deltaY)) {
      return;
    }
    if (deltaX < 0) next();
    else previous();
  }, { passive: true });

  addEventListener("hashchange", () => {
    currentIndex = indexFromHash();
    render();
  });

  currentIndex = indexFromHash();
  render();
})();