<!--
 * @Date: 2020-09-30 08:50:47
 * @LastEditors: Jecosine
 * @LastEditTime: 2020-10-10 15:56:37
-->
<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
const ws = require("nodejs-websocket")
export default {
  name: "network_snipper",
  data: function() {
    return {
      server: null,
      packageData: [],
    };
  },
  methods: {
    onMessage: function(msg, con) {
      console.log("RECV: ", msg);
      msg = JSON.parse(msg);
      this.packageData.push(msg);
    },
    onError: function(code, reason) {
      console.log("ERROR: ", reason);
    },
    onClose: function(con, code, reason) {
      console.log("CLOSED");
    },
  },
  created: function() {
    const that = this;
    this.server = ws
      .createServer(function(con) {
        console.log("A connection come");
        console.log("Sever connections = ", server.connections.length);
        //when a new message has been received.
        con.on("text", function(msg) {
          that.onMessage(msg, con);
        });

        //when a connection has been closed.
        con.on("close", function(code, reason) {
          that.onClose(con, code, reason);
        });

        //when a connection meet error.
        con.on("error", function(code, reason) {
          that.onClose(con, code, reason);
          that.onError(code, reason);
        });
      })
      .listen(8082);
  },
};
</script>

<style>
/* CSS */
</style>
