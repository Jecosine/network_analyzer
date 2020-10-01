/*
 * @Date: 2020-09-30 08:50:47
 * @LastEditors: Jecosine
 * @LastEditTime: 2020-09-30 17:26:20
 */
import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'



// import from antdesign
import {DatePicker} from 'ant-design-vue'
// import 'ant-design-vue/dist/antd.css'


const python = require('path')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(DatePicker)
console.log(__dirname)
/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
