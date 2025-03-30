export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.directive('auto-focus', {
    mounted(el) {
      el.focus();
    }
  });

  nuxtApp.vueApp.directive('click-outside', {
    mounted(el, binding) {
      el._clickOutside = (event) => {
        if (!(el === event.target || el.contains(event.target))) {
          binding.value(event);
        }
      };
      document.addEventListener('click', el._clickOutside);
    },
    unmounted(el) {
      document.removeEventListener('click', el._clickOutside);
    }
  });

  nuxtApp.vueApp.directive('format-number', {
    mounted(el, binding) {
      const formatter = new Intl.NumberFormat('th-TH', binding.value || {});
      
      const updateValue = () => {
        const value = el.value || el.textContent;
        const formattedValue = formatter.format(value);
        
        if (el.tagName === 'INPUT') {
          el.value = formattedValue;
        } else {
          el.textContent = formattedValue;
        }
      };
      
      updateValue();
      
      if (el.tagName === 'INPUT') {
        el.addEventListener('input', updateValue);
      }
    }
  });
});
