/*
 * @Date: 2020-09-30 08:50:47
 * @LastEditors: Jecosine
 * @LastEditTime: 2020-10-28 15:13:31
 */
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'



// import from antdesign
import {DatePicker} from 'ant-design-vue'
// import 'ant-design-vue/dist/antd.css'

const path = require('path')
import axios from 'axios'
Vue.prototype.$axios = axios
axios.defaults.baseURL="/api"
axios.defaults.headers.post['Content-Type']='application/json';
if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(DatePicker)
console.log(__dirname)
/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  
  components: { App },
  router,
  template: '<App/>'
});
