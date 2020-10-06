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

const ws = require("nodejs-websocket")
const path = require('path')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(DatePicker)
console.log(__dirname)
/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  data: function()
  {
    return  {
      server: null,
      packageData: []
    }
  },
  methods: {
    onMessage: function (msg, con)
    {
      console.log("RECV: ", msg)
      msg = JSON.parse(msg)
      this.packageData.push(msg)
    },
    onError: function (code, reason)
    {
      console.log("ERROR: ", reason)
    },
    onClose: function (con, code, reason)
    {
      console.log("CLOSED")
    }
  },
  created: function()
  {
    const that = this
    this.server = ws.createServer(function(con)
    {
      console.log("A connection come")
      console.log("Sever connections = ", server.connections.length)
      //when a new message has been received.
      con.on("text", function(msg){ that.onMessage(msg, con) })

      //when a connection has been closed.
      con.on("close", function(code, reason){ that.onClose(con, code, reason) })

      //when a connection meet error.
      con.on("error", function(code, reason){ that.onClose(con, code, reason); that.onError(code, reason) })
    }).listen(8082)
  },
  components: { App },
  router,
  store,
  template: '<App/>'
});
