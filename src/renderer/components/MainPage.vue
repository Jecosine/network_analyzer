<template>
  <a-layout id="components-layout-demo-basic" class="layout">
    <a-affix :offset-top="top">
      <a-layout-header id="app-header">
        <div
          class="logo"
          style="width: 100%;height: 30px;background: rgba(8, 151, 156, 1); line-height: 30px;color: white"
        >
          <span
            style="margin-left: 20px;font-family: 'Poiret One';font-weight: bold"
            ><a-icon type="heat-map" size="small" /> WireWhale</span
          >
          <a-button-group id="window-tools" style="float: right; right: 5px">
            <a-button icon="minus" size="small"></a-button>
            <a-button icon="plus-square" size="small"></a-button>
            <a-button icon="close" size="small"></a-button>
          </a-button-group>
        </div>
        <a-menu
          :selectable="false"
          mode="horizontal"
          :style="{ lineHeight: '40px' }"
        >
          <a-menu-item key="mail"> <a-icon type="file" />File </a-menu-item>
          <a-menu-item key="app"> <a-icon type="appstore" />Edit </a-menu-item>
          <a-sub-menu>
            <span slot="title" class="submenu-title-wrapper"
              ><a-icon type="setting" />Option</span
            >
            <a-menu-item-group title="Item 1">
              <a-menu-item key="setting:1">bana </a-menu-item>
              <a-menu-item key="setting:2">
                Option 2
              </a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="Item 2">
              <a-menu-item key="setting:3">
                Option 3
              </a-menu-item>
              <a-menu-item key="setting:4">
                Option 4
              </a-menu-item>
            </a-menu-item-group>
          </a-sub-menu>
          <a-sub-menu key="help">
            <span slot="title" class="submenu-title-wrapper"
              ><a-icon type="question-circle" />Help</span
            >
          </a-sub-menu>
        </a-menu>
      </a-layout-header>
    </a-affix>
    <a-layout-content>
      <div
        :style="{
          background: '#fefefe',
          width: '100%',
          height: 'calc(100vh - 110px)',
        }"
      >
        <a-table
          id="main-table"
          ref="dataTable"
          :scroll="{ y: 'calc(100% - 55px)' }"
          :columns="tableColumns"
          :data-source="tableData"
          :pagination="false"
        >
          <a slot="name" slot-scope="text">{{ text }}</a>
          <span slot="customTitle">Frame Type</span>
          <span slot="tags" slot-scope="tags">
            <a-tag
              v-for="tag in tags"
              :key="tag"
              :color="
                tag === 'loser'
                  ? 'volcano'
                  : tag.length > 5
                  ? 'geekblue'
                  : 'green'
              "
            >
              {{ tag.toUpperCase() }}
            </a-tag>
          </span>
          <!-- <span slot="action" slot-scope="text, record">
            <a>Invite 一 {{ record.name }}</a>
            <a-divider type="vertical" />
            <a>Delete</a>
            <a-divider type="vertical" />
            <a class="ant-dropdown-link">
              More actions <a-icon type="down" />
            </a>
          </span> -->
        </a-table>
      </div>
    </a-layout-content>
    <a-layout-footer
      style="position:fixed;bottom: 0;width: 100%;height: 40px;padding: 0 10px;line-height: 40px"
    >
      <a-icon type="check-circle" class="green" /> Listening on
      <strong>'Intel Wireless Adapter'</strong>
    </a-layout-footer>
  </a-layout>
</template>

<script>
const _columns = [
  {
    title: "Index",
    key: "key",
    dataIndex: "key",
    width: "80px",
  },
  {
    dataIndex: "frame_type",
    key: "frame_type",
    default: 'Ethernet II',
    slots: { title: "customTitle" },
    scopedSlots: { customRender: "name" },
  },
  {
    title: "Src",
    dataIndex: "source_address",
    key: "src",
  },
  {
    title: "Dst",
    dataIndex: "destination_address",
    key: "dst",
  },
  {
    title: "Length",
    dataIndex: "tlen",
    key: "length",
  },
  {
    title: "Protocol",
    key: "protocol",
    dataIndex: "protocol.keyword",
    scopedSlots: { customRender: "tags" },
  },
  {
    title: "Info",
    key: "info",
    dataIndex: "protocol.description",
  },
];

