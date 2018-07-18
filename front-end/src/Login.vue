<template>
    <b-container fluid>
        <b-row>
            <b-col cols="4" md="6" sm="10" offset="4" offset-md="3" offset-sm="1">
                <b-card style="margin-top: 2rem; box-shadow: 0px 0px 15px rgb(0,0,0,0.3);">
                <b-container style="padding-left: 2rem; padding-right: 2rem;">
                    <b-row class="my-1" style="justify-content: center;">
                    <h2>Sign in</h2>
                    </b-row>
                    <b-row class="my-1" style="padding-top: 1rem;">
                    <label for="usernameLive">Username:</label>
                    <b-form-input id="usernameLive"
                                    v-model="input_username"
                                    type="text"
                                    :state="state"
                                    placeholder="Enter your username">
                    </b-form-input>
                    <b-form-invalid-feedback id="usernameLiveFeedback">
                        Enter at least 3 letters
                    </b-form-invalid-feedback>
                    </b-row>
                    <b-row class="my-1" style="padding-top: 1rem;">
                    <label for="passLive">Password:</label>
                    <b-form-input id="passLive"
                                    v-model="input_password"
                                    type="password"
                                    :state="state"
                                    placeholder="Enter your password">
                    </b-form-input>
                    <b-form-invalid-feedback id="passwordLiveFeedback">
                        Enter at least 3 letters
                    </b-form-invalid-feedback>
                    </b-row>
                    <b-row class="my-1" style="padding-top: 1rem;">
                    <div>
                        <b-button @click="verify" variant="primary">Sign in</b-button>
                        <b-button @click="$router.replace('/register')" variant="outline-success" style="opacity: 0.8">  New here? Sign up for Cortex now.  </b-button>
                    </div>
                    </b-row>
                </b-container>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import bus from "@/components/bus";

const usernamePattern = /^[a-zA-Z0-9_-]{3,16}$/;
const passwordPattern = /^.*(?=.{6,32}$)(?=.*\d)(?=.*[A-Z])(?=.*[a-z])/;

export default {
  name: "Login",
  data() {
    return {
      user: { name: '', key: null },
      input_username: '',
      input_password: '',
      state: null,
    };
  },
  components: {
  },
  computed: {
  },
  methods: {
    verify() {
      const username = 'cortex_username_' + this.input_username;
      const password = this.web3.utils.sha3(this.input_password);
      if (localStorage[username] == password) {
        const token = this.web3.utils.sha3(Math.random().toString());
        bus.$emit('login', this.input_username, token);
        this.$router.replace("/");
      }
    }
  },
  created() {
    this.user = sessionStorage['cortex_silencer_test_user'] || this.user;
  }
};
</script>

<style>
</style>
