<template>
  <div class="upload-form">
    <b-jumbotron bg-variant="dark" class = "form-content">
      <template slot="header">
        Cortex
      </template>
      <hr class="my-4">
      <b-row>
        <b-col cols="11">
          <b-form-file v-model="file" :state="Boolean(file)" accept="image/*" placeholder="Choose a file..."></b-form-file>
        </b-col>
        <b-col cols="1">
          <b-button variant="secondary" @click="upload(file)" >Upload</b-button>
        </b-col>
      </b-row>
      
      <b-alert v-if="msg" show variant="light" class="form-message">
        <h4 class="alert-heading">Well done!</h4>
        <p>payload: {{ msg }}</p>
        <b-button variant="secondary" @click="getTransaction()" >Get Transaction</b-button>
        <p>transaction: {{ transaction }} </p>
        <p>receipt: {{ receipt }} </p>
      </b-alert>
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
      transactionHash: null,
      transaction: null,
      receipt: null,
    };
  },
  methods: {
    createPayload(msg) {
      return createPayload(msg);
    },
    getTransaction() {
      web3.eth.getTransaction(this.transactionHash,
        (err, transaction) => {
          console.log(transaction);
          this.transaction = transaction;
          web3.eth.getTransactionReceipt(transaction.hash, (err, receipt) => {
            console.log(receipt);
            this.receipt = receipt;
          });
        });
    },
    upload(file) {
      var formdata = new FormData();
      formdata.append("file", file);
      var parma = { type: "input_data", author: '$.mineraddr' };
      formdata.append("json", new Blob([JSON.stringify(parma)], { type: "application/json" }));
      this.$http.post("http://192.168.5.11:5000/txion", formdata, {emulateJSON: true})
        .then((response) => {
          this.msg = "0x0002" + createPayload(response.body.info);
          return this.msg;
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
            this.transactionHash = transactionHash;
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

</style>
