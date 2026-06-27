const tabs = document.querySelectorAll('.car-types-tabs .tab-btn');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelector('.car-types-tabs .tab-btn.active')?.classList.remove('active');
        tab.classList.add('active');
    });
});

