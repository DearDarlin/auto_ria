const tabs = document.querySelectorAll('.car-types-tabs .tab-btn');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
        // 1. Удаляем класс active у кнопки, которая была активной до этого
            document.querySelector('.car-types-tabs .tab-btn.active')?.classList.remove('active');
        // 2. Добавляем класс active той кнопке, на которую только что кликнули
            tab.classList.add('active');
            });
        });