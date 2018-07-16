<template>
  <div class="upload-form">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="InputGroup1"
                    label="Sender:"
                    label-for="senderAddrInput"
                    description="We'll never share your address with anyone else.">
        <b-form-input id="senderAddrInput"
                      type="text"
                      v-model="form.sender"
                      required
                      placeholder="Enter address">
        </b-form-input>
      </b-form-group>
      <b-form-group id="InputGroup2"
                    label="Recipient:"
                    label-for="recipientAddrInput">
        <b-form-input id="recipientAddrInput"
                      type="text"
                      v-model="form.recipient"
                      placeholder="Enter address">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <hr class="my-4">
  </div>
</template>

<script>
import * as RLP from "rlp";
import { Buffer } from "safe-buffer";
import { promisify } from "es6-promisify";

function parseHexString(str) {
  var result = [];
  for (var i = 0; i < str.length; i += 2) {
    result.push(parseInt(str.substring(i, i + 2), 16));
  }
  return Buffer.from(result);
}

function createHexString(arr) {
  const str = "0123456789abcdef";
  return "".concat(...Array.from(arr).map(d => "" + str[d >> 4] + str[d & 15]));
}

function createPayload(jsondata) {
  let ret = "";
  try {
    const addrBytes = Buffer.from(jsondata["AuthorAddress"]);
    const addr = addrBytes.slice(addrBytes.length - 20);
    const hash = parseHexString(jsondata["Hash"].slice(2));
    const listdata = [hash, jsondata["RawSize"], jsondata["Shape"], addr];
    ret = createHexString(RLP.encode(listdata));
  } catch (e) {}
  return ret;
}

export default {
  name: "CallContractView",
  data() {
    return {
      msg: null,
      input_datas: [],
      form: {
        file: null,
        sender: this.web3.eth.coinbase,
        recipient: null,
      },
      show: true
    };
  },
  methods: {
    async onSubmit(evt) {
      var formdata = new FormData();
      formdata.append("file", this.form.file);
      var parma = { type: "input_data", author: web3.eth.defaultAccount };
      formdata.append("json", new Blob([JSON.stringify(parma)], { type: "application/json" }));
    },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      this.form.sender = '';
      this.form.recipient = null;
      this.form.file = null;
      this.show = false;
      this.$nextTick(() => { this.show = true });
    },
    getTransactionReceipt(data) {
      this.web3.eth.getTransactionReceipt(data.transaction.hash, (err, receipt) => {
        data.receipt = receipt;
      });
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.upload-form {
  width: 100%;
  margin-top: 2em;
  margin-bottom: 2em;
}

.form-content {
  width: 100%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}

.form-message {
  margin-top: 2em;
  margin-bottom: 2em;
}

.custom-file-label {
  border-color: lightgray !important;
}

.b-form-file {
  margin-bottom: 1em;
}
.b-form-group {
  margin-top: 2em;
}

</style>