const _data = [
  {
    key: "1",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "15.163.12.222",
    tags: ["nice", "developer"],
    info: "Transmission Control Protocol",
  },
  {
    key: "2",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["loser"],
    info: "Transmission Control Protocol",
  },
  {
    key: "3",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["cool", "teacher"],
    info: "Transmission Control Protocol",
  },
  {
    key: "4",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "15.163.12.222",
    tags: ["nice", "developer"],
    info: "Transmission Control Protocol",
  },
  {
    key: "5",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["loser"],
    info: "Transmission Control Protocol",
  },
  {
    key: "6",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["cool", "teacher"],
    info: "Transmission Control Protocol",
  },
  {
    key: "7",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "15.163.12.222",
    tags: ["nice", "developer"],
    info: "Transmission Control Protocol",
  },
  {
    key: "8",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["loser"],
    info: "Transmission Control Protocol",
  },
  {
    key: "9",
    frame_type: "Ethernet",
    src: "10.128.192.92",
    length: 19247,
    protocol: ["TCP"],
    dst: "10.128.192.92",
    tags: ["cool", "teacher"],
    info: "Transmission Control Protocol",
  },
];
export default {
  name: "main-page",
  props: {
    // tableData: _data,
    // columns: _columns
    server: {
      type: Object,
      default: null,
      packageData: []
    },
  },
  data() {
    return {
      top: null,
      tableData: _data,
      tableColumns: _columns,
      collapsed: false,
      counter: 10,
      reachBottom: false,
    };
  },
  // components: { SystemInformation },
  methods: {
    onMessage: function(msg, con) {
      console.log("(MP)RECV: ", msg);
      msg = JSON.parse(msg);
      this.packageData.push(msg);
    },
    onError: function(code, reason) {
      console.log("(MP)ERROR: ", reason);
    },
    onClose: function(con, code, reason) {
      console.log("(MP)CLOSED");
    },
    toBottom: function() {
      const that = this;
      let calcHeight = 0.0;
      if (that.reachBottom)
        this.itv = setInterval(() => {
          calcHeight =
            that.mainTable.scrollHeight -
            that.mainTable.clientHeight -
            that.mainTable.scrollTop;
          if (calcHeight < 5) {
            that.mainTable.scrollTop =
              that.mainTable.scrollHeight - that.mainTable.clientHeight;
            clearInterval(that.itv);
          } else that.mainTable.scrollTop += calcHeight / 2;
        }, 50);
    },
  },
  mounted() {
    const that = this;
    this.mainTable = document.getElementsByClassName("ant-table-body")[0];
    console.log(this.mainTable);
    this.mainTable.addEventListener("scroll", (e) => {
      // console.log(e);

      if (e.target.scrollTop == e.target.scrollHeight - e.target.clientHeight) {
        console.log("On bottom");
        that.reachBottom = true;
      } else {
        that.reachBottom = false;
        // clearInterval(that.itv);
      }
    });
    // addEventListener('scroll', (event) => {
    //     console.log(event);
    // })
    // bind server
    that.server.on("connection", (con) => {
      console.log("A connection come(Real)");
      console.log(that.server)
      // console.log("Sever connections = ", that.server.connections.length);
      //when a new message has been received.
      con.on("message", function(msg) {
        // that.onMessage(msg, con);
        console.log(msg);
        that.tableData.push(JSON.parse(msg))
        if (that.reachBottom) {
          that.toBottom();
        }
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
    });
  },
  created: function() {
    const that = this;
    // setInterval(() => {
    //   that.tableData.push({
    //     key: (that.counter++).toString(),
    //     frame_type: "Ethernet",
    //     src: "10.128.192.92",
    //     length: 19247,
    //     protocol: ["TCP"],
    //     dst: "10.128.192.92",
    //     tags: ["cool", "teacher"],
    //     info: "Transmission Control Protocol",
    //   });
    //   if (that.reachBottom) {
    //     that.toBottom();
    //   }
    // }, 2000);
  },
};
</script>

<style>
#main-table {
  height: calc(100vh - 110px);
}
#window-tools .ant-btn {
  border: none;
  height: 30px;
  line-height: 30px;
  background: transparent;
  color: white;
  font-weight: 1000;
  box-shadow: none;
}
.green {
  color: green;
  font-weight: bold;
}
#app-header {
  height: 60px;
  line-height: 40px;
  padding: 0;
}
#components-layout-demo-basic .ant-menu-item {
  /* text-align: center; */
  height: 40px;
}

#components-layout-demo-basic .ant-layout-footer {
  height: 0;
}
.ant-menu-submenu,
.ant-btn-group {
  -webkit-app-region: no-drag;
}
#components-layout-demo-basic .ant-layout-header {
  height: 60px;
  background: white;
  -webkit-app-region: drag;
  position: fixed;
  width: 100%;
  top: 0;
}
.ant-table-scroll {
  height: calc(100vh - 110px);
}
#components-layout-demo-basic .ant-layout-content {
  position: relative;
  top: 70px;
}
</style>
