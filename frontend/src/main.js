// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import 'font-awesome/css/font-awesome.min.css'
import Vue from 'vue'
import App from './App'
import router from './router'
import DatatableFactory from 'vuejs-datatable';
import VueYouTubeEmbed from 'vue-youtube-embed'


Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(DatatableFactory);
Vue.use(VueYouTubeEmbed);

Vue.directive('scroll', {
  inserted: function (el, binding) {
    let f = function (evt) {
      if (binding.value(evt, el)) {
        window.removeEventListener('scroll', f)
      }
    }
    window.addEventListener('scroll', f)
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App
  },
  template: '<App/>'
})

