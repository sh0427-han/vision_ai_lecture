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
  let fitFrame = 0;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function indexFromHash() {
    const match = location.hash.match(/^#slide-(\d+)$/);
    if (!match) return 0;
    return clamp(Number(match[1]) - 1, 0, slides.length - 1);
  }

  function fitActiveSlide() {
    const slide = slides[currentIndex];
    const inner = slide?.querySelector(".slide-inner");
    if (!slide || !inner || !slide.classList.contains("active")) return;

    inner.style.zoom = "1";
    inner.style.transform = "";
    slide.removeAttribute("data-fit-scale");

    const style = getComputedStyle(slide);
    const availableWidth =
      slide.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    const availableHeight =
      slide.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);

    const naturalWidth = Math.max(inner.scrollWidth, inner.getBoundingClientRect().width);
    const naturalHeight = Math.max(inner.scrollHeight, inner.getBoundingClientRect().height);

    if (!naturalWidth || !naturalHeight || availableWidth <= 0 || availableHeight <= 0) return;

    const scale = Math.min(
      1,
      availableWidth / naturalWidth,
      availableHeight / naturalHeight
    );

    if (scale < 0.998) {
      if (CSS.supports("zoom", "0.9")) {
        inner.style.zoom = String(scale);
      } else {
        inner.style.transform = `scale(${scale})`;
      }
      slide.dataset.fitScale = scale.toFixed(3);
    } else {
      slide.dataset.fitScale = "1.000";
    }
  }

  function scheduleFit() {
    cancelAnimationFrame(fitFrame);
    fitFrame = requestAnimationFrame(() => {
      fitActiveSlide();
      requestAnimationFrame(fitActiveSlide);
    });
  }

  function render() {
    slides.forEach((slide, index) => {
      const active = index === currentIndex;
      slide.classList.toggle("active", active);
      slide.setAttribute("aria-hidden", String(!active));
      if (!active) {
        const inner = slide.querySelector(".slide-inner");
        if (inner) {
          inner.style.zoom = "1";
          inner.style.transform = "";
        }
        slide.removeAttribute("data-fit-scale");
      }
    });

    if (currentLabel) currentLabel.textContent = String(currentIndex + 1);
    if (totalLabel) totalLabel.textContent = String(slides.length);
    if (progressBar) {
      progressBar.style.width =
        (((currentIndex + 1) / slides.length) * 100) + "%";
    }

    if (prevButton) prevButton.disabled = currentIndex === 0 && !prevPage;
    if (nextButton) {
      nextButton.disabled = currentIndex === slides.length - 1 && !nextPage;
    }

    history.replaceState(null, "", "#slide-" + (currentIndex + 1));
    scheduleFit();
  }

  function goTo(index) {
    currentIndex = clamp(index, 0, slides.length - 1);
    render();
  }

  function next() {
    if (currentIndex < slides.length - 1) goTo(currentIndex + 1);
    else if (nextPage) location.href = nextPage;
  }

  function previous() {
    if (currentIndex > 0) goTo(currentIndex - 1);
    else if (prevPage) location.href = prevPage;
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
    event.preventDefault();
    wheelLocked = true;
    if (event.deltaY > 0) next();
    else previous();
    setTimeout(() => {
      wheelLocked = false;
    }, 500);
  }, { passive: false });

  addEventListener("touchstart", (event) => {
    const touch = event.changedTouches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
  }, { passive: true });

  addEventListener("touchend", (event) => {
    const touch = event.changedTouches[0];
    const deltaX = touch.clientX - touchStartX;
    const deltaY = touch.clientY - touchStartY;
    if (Math.abs(deltaX) < 50 || Math.abs(deltaX) < Math.abs(deltaY)) return;
    if (deltaX < 0) next();
    else previous();
  }, { passive: true });

  slides.forEach((slide) => {
    slide.querySelectorAll("img").forEach((img) => {
      if (!img.complete) img.addEventListener("load", scheduleFit, { once: true });
    });
  });

  addEventListener("resize", scheduleFit);
  addEventListener("load", scheduleFit, { once: true });
  if (document.fonts?.ready) {
    document.fonts.ready.then(scheduleFit).catch(() => {});
  }

  addEventListener("hashchange", () => {
    currentIndex = indexFromHash();
    render();
  });

  currentIndex = indexFromHash();
  render();
})();