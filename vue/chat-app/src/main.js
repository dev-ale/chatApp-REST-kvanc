import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import titleComponent from './components/VueTitle'
import store from './store'

Vue.config.productionTip = false
Vue.component('vue-title', titleComponent)

new Vue({
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
