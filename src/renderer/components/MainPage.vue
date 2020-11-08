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
                    <a-button-group
                        id="window-tools"
                        style="float: right; right: 5px"
                    >
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
                    <a-menu-item key="mail">
                        <a-icon type="file" />File
                    </a-menu-item>
                    <a-menu-item key="app">
                        <a-icon type="appstore" />Edit
                    </a-menu-item>
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
                        <span slot="title" class="submenu-title-wrapper">
                            <a-icon type="question-circle" />Help</span
                        >
                    </a-sub-menu>
                </a-menu>
            </a-layout-header>
        </a-affix>
        <a-layout-content>
            <div id="toolbar">
                <a-input-search
                    id="filter-container"
                    placeholder="Filter the packets"
                    style="width: 200px"
                    @search="onSearch"
                >
                    <a-icon slot="prefix" type="filter" />
                </a-input-search>
                <a-dropdown id="selector-container">
                    <a-menu slot="overlay" @click="handleMenuClick">
                        <a-menu-item :key="i" v-for="(item, i) in ifaces" @visibleChange="onVisibleChange">
                            <a-icon type="api" /> {{item.name}}
                        </a-menu-item>
                    </a-menu>
                    <a-button style="margin-left: 8px">
                        {{currentInterface}} <a-icon type="down" />
                    </a-button>
                </a-dropdown>
                <a-button-group id="tool-group">
                    <a-button :loading="loading_start" @click="onStart" :icon="isPause ? 'caret-right' : 'pause'" />
                    <a-button style="color:red" icon="close" />
                </a-button-group>
            </div>
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
                    :scroll="{ y: 'calc(100vh - 165px)' }"
                    :columns="tableColumns"
                    :data-source="tableData"
                    :pagination="false"
                >
                    <a slot="name" slot-scope="text">{{
                        "Ethernet II/" + text
                    }}</a>
                    <span slot="customTitle">Frame Type</span>
                    <span slot="tags" slot-scope="tags">
                        <a-tag>
                            {{ tags ? tags.toUpperCase() : "OTHERS" }}
                        </a-tag>
                    </span>
                    <div
                        slot="expandedRowRender"
                        slot-scope="record"
                        style="margin: 0"
                    >
                        <a-collapse
                            :bordered="false"
                            v-if="record != null && record != {}"
                        >
                            <template #expandIcon="props">
                                <a-icon
                                    type="caret-right"
                                    :rotate="props.isActive ? 90 : 0"
                                />
                            </template>
                            <a-collapse-panel
                                :key="i + 90"
                                v-for="(item, i) in record.detail"
                                :header="item.name"
                            >
                                <a-descriptions
                                    title=""
                                    layout="horizontal"
                                    :column="2"
                                >
                                    <a-descriptions-item
                                        :key="j"
                                        v-for="(field, j) in item.child"
                                        :label="field.name"
                                        >{{ field.value }}</a-descriptions-item
                                    >
                                </a-descriptions>
                            </a-collapse-panel>
                        </a-collapse>
                    </div>
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
// axios = require('axios')
const _columns = [
    {
        title: "Index",
        key: "key",
        dataIndex: "key",
        width: "80px",
    },
    {
        dataIndex: "ethernet.frame_type",
        key: "frame_type",
        default: "Ethernet II",
        slots: { title: "customTitle" },
        scopedSlots: { customRender: "name" },
    },
    {
        title: "Src",
        dataIndex: "ethernet.src",
        key: "src",
        width: "220px",
    },
    {
        title: "Dst",
        dataIndex: "ethernet.dst",
        key: "dst",
        width: "220px",
    },
    {
        title: "Length",
        dataIndex: "ethernet.len",
        key: "length",
    },
    {
        title: "Protocol",
        key: "protocol",
        dataIndex: "ip.protocol.keyword",
        scopedSlots: { customRender: "tags" },
    },
    {
        title: "Info",
        key: "info",
        dataIndex: "ip.protocol.description",
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
            packageData: [],
        },
    },
    data() {
        return {
            ifaces: [],
            currentInterface: 'Not Selected',
            top: null,
            tableData: [],
            tableColumns: _columns,
            collapsed: false,
            counter: 1,
            reachBottom: false,
            isPause: true,
            replaceFields: {
                children: "child",
                title: "name",
            },
            loading_start: false
        };
    },
    // components: { SystemInformation },
    methods: {
        onVisibleChange: function(visible)
        {
            console.log(visible);
        },
        onStart: function() {
            const that = this;
            if(that.isPause)
            {
                this.loading_start = true;
                this.$axios.get("/start?no=15", {}).then((res) => {
                    console.log(res);
                    that.loading_start = false;
                });
            } else {
                this.loading_start = true;
                
                this.$axios.get("/pause", {}).then((res) => {
                    console.log(res);
                    that.loading_start = false;
                });
            }
            that.isPause = !that.isPause;
        },
        onSearch() {},
        handleMenuClick(e) {
            console.log("click", e);
        },
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
                            that.mainTable.scrollHeight -
                            that.mainTable.clientHeight;
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

            if (
                e.target.scrollTop ==
                e.target.scrollHeight - e.target.clientHeight
            ) {
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
            console.log(that.server);
            // console.log("Sever connections = ", that.server.connections.length);
            //when a new message has been received.
            con.on("message", function(msg) {
                // that.onMessage(msg, con);
                console.log(msg);
                msg = JSON.parse(msg);
                msg["key"] = that.counter++;
                that.tableData.push(msg);
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
        this.$axios.get("/start?no=22", {}).then((res) => {
            console.log(res);
        });
        this.$axios.get("/getInterface", {}).then((res) => {
            console.log(res);
            that.ifaces = res.data;
        });
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
#toolbar {
    display: flex;
    flex-direction: row;
    width: calc(100% - 20px);
    padding-left: 10px;
    padding-right: 10px;
    height: 40px;
    line-height: 40px;
}
#filter-container {
    /* line-height: 40px; */
    height: 30px;
    margin: 5px;
    vertical-align: middle;
}

#selector-container {
    height: 30px;
    margin: 5px;
    /* line-height: 40px; */
}
#tool-group {
    height: 30px;
}
.ant-table-body {
    font-family: "Fira Code";
}
.ant-table-row > td {
    font-size: 12px;
    height: 40px;
    line-height: 40px;
    padding: 5px !important;
    padding-left: 15px !important;
}
.ant-collapse,
.ant-collapse-item span {
    font-size: 12px;
}
.ant-descriptions-item-label {
    font-weight: bolder;
}
</style>
