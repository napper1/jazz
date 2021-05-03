// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'font-awesome/css/font-awesome.min.css'
import Vue from 'vue'
import Vuex from 'vuex'

import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
// import IconsPlugin from 'bootstrap-vue'
// import BootstrapVueIcons from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css';

import App from './App'
import router from './router'
import DatatableFactory from 'vuejs-datatable';
import VueYouTubeEmbed from 'vue-youtube-embed'
import axios from 'axios';

axios.defaults.baseURL = `http://localhost:8000`;
Vue.config.productionTip = false
Vue.use(BootstrapVue);
// Vue.use(IconsPlugin);
Vue.use(BootstrapVueIcons);
Vue.use(DatatableFactory);
Vue.use(VueYouTubeEmbed);
Vue.use(Vuex);

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

const store = new Vuex.Store({
  state: {
    count: 0,
    api_host: 'http://localhost:8000',
    songs: [],
    filter_loading: false,
  },
  mutations: {
    increment (state) {
      state.count++
    },
    setSongs(state, songs){
      state.songs = songs;
    }
  },
  actions: {
    getSongs(state) {
      console.log(state.state.api_host);
      this.filter_loading = true;
      const path = state.state.api_host + '/songs/';
      axios.get(path)
        .then((res) => {
          // this calls setSongs mutation which saves response to the state
          store.commit('setSongs', res.data);
          state.filter_loading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          state.filter_loading = false;
        });
    },
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store: store,
  router,
  components: {
    App
  },
  template: '<App/>'
})

