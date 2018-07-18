<template>
  <div>        
    <b-container fluid>
        <b-row>
            <b-col cols="4" md="6" sm="10" offset="4" offset-md="3" offset-sm="1">
                <b-card style="margin-top: 2rem; box-shadow: 0px 0px 15px rgb(0,0,0,0.3);">
                <b-container style="padding-left: 2rem; padding-right: 2rem;">
                    <b-row class="my-1" style="justify-content: center;">
                    <h3 style="text-align: center;">Sign up</h3>
                    </b-row>
                    <b-row class="my-1" style="padding-top: 1rem;">
                    <label for="usernameLive">Username:</label>
                    <b-form-input id="usernameLive"
                                    v-model="input_username"
                                    type="text"
                                    :state="nameState"
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
                                    :state="passwordState"
                                    placeholder="Enter your password">
                    </b-form-input>
                    <b-form-invalid-feedback id="passLiveFeedback">
                        Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number
                    </b-form-invalid-feedback>
                    </b-row>
                    <b-row class="my-1" style="padding-top: 1rem;">
                    <div>
                        <b-button @click="onSignup" variant="success">Sign up</b-button>
                        <b-button @click="view = 'signin'" variant="outline-primary" style="opacity: 0.8">Already registered? Sign in.</b-button>
                    </div>
                    </b-row>
                </b-container>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import DataUploadView from "./components/DataUploadView"
import CallContractView from "./components/CallContractView"

const usernamePattern = /^[a-zA-Z0-9_-]{3,16}$/;
const passwordPattern = /^.*(?=.{6,32}$)(?=.*\d)(?=.*[A-Z])(?=.*[a-z])/;


export default {
  name: "Home",
  data() {
    return {
      user: { name: '', key: null },
      input_username: '',
      input_password: '',
      view: 'signin',
    };
  },
  components: {
    DataUploadView,
    CallContractView
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
    onSignup() {
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
