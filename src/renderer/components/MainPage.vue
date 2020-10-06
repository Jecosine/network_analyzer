<template>
  <a-layout id="components-layout-demo-basic" class="layout">
    <a-layout-header id="app-header">
      <div class="logo" />
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
        <a-button-group style="float: right; right: 5px">
          <a-button icon="minus"></a-button>
          <a-button icon="plus-square"></a-button>
          <a-button icon="close"></a-button>
        </a-button-group>
      </a-menu>
    </a-layout-header>
    <a-layout-content>
      <div
        :style="{
          background: '#eee',
          width: '100%',
          height: 'calc(100vh - 80px)',
        }"
      >
        <a-table :columns="tableColumns" :data-source="tableData" :pagination="false">
          <a slot="name" slot-scope="text">{{ text }}</a>
          <span slot="customTitle"><a-icon type="smile-o" /> Name</span>
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
          <span slot="action" slot-scope="text, record">
            <a>Invite 一 {{ record.name }}</a>
            <a-divider type="vertical" />
            <a>Delete</a>
            <a-divider type="vertical" />
            <a class="ant-dropdown-link">
              More actions <a-icon type="down" />
            </a>
          </span>
        </a-table>
      </div>
    </a-layout-content>
    <a-layout-footer style="height: 40px;padding: 0 10px;line-height: 40px">
      <a-icon type="check-circle" class="green"/> Listening on <strong>'Intel Wireless Adapter'</strong>
    </a-layout-footer>
  </a-layout>
</template>

<script>
const _columns = [
  {
    dataIndex: "name",
    key: "name",
    slots: { title: "customTitle" },
    scopedSlots: { customRender: "name" },
  },
  {
    title: "Age",
    dataIndex: "age",
    key: "age",
  },
  {
    title: "Address",
    dataIndex: "address",
    key: "address",
  },
  {
    title: "Tags",
    key: "tags",
    dataIndex: "tags",
    scopedSlots: { customRender: "tags" },
  },
  {
    title: "Action",
    key: "action",
    scopedSlots: { customRender: "action" },
  },
];

const _data = [
  {
    key: "1",
    name: "John Brown",
    age: 32,
    address: "New York No. 1 Lake Park",
    tags: ["nice", "developer"],
  },
  {
    key: "2",
    name: "Jim Green",
    age: 42,
    address: "London No. 1 Lake Park",
    tags: ["loser"],
  },
  {
    key: "3",
    name: "Joe Black",
    age: 32,
    address: "Sidney No. 1 Lake Park",
    tags: ["cool", "teacher"],
  },
];
export default {
  name: "main-page",
  props: {
    // tableData: _data,
    // columns: _columns
  },
  data() {
    return {
      tableData: [
        {
          key: "1",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park",
          tags: ["nice", "developer"],
        },
        {
          key: "2",
          name: "Jim Green",
          age: 42,
          address: "London No. 1 Lake Park",
          tags: ["loser"],
        },
        {
          key: "3",
          name: "Joe Black",
          age: 32,
          address: "Sidney No. 1 Lake Park",
          tags: ["cool", "teacher"],
        },
      ],
      tableColumns: [
        {
          dataIndex: "name",
          key: "name",
          slots: { title: "customTitle" },
          scopedSlots: { customRender: "name" },
        },
        {
          title: "Age",
          dataIndex: "age",
          key: "age",
        },
        {
          title: "Address",
          dataIndex: "address",
          key: "address",
        },
        {
          title: "Tags",
          key: "tags",
          dataIndex: "tags",
          scopedSlots: { customRender: "tags" },
        },
        {
          title: "Action",
          key: "action",
          scopedSlots: { customRender: "action" },
        },
      ],
      collapsed: false,
    };
  },
  // components: { SystemInformation },
  methods: {},
};
</script>

<style>
.green {
  color: green;
  font-weight: bold;
}
#app-header {
  height: 40px;
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
#components-layout-demo-basic .ant-layout-header {
  height: 40px;
  background: white;
}
</style>
