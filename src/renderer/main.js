/*
 * @Date: 2020-09-30 08:50:47
 * @LastEditors: Jecosine
 * @LastEditTime: 2020-10-10 15:56:03
 */
import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'

// import from antdesign
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(Antd)

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  template: '<App/>'
}).$mount('#app')
