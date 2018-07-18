import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/Home.vue'
import Login from '@/Login.vue'
import Register from '@/Register.vue'

Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
  ]
})