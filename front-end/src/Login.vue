<template>
    <b-container fluid>
        <b-row>
        <b-col cols="4" md="6" sm="10" offset="4" offset-md="3" offset-sm="1">
            <b-card style="margin-top: 2rem; box-shadow: 0px 0px 15px rgb(0,0,0,0.3);">
            <b-container style="padding-left: 2rem; padding-right: 2rem;">
                <b-row class="my-1" style="justify-content: center;">
                <h3>Sign in</h3>
                </b-row>
                <b-row class="my-1" style="padding-top: 1rem;">
                <label for="usernameLive">Username:</label>
                <b-form-input id="usernameLive"
                                v-model="input_username"
                                type="text"
                                placeholder="Enter your username">
                </b-form-input>
                </b-row>
                <b-row class="my-1" style="padding-top: 1rem;">
                <label for="passLive">Password:</label>
                <b-form-input id="passLive"
                                v-model="input_password"
                                type="password"
                                placeholder="Enter your password">
                </b-form-input>
                </b-row>
                <b-row class="my-1" style="padding-top: 1rem;">
                <div>
                    <b-button @click="onSignin" variant="primary">Sign in</b-button>
                    <b-button @click="view = 'signup'" variant="outline-success" style="opacity: 0.8">  New here? Sign up for Cortex now.  </b-button>
                </div>
                </b-row>
            </b-container>
            </b-card>
        </b-col>
        </b-row>
    </b-container>
</template>

<script>
const usernamePattern = /^[a-zA-Z0-9_-]{3,16}$/;
const passwordPattern = /^.*(?=.{6,32}$)(?=.*\d)(?=.*[A-Z])(?=.*[a-z])/;

export default {
  name: "Login",
  data() {
    return {
      user: { name: '', key: null },
      input_username: '',
      input_password: '',
      view: 'signin',
    };
  },
  components: {
  },
  computed: {
    nameState () {
      return usernamePattern.test(this.input_username);
    },
    passwordState () {
      return passwordPattern.test(this.input_password);
    }
  },
  methods: {
    onSignin() {
      this.user.name = this.input_username;
      this.user.key = this.input_password;
    },
  },
  created() {
    this.user = sessionStorage['cortex_silencer_test_user'] || this.user;
  }
};
</script>

<style>
</style>
