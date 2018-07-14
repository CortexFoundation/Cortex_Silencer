<template>
  <div class="upload-form">
    <b-jumbotron bg-variant="dark" class = "form-content">
      <template slot="header">
        Cortex Silencer
      </template>
      <b-form-group label="">
        <b-form-radio-group id="btnradios1"
                            buttons
                            v-model="selected"
                            :options="options"
                            name="radiosBtnDefault" />
      </b-form-group>
      <hr class="my-4">
      <template v-if="selected=='blocks'">
      </template>
      <template v-if="selected=='input_data'">
        <p> Upload Image (.png .jpg .jpeg, size &lt; 200K) </p>
        <b-form-file v-model="file" class="mt-3"></b-form-file>
        <b-button @click="clear()" >Clear</b-button>
        <b-button variant="primary" @click="upload(file)" >Upload</b-button>
        <b-alert :key="input_data" v-for="input_data in input_datas" show variant="light" class="form-message">
          <h4 class="alert-heading">Well done!</h4>
          <p>payload: {{ input_data && input_data.msg }}</p>
          <b-button variant="secondary" @click="getTransaction(input_data)" >Get Transaction</b-button>
          <b-table hover :items="Object.entries(input_data.transaction || {})"></b-table>
          <p>receipt: {{ input_data && input_data.receipt }} </p>
        </b-alert>
      </template>
    </b-jumbotron>
  </div>
</template>

<script>
import * as RLP from "RLP";
import { Buffer } from "safe-buffer";

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
  name: "HelloWorld",
  data() {
    return {
      msg: null,
      file: null,
      selected: 'input_data',
      options: [
        { text: 'Blocks', value: 'blocks' },
        { text: 'Input Data', value: 'input_data' },
      ],
      input_datas: [],
    };
  },
  methods: {
    clear() {
      return;
    },
    getTransaction(data) {
      web3.eth.getTransaction(data.transactionHash,
        (err, transaction) => {
          data.transaction = transaction;
          web3.eth.getTransactionReceipt(transaction.hash, (err, receipt) => {
            data.receipt = receipt;
          });
        });
    },
    upload(file) {
      var formdata = new FormData();
      const ret = {
        transactionHash: '',
        msg: '',
        transaction: {},
      };
      formdata.append("file", file);
      var parma = { type: "input_data", author: web3.eth.defaultAccount };
      formdata.append("json", new Blob([JSON.stringify(parma)], { type: "application/json" }));

      this.$http.post("http://192.168.5.11:5000/txion", formdata, {emulateJSON: true})
        .then((response) => {
          ret.msg = "0x0002" + createPayload(response.body.info);
          return ret.msg;
        })
        .then((msg) => {
          web3.eth.sendTransaction({
            to: null,
            from: web3.eth.coinbase,
            gasPrice: 1000000000,
            gas: 2100000,
            value: 0,
            input: msg,
          }, (err, transactionHash) => {
            ret.transactionHash = transactionHash;
            this.input_datas.push(ret);
          });
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
