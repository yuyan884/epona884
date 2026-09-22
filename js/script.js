document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav toggle
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  hamburger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    hamburger.classList.toggle('is-open', isOpen);
    hamburger.setAttribute('aria-expanded', String(isOpen));
  });

  nav.querySelectorAll('.nav__link').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      hamburger.classList.remove('is-open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });

  // Header background on scroll
  const header = document.getElementById('header');
  const onScroll = () => {
    header.style.borderBottomColor = window.scrollY > 10
      ? 'rgba(221, 210, 193, 1)'
      : 'transparent';
  };
  onScroll();
  window.addEventListener('scroll', onScroll);

  // Gallery lightbox
  const lightbox = document.getElementById('lightbox');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');

  document.querySelectorAll('.gallery__item').forEach((item) => {
    item.addEventListener('click', () => {
      lightboxCaption.textContent = item.dataset.caption || '';
      lightbox.classList.add('is-open');
    });
  });

  const closeLightbox = () => lightbox.classList.remove('is-open');

  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
});
