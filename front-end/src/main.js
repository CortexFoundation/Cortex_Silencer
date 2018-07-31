// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import VueResource from 'vue-resource'
Vue.use(VueResource);

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Router from 'vue-router'
Vue.use(Router)

import { Tabs, Tab } from 'vue-tabs-component'
import router from './router'
import App from './App'
import Web3 from 'web3'

import WebTorrent from 'WebTorrent'

Vue.prototype.torrentClient = new WebTorrent({ tracker: false })

if (typeof web3 !== 'undefined') {
  Vue.prototype.web3 = new Web3(web3.currentProvider);
  Vue.prototype.web3.eth.defaultAccount = web3.eth.defaultAccount;
} else {
  Vue.prototype.web3 = new Web3(new Web3.providers.HttpProvider("http://192.168.5.11:8845"));
}

Vue.config.productionTip = false
Vue.component('tabs', Tabs);
Vue.component('tab', Tab);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
