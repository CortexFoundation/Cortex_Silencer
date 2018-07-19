<template>
  <div id="app">
    <b-navbar class="cortex-header" toggleable="md" type="dark" variant="dark">
      <b-navbar-brand @click="$router.replace('/')">
        <img src="./assets/logo.png" style="hegith: 28px; width: 28px;">
        Cortex
      </b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right v-if="true">
            <template slot="button-content">
              <em>{{ web3.eth.defaultAccount.toLowerCase() }}</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
          </b-nav-item-dropdown>
          <template v-else>
            <b-nav-item href="#" @click="$router.replace('/login')">Sign in</b-nav-item>
            <b-button @click="$router.replace('/register')">Sign up</b-button >
          </template>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view/>
  </div>
</template>

<script>
import bus from "./components/bus"
export default {
  name: 'App',
  data() {
    return {
      user: { name: '', key: null },
    };
  },
  created() {
    this.user = sessionStorage['cortex_current_user'] || this.user;
    bus.$on("login", (username, key) => {
      this.user.name = username;
      this.user.key = key;
    })
  }
}
</script>

<style>
body {
  background: rgb(0, 0, 0, .05);
}
</style>