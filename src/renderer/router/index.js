import Vue from 'vue'
import Router from 'vue-router'
import Antd from 'ant-design-vue/es'
import 'ant-design-vue/dist/antd.less'
Vue.use(Antd)
Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'landing-page',
    //   component: require('@/components/LandingPage').default
    // },
    {
      path: '/',
      name: 'main-page',
      component: require('@/components/MainPage').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
